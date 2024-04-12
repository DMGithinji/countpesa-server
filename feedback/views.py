import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task
from .g_sheet import post_feedback_data, post_failed_chatpesa_questions

@csrf_exempt
@require_http_methods(["POST"])
def submit_feedback(request):

    try:
        data = json.loads(request.body)
        async_task(post_feedback_data, data)
        return JsonResponse({"status": "success", "message": "Feedback submitted successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def post_failed_prompt(request):

    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', None)
        response = data.get('response', None)
        # async_task(post_failed_chatpesa_questions, prompt)
        post_failed_chatpesa_questions(prompt, response)
        return JsonResponse({"status": "success", "message": "Submitted successfully"}, status=200)

    except Exception as e:
        error_message = str(e)  # Convert the exception message to a string
        return JsonResponse({"status": "error", "message": error_message}, status=400)
