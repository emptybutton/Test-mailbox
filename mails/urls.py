from django.urls import path

from mails.views import index 


app_name = "mails"

urlpatterns = [
    path('', index, name="index"),
]
