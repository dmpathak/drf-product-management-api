import json
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.tasks import process_upload


class UploadView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        process_upload.delay(data)

        return Response({"message": "Processing started In Background"})
