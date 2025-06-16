import logging

from rest_framework import views, permissions, parsers, status
from rest_framework.response import Response

from .face_utils import match_face

logger = logging.getLogger(__name__)


class IdentifyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def post(self, request):
        """Handle face identification from uploaded image."""
        file = request.FILES.get("file")
        if not file:
            logger.warning("#IdentifyView No file provided in request")
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file type
        if not file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            logger.warning(f"#IdentifyView Invalid file type: {file.name}")
            return Response({"error": "Only JPG and PNG files are supported"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file size (e.g., max 5MB)
        if file.size > 5 * 1024 * 1024:
            logger.warning(f"#IdentifyView File too large: {file.size} bytes")
            return Response({"error": "File size exceeds 5MB limit"}, status=status.HTTP_400_BAD_REQUEST)

        result = match_face(file)
        return Response(result, status=status.HTTP_200_OK)
