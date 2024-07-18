import json
import logging
from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, PermissionDenied

from .parsers.statement_parser import get_parsed_statement
from .utils.encryption_utils import decrypt, encrypt

logger = logging.getLogger(__name__)

class BasePdfProcessView(View):
    """Base class for PDF processing views."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def process_pdf(self, statement: UploadedFile, password: str) -> dict:
        """Process the PDF file and return the parsed statement."""
        raise NotImplementedError("Subclasses must implement process_pdf method")

    def post(self, request, *args, **kwargs):
        try:
            statement = request.FILES.get('statement')
            password = self.get_password(request)

            if not (password and statement):
                raise ValidationError("Missing statement file or password")

            parsed_statement = self.process_pdf(statement, password)
            return self.success_response(parsed_statement)

        except ValidationError as e:
            logger.warning(f"Invalid input: {str(e)}")
            return self.error_response(str(e), status=400)
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return self.error_response(str(e), status=403)
        except Exception as e:
            logger.exception("Unexpected error occurred")
            return self.error_response("An unexpected error occurred", status=500)

    def get_password(self, request) -> Optional[str]:
        """Extract password from request. Override in subclasses if needed."""
        return request.POST.get('password')

    def success_response(self, data: dict) -> JsonResponse:
        """Return a success response with the given data."""
        return JsonResponse({
            'status': 'success',
            'message': 'PDF processed successfully',
            'results': data
        })

    def error_response(self, message: str, status: int = 400) -> JsonResponse:
        """Return an error response with the given message and status code."""
        return JsonResponse({'status': 'error', 'message': message}, status=status)


class ProcessPdfView(BasePdfProcessView):
    """View for processing PDF with plain text password."""

    def process_pdf(self, statement: UploadedFile, password: str):
        return get_parsed_statement(statement, password)


class ProcessPdfWithEncryptedPasswordView(BasePdfProcessView):
    """View for processing PDF with encrypted password."""

    def get_password(self, request) -> Optional[str]:
        encrypted_password = request.POST.get('password')
        if encrypted_password:
            try:
                return decrypt(encrypted_password)
            except Exception as e:
                logger.error(f"Failed to decrypt password: {str(e)}")
                raise PermissionDenied("Invalid encrypted password")
        return None

    def process_pdf(self, statement: UploadedFile, password: str):
        parsed_statement = get_parsed_statement(statement, password)
        parsed_trs = json.dumps(parsed_statement)
        try:
            return encrypt(parsed_trs)
        except Exception as e:
            logger.error(f"Failed to encrypt parsed statement: {str(e)}")
            raise

def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({'status': 'OK'}, status=200)
