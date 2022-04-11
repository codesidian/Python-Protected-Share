from django.contrib import admin
from .models import Page

# Register your models here.
admin.site.register(Page)


def get_changeform_initial_data(self, request):
    return {
        "template": """{% extends 'basic_template.html' %} 
            {% block 'body' %}
            /* HTML goes here */
            {% endblock %}"""
    }
