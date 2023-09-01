from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
import pdfplumber
from io import BytesIO
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['file']
            logger.info("Received a new file upload request.")

            if not pdf_file.name.endswith('.pdf'):
                logger.warning("Invalid file type attempted to upload.")
                return render(request, 'upload.html', {'form': form, 'error': 'Invalid file type'})

            pdf_bytes = BytesIO(pdf_file.read())
            content = ''

            with pdfplumber.open(pdf_bytes) as pdf:
                for page in pdf.pages:
                    content += page.extract_text()
                    print(content)

            UploadedFile.objects.create(content=content)
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
