from django.urls import path
from .views import submit_feedback, post_failed_prompt

urlpatterns = [
    path('feedback/', submit_feedback, name='feedback'),
    path('failed-prompt/', post_failed_prompt, name='failed-prompt'),
]
