from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from sales.models import order
from api.serializers import orderSerializer

# Create your views here.

@csrf_exempt
def api_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        apivar = order.objects.all()
        serializer = orderSerializer(apivar, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = orderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

