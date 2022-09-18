from django.contrib import admin
from app.models import CompanyName


@admin.register(CompanyName)
class CompanyNameAdmin(admin.ModelAdmin):
    pass
