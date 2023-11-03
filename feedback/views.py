import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .g_sheet import post_data

@csrf_exempt
@require_http_methods(["POST"])
def submit_feedback(request):

    try:
        data = json.loads(request.body)
        print(data)
        post_data(data)

        return JsonResponse({"status": "success", "message": "Feedback submitted successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
