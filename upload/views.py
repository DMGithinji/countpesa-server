from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            content = file.read().decode('utf-8')
            UploadedFile.objects.create(content=content)
            return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
