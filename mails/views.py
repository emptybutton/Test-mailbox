from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET

from django.shortcuts import render


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "mails/index.html")
