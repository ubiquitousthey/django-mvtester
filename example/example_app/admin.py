from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from example.example_app.models import Registration

admin.site.register(Registration,ModelAdmin)
