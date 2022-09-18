import json
import datetime

import pytz
from celery.result import AsyncResult
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.generic import TemplateView
from django.views import View
from django.conf import settings
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.models import CompanyName
from app.tasks import company_name_bulk_create


class IndexView(TemplateView):
    template_name = "app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django Task Scheduler - Version ' + settings.VERSION
        return context


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyName
        fields = ('name', 'create_dt')


class CompanyNameResultsSetPagination(pagination.PageNumberPagination):
    class Meta:
        ordering = ['id']

    page_size = 100
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        """
        Override to add custom parameter.
        """
        return super(CompanyNameResultsSetPagination, self).paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        """
        Add custom data to the Response in addition to what already in the Serializer class.
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


@api_view(['POST'])
def submit_celery_task(request):
    if request.method == 'POST':
        count = int(request.data['count'])
        execution_time = datetime.datetime.fromisoformat(request.data['execution_time']).astimezone(tz=pytz.utc).replace(tzinfo=None)
        task = company_name_bulk_create.apply_async(
            args=[count],
            eta=execution_time
        )
    return JsonResponse({"task_id": task.id}, status=202)


@api_view(['GET'])
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)
