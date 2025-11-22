# Project Specification: AesthetixOS
### Modular Clinic Resource Planning (ERP) System

**AesthetixOS** is a cloud-native ERP solution tailored for the aesthetic medicine industry. It addresses the specific challenges of high-resolution medical imaging, complex therapist commission structures, and strictly segmented workflows (Clinical vs. Commercial).

The system is architected as a **Monorepo** utilizing **Micro-Frontends** to decouple domain logic and a **Django** backend optimized for asynchronous processing and secure data handling.

---

## 1. High-Level Architecture

### Core Design Patterns
*   **Micro-Frontends (Module Federation):** The frontend is split into a "Host" (Shell) and separate "Remotes" for EMR (Electronic Medical Records) and POS (Point of Sale). This ensures independent deployability and strict separation of concerns.
*   **Direct-to-Object Storage:** High-resolution clinical photos bypass the application server, uploading directly to MinIO (S3 compatible) via Presigned URLs to reduce latency and server load.
*   **Asynchronous Computing:** Complex commission calculations are offloaded to a background task queue (Celery) to ensure the POS terminal remains non-blocking during checkout.
*   **Design System:** A shared UI library ensures visual consistency across all micro-applications.

---

## 2. Repository Structure (Monorepo)

```text
/aesthetix-os
│
├── /packages                  # Shared Frontend Logic
│   └── /ui-kit                # Internal Design System (Buttons, Inputs, Tables)
│
├── /backend-core              # Python/Django API
│   ├── /core                  # Settings, Auth, middleware
│   ├── /clinic                # App: EMR, Photos, PDPA logic
│   ├── /commerce              # App: Inventory, Courses, Ledger
│   ├── /tasks                 # Celery tasks (Commission calculation)
│   ├── manage.py
│   └── Dockerfile
│
├── /frontend-host             # Vue.js (Application Shell)
│   ├── /src                   # Auth, Navigation, Layouts
│   ├── vite.config.js         # Federation: HOST
│   └── Dockerfile
│
├── /frontend-remote-emr       # Vue.js (Medical Module)
│   ├── /src                   # Face Charting, Image Gallery
│   ├── vite.config.js         # Federation: REMOTE (exposes 'PatientModule')
│   └── Dockerfile
│
├── /frontend-remote-pos       # Vue.js (Cashier Module)
│   ├── /src                   # Course Grid, Checkout Flow
│   ├── vite.config.js         # Federation: REMOTE (exposes 'BillingModule')
│   └── Dockerfile
│
└── docker-compose.yml         # Infrastructure Orchestration
```

---

## 3. Technology Stack

| Layer | Technology | Key Libraries/Tools |
| :--- | :--- | :--- |
| **Backend** | Python 3.11 | **Django 5.0**, **DRF**, **Celery** (Async), **Boto3** (S3/MinIO), **Pytest** |
| **Database & Cache** | SQL / NoSQL | **PostgreSQL 15** (Relational), **Redis** (Broker/Cache), **MinIO** (Object Storage) |
| **Frontend (Core)** | JavaScript | **Vue.js 3** (Composition API), **Vite**, **Pinia** (State), **TypeScript** |
| **Frontend (Arch)** | Federation | **vite-plugin-federation**, **Lerna** or **npm workspaces** (Monorepo tools) |
| **UI & Style** | Styling | **TailwindCSS**, **Headless UI** (Accessible components) |
| **Infra** | Containerization | **Docker**, **Docker Compose**, **Nginx** (Reverse Proxy) |

---

## 4. Backend Specifications (Django)

The backend exposes a RESTful API (`/api/v1/`).

### Module A: Clinical Operations (`/clinic`)
**Focus:** Medical Data, PDPA Compliance, Image Handling.

1.  **Feature: Zero-Trust Image Uploads (Presigned URLs)**
    *   *Problem:* Uploading 4K "Before/After" photos crashes standard HTTP threads.
    *   *Solution:*
        *   Endpoint `GET /api/v1/clinic/upload-token/`: Returns a temporary MinIO Presigned URL.
        *   Client uploads file directly to MinIO storage.
        *   Endpoint `POST /api/v1/clinic/confirm-upload/`: Client notifies backend to link the S3 key to the `TreatmentSession` model.
2.  **Feature: Role-Based Data Masking (PDPA)**
    *   *Logic:* Custom DRF Serializer Field (`PDPAMaskingField`).
    *   *Behavior:* Checks `request.user.role`.
        *   If `Doctor`: Returns `081-555-0101`.
        *   If `Receptionist`: Returns `081-XXX-0101`.

### Module B: Commerce & Revenue (`/commerce`)
**Focus:** Financials, Inventory, Commissions.

1.  **Feature: Asynchronous Commission Engine**
    *   *Problem:* Calculating multi-tier commissions (e.g., "10% if sales > 100k, else 5%", split between 2 therapists) freezes the POS.
    *   *Solution:*
        *   Checkout triggers `tasks.calculate_commission.delay(transaction_id)`.
        *   Celery Worker processes logic in background.
        *   Updates `CommissionLog` model.
        *   Frontend polls or receives WebSocket update when calculation completes.
2.  **Feature: Event-Driven Data Signals**
    *   *Logic:* Uses Django Signals (`post_save`).
    *   *Purpose:* When `UserCourseBalance` is deducted, a signal is emitted. Ideally formatted to be structurally ready for a Message Broker (Kafka) to demonstrate readiness for Data Lake integration.

---

## 5. Frontend Specifications (Vue.js Micro-Frontends)

### Service 1: Shared UI Kit (`@aesthetix/ui-kit`)
*   **Role:** Internal npm package / submodule.
*   **Content:** Atomic components (`BaseButton`, `InputGroup`, `Modal`) styled with Tailwind.
*   **Why:** Ensures the EMR and POS modules look identical to the Host, simulating a unified Design System.

### Service 2: Host Application (`frontend-host`)
*   **Port:** 3000
*   **Responsibilities:**
    *   **Global Auth:** Login Page. Stores JWT in `localStorage`.
    *   **Event Bus:** Listens for global events (e.g., `SESSION_EXPIRED`) to trigger redirects.
    *   **Layout:** Top navigation and Sidebar.
    *   **Federation:** Dynamically imports Remotes based on routes.

### Service 3: Remote EMR (`frontend-remote-emr`)
*   **Port:** 3001
*   **Key Component:** `<FaceCanvas />`
    *   Uses HTML5 Canvas API.
    *   Allows doctors to draw injection points over the patient's photo.
    *   Saves annotation coordinates (JSON) to the backend.

### Service 4: Remote POS (`frontend-remote-pos`)
*   **Port:** 3002
*   **Key Component:** `<SmartCourseGrid />`
    *   Reactive product selection.
    *   Real-time subtotal calculation (Client-side) before confirming payment.

---

## 6. Infrastructure & DevOps

### Docker Composition
The system runs on a unified network defined in `docker-compose.yml`.

```yaml
services:
  # --- Data Layer ---
  db:
    image: postgres:15
    volumes: [pgdata:/var/lib/postgresql/data]
  
  redis:
    image: redis:7-alpine
  
  minio: # S3 Compatible Object Storage
    image: minio/minio
    command: server /data --console-address ":9001"
    ports: ["9000:9000", "9001:9001"]

  # --- Backend Layer ---
  backend:
    build: ./backend-core
    depends_on: [db, redis, minio]
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - AWS_S3_ENDPOINT_URL=http://minio:9000

  celery_worker:
    build: ./backend-core
    command: celery -A core worker -l info
    depends_on: [backend, redis]

  # --- Frontend Layer ---
  host:
    build: ./frontend-host
    ports: ["3000:3000"]
    
  remote-emr:
    build: ./frontend-remote-emr
    ports: ["3001:3001"]
    
  remote-pos:
    build: ./frontend-remote-pos
    ports: ["3002:3002"]
```

### Testing Strategy
*   **Backend:** `pytest` for Unit Tests on commission logic. `APIClient` tests for PDPA masking verification.
*   **Frontend:** `Vitest` for testing the shared `ui-kit` components to ensure stability across micro-frontends.

---

## 7. Implementation Roadmap

1.  **Phase 1: Infrastructure Core**
    *   Setup Monorepo.
    *   Configure Docker Compose (Postgres, Redis, MinIO).
    *   Initialize Django project.
2.  **Phase 2: Backend Logic**
    *   Implement Models (Patient, Treatment, Course).
    *   Build Auth & PDPA Middleware.
    *   Setup Celery & MinIO Boto3 configuration.
3.  **Phase 3: Frontend Foundation**
    *   Create Host App (Shell).
    *   Build `@aesthetix/ui-kit`.
    *   Configure Vite Federation (expose/remote).
4.  **Phase 4: Vertical Implementation**
    *   Develop EMR (Canvas + Uploads).
    *   Develop POS (Grid + Async Commission check).
5.  **Phase 5: Integration & Polish**
    *   End-to-end flow testing.
    *   Documentation & API Specs (Swagger/OpenAPI).