import logging
import json
from pprint import pprint
from django.shortcuts import render, redirect
import fitz  # PyMuPDF
from .forms import UploadFileForm
from .models import UploadedFile
from .statement_parser.parser import parse_statement_text

# Initialize logger
logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file'].read()
            password = form.cleaned_data['password']

            print(f"Received a new file upload request. Password {password}")

            try:
                pdf_reader = fitz.open(stream=pdf_file, filetype='pdf')
                pdf_reader.authenticate(password)

                if pdf_reader.is_encrypted:
                    logger.error(f'Cannot decrypt file with password {password}')
                    return render(request, 'upload.html', {'form': form, 'error': 'Could not open or decrypt PDF'})
                print(f'Authenticated!')
            except Exception as e:
                logger.error(f"Could not open or decrypt the PDF: {e}")
                return render(request, 'upload.html', {'form': form, 'error': 'Could not open or decrypt PDF'})

            # Reading PDF content with pdfplumber
            text_content = ''
            for page_number in range(len(pdf_reader)):
                page = pdf_reader[page_number]
                text_content += page.get_text("text")

            statement_list = text_content.split("\n")
            parsed_statement = parse_statement_text(statement_list)
            pprint(parsed_statement)

            json_string = json.dumps(parsed_statement)
            upload = UploadedFile.objects.create(content=json_string)

            return redirect('success')
        else:
            logger.warning("Form is not valid.")
    else:
        form = UploadFileForm()
        logger.info("New file upload form served.")

    return render(request, 'upload.html', {'form': form})


def success(request):
    return render(request, 'success.html')
