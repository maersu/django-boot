#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template.response import TemplateResponse
from django.conf import settings
import os

def start(request):
    context = {}
    return TemplateResponse(request, 'start.html', context)

