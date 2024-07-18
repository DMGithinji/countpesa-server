import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task
from .g_sheet import post_feedback_data, post_failed_chatpesa_questions

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def submit_feedback(request):

    try:
        data = json.loads(request.body)
        async_task(post_feedback_data, data)
        return JsonResponse({"status": "success", "message": "Feedback submitted successfully"}, status=200)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in feedback submission: {str(e)}")
        return JsonResponse({"status": "error", "message": "Invalid input"}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in feedback submission: {str(e)}")
        return JsonResponse({"status": "error", "message": "Unexpected error occurred"}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def post_failed_prompt(request):

    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', None)
        response = data.get('response', None)
        async_task(post_failed_chatpesa_questions, prompt, response)
        return JsonResponse({"status": "success", "message": "Submitted successfully"}, status=200)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in failed prompt submission: {str(e)}")
        return JsonResponse({"status": "error", "message": "Invalid input"}, status=400)
    except Exception as e:
        logger.error(f"Error occured while posting failed prompt : {str(e)}")
        return JsonResponse({"status": "error", "message": "Unexpected error occurred"}, status=500)
