import logging
import json

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from upload.statement_parser.encryption_utils import decrypt, encrypt
from .statement_parser.parser import get_pdf_text, parse_statement_text

# Initialize logger
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class ProcessPdfView(View):

    def post(self, request, *args, **kwargs):
        try:
            uploaded_file = request.FILES.get('statement', None)
            password = request.POST.get('password', None)

            if not password or not uploaded_file:
                response = {'status': 'error', 'message': 'Payload is not valid'}
                return JsonResponse(response)

            pdf_data = get_pdf_text(uploaded_file, password)

            if (pdf_data.get('error', None)):
                response = {'status': 'error', 'message': pdf_data['error']}
                return JsonResponse(response)

            text_content = pdf_data.get('text', None)
            statement_list = text_content.split("\n")
            parsed_statement = parse_statement_text(statement_list)

            response = {
                'status': 'success',
                'message': 'PDF processed successfully',
                'results': parsed_statement
            }

            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})

@method_decorator(csrf_exempt, name='dispatch')
class ProcessPdfWithEncryptedPasswordView(View):

    def post(self, request, *args, **kwargs):
        try:
            uploaded_file = request.FILES.get('statement', None)
            encrypted_password = request.POST.get('password', None)
            password = decrypt(encrypted_password)
            print(password)

            if not (password and uploaded_file):
                response = {'status': 'error', 'message': 'Payload is not valid'}
                return JsonResponse(response)

            pdf_data = get_pdf_text(uploaded_file, password)

            if (pdf_data.get('error', None)):
                response = {'status': 'error', 'message': pdf_data['error']}
                return JsonResponse(response)

            text_content = pdf_data.get('text', None)
            statement_list = text_content.split("\n")
            parsed_statement = parse_statement_text(statement_list)
            json_string = json.dumps(parsed_statement)
            encrypted_payload = encrypt(json_string)

            response = {
                'status': 'success',
                'message': 'PDF processed successfully',
                'results': encrypted_payload
            }

            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})

def health_check(request):
    return JsonResponse({'status': 'OK'}, status=200)
