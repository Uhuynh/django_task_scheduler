import datetime
import pytz

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.decorators import api_view

from app.tasks import company_name_bulk_create


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django Task Scheduler - Version ' + settings.VERSION
        return context


@api_view(['POST'])
def submit_celery_task(request):
    if request.method == 'POST':
        count = int(request.data['count'])
        execution_time = datetime.datetime.fromisoformat(request.data['execution_time']).astimezone(tz=pytz.utc).replace(tzinfo=None)
        if execution_time > datetime.datetime.utcnow():
            task = company_name_bulk_create.apply_async(
                args=[count],
                eta=execution_time
            )
            return JsonResponse({"task_id": task.id}, status=202)
        else:
            return JsonResponse({}, status=400)
