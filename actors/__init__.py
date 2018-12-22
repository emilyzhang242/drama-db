from DramaWebsite import settings

from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.template.response import TemplateResponse

from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponseRedirect,
    Http404
)

import requests