## Frontend
```
# 1. Initialize Root
pnpm init
touch pnpm-workspace.yaml

# 2. Configure Workspace (Add this content to pnpm-workspace.yaml)
echo "packages:
  - 'frontend-*'
  - 'packages/*'" > pnpm-workspace.yaml

# 3. Scaffold Micro-Frontends (Vue + TypeScript)
pnpm create vite frontend-host --template vue-ts
pnpm create vite frontend-remote-emr --template vue-ts
pnpm create vite frontend-remote-pos --template vue-ts

# 4. Scaffold Shared UI Kit
mkdir -p packages/ui-kit
cd packages/ui-kit
pnpm init
cd ../..

# 5. Install shared dependencies (like Tailwind)
pnpm install -w -D tailwindcss postcss autoprefixer
```

## Backend
```
# 1. Create Backend Directory
mkdir backend-core
cd backend-core

# 2. Initialize with uv (creates pyproject.toml & .venv)
uv init
uv python install 3.11

# 3. Install Core Dependencies
uv add django djangorestframework celery redis boto3 django-cors-headers psycopg2-binary gunicorn

# 4. Start Django Project (named 'core' to match your spec)
uv run django-admin startproject core .

# 5. Create Domain Apps
uv run python manage.py startapp clinic
uv run python manage.py startapp commerce

# 6. Return to root
cd ..
```