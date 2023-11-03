from django.urls import path
from . import views

urlpatterns = [
    path('process_pdf/', views.ProcessPdfView.as_view(), name='process_pdf'),
    path('health-check/', views.health_check, name='health_check'),
]
