from django import forms

class UploadFileForm(forms.Form):
    pdf_file = forms.FileField()
    password = forms.CharField(
            widget=forms.PasswordInput(),
            required=False,
            label='PDF Password (if encrypted)'
        )