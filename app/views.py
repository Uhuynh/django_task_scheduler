import json

import pytz
from django.http import HttpResponseRedirect
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

from app.forms import CompanyNameForm
from app.models import CompanyName
from app.tasks import company_name_bulk_create


class IndexView(TemplateView):
    template_name = "app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django Task Scheduler - Version ' + settings.VERSION
        context['form'] = CompanyNameForm()
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


class CompanyNameList(View):
    template_name = "app/home.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': CompanyNameForm()
        })

    def post(self, request, *args, **kwargs):
        if 'task-submit' in request.POST:
            form = CompanyNameForm(request.POST)
            if form.is_valid():
                company_name_bulk_create.apply_async(
                    args=[form.cleaned_data['count']],
                    eta=form.cleaned_data['execution_time'].astimezone(tz=pytz.utc).replace(tzinfo=None)
                )
                messages.success(request, 'Task was submitted successfully.')
            else:
                messages.error(request, 'Task was not submitted succesfully')
        return HttpResponseRedirect('/')


@api_view(['POST'])
def submit_celery_task(request):
    if request.method == 'POST':
        form = CompanyNameForm(request.POST)
        if form.is_valid():
            company_name_bulk_create.apply_async(
                args=[form.cleaned_data['count']],
                eta=form.cleaned_data['execution_time']
            )
            # set an interval to execute task every 1 second (purpose is to use for one-off task)
            # schedule, created = IntervalSchedule.objects.get_or_create(
            #     every=1,
            #     period=IntervalSchedule.SECONDS,
            # )
            # PeriodicTask.objects.create(
            #     interval=schedule,
            #     name='Create company name',
            #     task='app.tasks.company_name_bulk_create',
            #     args=json.dumps([
            #         form.cleaned_data['byid'],
            #         form.cleaned_data['byid']
            #     ])
            # )



# @api_view(['POST'])
# def run_task(request):
#     if request.POST:
#         task_type = request.POST.get("type")
#         return JsonResponse({"task_type": task_type}, status=202)