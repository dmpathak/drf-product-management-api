import json
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from projectmanagement.serializers import UploadSerializer
from utils.tasks import process_bulk_upload


class UploadView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = UploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return Response(
                {"message": "Invalid JSON file"},
                status=400
            )

        process_bulk_upload.delay(data)

        return Response({"message": "Processing started"})
