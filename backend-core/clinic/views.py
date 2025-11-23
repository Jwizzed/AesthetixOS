from rest_framework import viewsets, views, status
from rest_framework.response import Response
from core.services.storage import MinIOService
from .models import Patient, TreatmentSession, ClinicalImage
from .serializers import PatientSerializer, TreatmentSessionSerializer, ClinicalImageSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class TreatmentSessionViewSet(viewsets.ModelViewSet):
    queryset = TreatmentSession.objects.all()
    serializer_class = TreatmentSessionSerializer

class UploadTokenView(views.APIView):
    """
    Generates a presigned URL for direct-to-MinIO uploads.
    """
    def get(self, request):
        service = MinIOService()
        # Optional: get extension from query param, default to jpg
        file_extension = request.query_params.get('ext', 'jpg')
        
        url, key = service.generate_presigned_url(file_extension=file_extension)
        
        if not url:
            return Response({"error": "Storage service unavailable"}, status=503)
            
        return Response({
            "upload_url": url, 
            "key": key
        })

class ConfirmUploadView(views.APIView):
    """
    Links an uploaded S3 key to a Treatment Session.
    """
    def post(self, request):
        session_id = request.data.get('session_id')
        s3_key = request.data.get('key')
        image_type = request.data.get('image_type', 'BEFORE')

        if not session_id or not s3_key:
            return Response({"error": "Missing session_id or key"}, status=400)
        
        try:
            session = TreatmentSession.objects.get(id=session_id)
            image = ClinicalImage.objects.create(
                session=session,
                s3_key=s3_key,
                image_type=image_type
            )
            return Response(ClinicalImageSerializer(image).data, status=201)
        except TreatmentSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=404)
        except Exception as e:
             return Response({"error": str(e)}, status=500)
