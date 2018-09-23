# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

# Create your views here.

# Login view
def login(request):
    return HttpResponse("You've Reached Login Page")

# Logout view
def logout(request):
    return HttpResponse("You've Reached Logout Page")
