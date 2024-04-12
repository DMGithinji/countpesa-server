import json

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .parsers.statement_parser import get_parsed_statement
from .utils.encryption_utils import decrypt, encrypt


@method_decorator(csrf_exempt, name='dispatch')
class ProcessPdfView(View):

    def post(self, request, *args, **kwargs):
        try:
            parsered_file = request.FILES.get('statement', None)
            password = request.POST.get('password', None)

            if not (password and parsered_file):
                response = {'status': 'error', 'message': 'Payload is not valid'}
                return JsonResponse(response)

            parsed_statement = get_parsed_statement(parsered_file, password)
            response = {
                'status': 'success',
                'message': 'PDF processed successfully',
                'results': parsed_statement
            }
            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'{str(e)}'})

@method_decorator(csrf_exempt, name='dispatch')
class ProcessPdfWithEncryptedPasswordView(View):

    def post(self, request, *args, **kwargs):
        try:
            parsered_file = request.FILES.get('statement', None)
            encrypted_password = request.POST.get('password', None)
            password = decrypt(encrypted_password)

            if not (password and parsered_file):
                response = {'status': 'error', 'message': 'Payload is not valid'}
                return JsonResponse(response)

            parsed_statement = get_parsed_statement(parsered_file, password)
            parsed_trs = json.dumps(parsed_statement)
            encrypted_trs = encrypt(parsed_trs)
            response = {
                'status': 'success',
                'message': 'PDF processed successfully',
                'results': encrypted_trs
            }
            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'{str(e)}'})

def health_check(request):
    return JsonResponse({'status': 'OK'}, status=200)
