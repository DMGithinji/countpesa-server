from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
import pdfplumber
import fitz  # PyMuPDF
from io import BytesIO
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file'].read()
            password = form.cleaned_data['password']

            logger.info(f"Received a new file upload request. Password {password}")

            try:
                pdf_reader = fitz.open("pdf", pdf_file)
                pdf_reader.authenticate(password)
            except Exception as e:
                logger.error(f"Could not open or decrypt the PDF: {e}")
                return render(request, 'upload.html', {'form': form, 'error': 'Could not open or decrypt PDF'})

            # Reading PDF content with pdfplumber
            text_content = ''
            for page_number in range(len(pdf_reader)):
                page = pdf_reader[page_number]
                text_content += page.get_text("text")

            print(text_content)
            UploadedFile.objects.create(content=text_content)
            logger.info("Successfully processed the PDF and saved the content.")
            return redirect('success')
        else:
            logger.warning("Form is not valid.")
    else:
        form = UploadFileForm()
        logger.info("New file upload form served.")

    return render(request, 'upload.html', {'form': form})


def success(request):
    return render(request, 'success.html')
