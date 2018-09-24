# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from models import InventoryLog, Item, Variant, Property

# Create your views here.

# Login view
def login(request):
    return HttpResponse("You've Reached Login Page")

# Logout view
def logout(request):
    return HttpResponse("You've Reached Logout Page")


# Get all Items
def allItems(request):
    allItems = Item.objects.all()
    return render(request, 'inventory/allItems.html', {'allItems': allItems})

def AggregateFeed(userFeed):
    timeAgg = {}
    for eachEntry in userFeed:
        concernedTime = eachEntry.time.replace(second=0, microsecond=0)
        if concernedTime in timeAgg:
            timeAgg[concernedTime].append(eachEntry.content)
        else:
            timeAgg[concernedTime] = [eachEntry.content]
    return timeAgg

# Generate Report
def generate_report(request):
    Response = {}
    if 'user_id' not in request.GET:
        userActivity = InventoryLog.objects.filter(user=request.user.id)
        Response[request.user.id] = AggregateFeed(userActivity)
    else:
        userIds = request.GET['user_id'].split(",")
        for user in userIds:
            userActivity = InventoryLog.objects.filter(user=user)
            Response[user] = AggregateFeed(userActivity)

    return render(request, 'inventory/report.html', {'allusers': Response})
