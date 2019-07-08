from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required(login_url='/')
def fetch_forms(request):
	return JsonResponse({"msg": "ok"})


@login_required(login_url='/')
def fetch_data(request, user_id):
	return JsonResponse({"msg": "ok"})


@login_required(login_url='/')
def offline_mode_test(request):
	if request.method == 'GET':
		return JsonResponse(
			{'msg': "ok testing"}, content_type='application/json', safe=True)
	else:
		print request.body
		return JsonResponse(
			{'msg': "submitted"}, content_type='application/json', safe=True)
