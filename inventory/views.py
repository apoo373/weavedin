# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import InventoryLog, Item, Variant, Property
from forms import *

# Create your views here.
def CreateLog(user, LogContent):
    newLog = InventoryLog(user=user, content=LogContent)
    newLog.save()
    return

# Login view
def login(request):
    # Implement the next Forward Functionality
    return HttpResponse("You've Reached Login Page")

# Logout view
def logout(request):
    return HttpResponse("You've Reached Logout Page")

# Get all Items
@login_required()
def allItems(request):
    allItems = Item.objects.all()
    return render(request, 'inventory/allItems.html', {'allItems': allItems})

# Get All Properties of an Item
@login_required()
def item_details(request, item_id):
    try:
        itemData = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("No Item Exist with this Id")
    allVariants = Variant.objects.filter(Item=itemData).all()
    return render(request, 'inventory/itemVariants.html', {'item': itemData, 'variants': allVariants})

# Get All Properties of the Variants
@login_required()
def variant_details(request, item_id, variant_id):
    try:
        itemData = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("No Item Exist with this Id")
    try:
        variantData = Variant.objects.get(Item=itemData, pk=variant_id)
    except Variant.DoesNotExist:
        raise Http404("Incorrect Item-Variant Id combination")
    allProperties = Property.objects.filter(Variant=variantData).all()
    addPropertyForm = PropertyForm()
    return render(request, 'inventory/variantProperties.html', {'item': itemData, 'variantData': variantData, 'allProperties': allProperties, 'addProperty': addPropertyForm})

# Delete Property
@login_required()
def deleteProperty(request, property_id):
    try:
        property = Property.objects.get(pk=property_id)
    except Property.DoesNotExist:
        raise Http404("No Property With this Id")
    redirectUrl = str(property.Variant.Item.id) + "/" + str(property.Variant.id)
    LogContent = "Deleted Property:(" + str(property.id) + property.Name + ") of the Variant:(" + str(property.Variant.id) + "-" + property.Variant.Name + ")"
    property.delete()
    CreateLog(request.user, LogContent)
    return redirect("/inventory/item/" + redirectUrl)

# Edit The Given Property
@login_required
def editProperty(request, property_id):
    try:
        property = Property.objects.get(pk=property_id)
    except Property.DoesNotExist:
        raise Http404("No Property With this Id")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PropertyForm(request.POST, instance=property)
        # check whether it's valid:
        if form.is_valid():
            editPropery = form.save()

            # Adding to Logs
            LogContent = "Modified Property:(" + str(editPropery.id) + "-" + editPropery.Name + ") of the Variant:(" + str(editPropery.Variant.id) + "-" + editPropery.Variant.Name + ")"
            CreateLog(request.user, LogContent)
            return HttpResponseRedirect('/inventory/item/' + str(editPropery.Variant.Item.id) + "/" + str(editPropery.Variant.id))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PropertyForm(instance=property)
    return render(request, 'inventory/editProperty.html', {'form': form, 'property': property_id})

# Add Property to a Variant
@login_required
def addProperty(request, item_id, variant_id):
    if request.method == 'POST':
        try:
            itemData = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise Http404("No Item Exist with this Id")
        try:
            variantData = Variant.objects.get(Item=itemData, pk=variant_id)
        except Variant.DoesNotExist:
            raise Http404("Incorrect Item-Variant Id combination")
        # create a form instance and populate it with data from the request:
        form = PropertyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            newProperty = form.save(commit=False)
            newProperty.Variant = variantData
            newProperty.save()

            # Adding to Logs
            LogContent = "Added Property:(" + str(newProperty.id) + "-" + newProperty.Name + ") of the Variant:(" + str(newProperty.Variant.id) + "-" + newProperty.Variant.Name + ")"
            CreateLog(request.user, LogContent)
            return HttpResponseRedirect('/inventory/item/' + str(item_id) + "/" + str(variant_id))
    # if a GET (or any other method) we'll create a blank form
    else:
        raise Http404("Get Call Not Supported for This URL")


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
