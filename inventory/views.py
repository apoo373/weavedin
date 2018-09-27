# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.forms.models import model_to_dict

from models import InventoryLog, Item, Variant, Property
from forms import *

# Create your views here.
def CreateLog(user, LogContent):
    newLog = InventoryLog(user=user, content=LogContent)
    newLog.save()
    return

# Check The Difference in Parameters
def CheckDiff(formData, originalData, param):
    result = []
    for each_param in param:
        if formData.cleaned_data[each_param] != originalData[each_param]:
            result.append(str(each_param))
    return str(result)


# Login view
def user_login(request):
    # Implement the next Forward Functionality
    if request.user.is_authenticated():
        return redirect("/inventory/allItems")
    redirection = request.GET.get('next', '')
    if redirection == "":
        redirection = "?next=/inventory/allItems"
    else:
        redirection = "?next=" + redirection
    return redirect("/admin/login/" + redirection)

# Logout view
def user_logout(request):
    logout(request)
    return HttpResponse("You've been Succesfully Logged Out !!")

# Get all Items
@login_required()
def allItems(request):
    allItems = Item.objects.all()
    newItem = ItemForm()
    return render(request, 'inventory/allItems.html', {'allItems': allItems, 'newItem': newItem})

# Get All Properties of an Item
@login_required()
def item_details(request, item_id):
    try:
        itemData = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("No Item Exist with this Id")
    allVariants = Variant.objects.filter(Item=itemData).all()
    newVariantForm = VariantForm()
    return render(request, 'inventory/itemVariants.html', {'item': itemData, 'variants': allVariants, 'variantForm': newVariantForm})

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
def delete_property(request, property_id):
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
def edit_property(request, property_id):
    try:
        property = Property.objects.get(pk=property_id)
    except Property.DoesNotExist:
        raise Http404("No Property With this Id")
    originalObject = model_to_dict(property)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PropertyForm(request.POST, instance=property)
        # check whether it's valid:
        if form.is_valid():
            diff = CheckDiff(form, originalObject, ["Name", "Value"])
            editPropery = form.save()

            # Adding to Logs
            LogContent = "Modified " + diff + " Property:(" + str(editPropery.id) + "-" + editPropery.Name + ") of the Variant:(" + str(editPropery.Variant.id) + "-" + editPropery.Variant.Name + ")"
            CreateLog(request.user, LogContent)
            return HttpResponseRedirect('/inventory/item/' + str(editPropery.Variant.Item.id) + "/" + str(editPropery.Variant.id))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PropertyForm(instance=property)
    return render(request, 'inventory/editProperty.html', {'form': form, 'property': property_id})

# Add Property to a Variant
@login_required
def add_property(request, item_id, variant_id):
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


# Delete Property
@login_required()
def delete_variant(request, variant_id):
    try:
        variantData = Variant.objects.get(pk=variant_id)
    except Variant.DoesNotExist:
        raise Http404("No Item Variant Found with this Id")
    redirectUrl = "/inventory/item/" + str(variantData.Item.id)
    LogContent = "Deleted Variant:(" + str(variantData.id) + "-" + variantData.Name + ") of the Item:(" + str(variantData.Item.id) + "-" + variantData.Item.Name + ")"
    variantData.delete()
    CreateLog(request.user, LogContent)
    return redirect(redirectUrl)

# Edit The Variant
@login_required
def edit_variant(request, variant_id):
    try:
        variantData = Variant.objects.get(pk=variant_id)
    except Variant.DoesNotExist:
        raise Http404("No Item Variant Found with this Id")
    originalObject = model_to_dict(variantData)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VariantForm(request.POST, instance=variantData)
        # check whether it's valid:
        if form.is_valid():
            diff = CheckDiff(form, originalObject, ["Name", "CostPrice", "SellingPrice", "Quantity"])
            editPropery = form.save()

            # Adding to Logs
            LogContent = "Modified " + diff + " of Variant:(" + str(variantData.id) + "-" + variantData.Name + ") of the Item:(" + str(variantData.Item.id) + "-" + variantData.Item.Name + ")"
            CreateLog(request.user, LogContent)
            return HttpResponseRedirect('/inventory/item/' + str(variantData.Item.id))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = VariantForm(instance=variantData)
    return render(request, 'inventory/editVariant.html', {'form': form, 'variant': variant_id})

# Add Variant to an Item
@login_required
def add_variant(request, item_id):
    if request.method == 'POST':
        try:
            itemData = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise Http404("No Item Exist with this Id")
        # create a form instance and populate it with data from the request:
        form = VariantForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            newVariant = form.save(commit=False)
            newVariant.Item = itemData
            newVariant.save()

            # Adding to Logs
            LogContent = "Added Variant:(" + str(newVariant.id) + "-" + newVariant.Name + ") of the Item:(" + str(itemData.id) + "-" + itemData.Name + ")"
            CreateLog(request.user, LogContent)
            return HttpResponseRedirect('/inventory/item/' + str(item_id))
    # if a GET (or any other method) we'll create a blank form
    else:
        raise Http404("Get Call Not Supported for This URL")

# Delete Item
@login_required()
def delete_item(request, item_id):
    try:
        itemData = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("No Item Exist with this Id")
    redirectUrl = "/inventory/allItems"
    LogContent = "Deleted Item:(" + str(itemData.id) + "-" + itemData.Name + ")"
    itemData.delete()
    CreateLog(request.user, LogContent)
    return redirect(redirectUrl)

# Edit the Item
@login_required
def edit_item(request, item_id):
    try:
        itemData = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("No Item Exist with this Id")
    originalObject = model_to_dict(itemData)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ItemForm(request.POST, instance=itemData)
        # check whether it's valid:
        if form.is_valid():
            diff = CheckDiff(form, originalObject, ['Name', 'Brand', 'Category', 'ProductCode'])
            editItem = form.save()

            # Adding to Logs
            LogContent = "Modified " + diff + " of Item:(" + str(editItem.id) + "-" + editItem.Name + ")"
            CreateLog(request.user, LogContent)
            return HttpResponseRedirect('/inventory/item/' + str(editItem.id))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ItemForm(instance=itemData)
    return render(request, 'inventory/editItem.html', {'form': form, 'item': item_id})

# Add Item
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            newItem = form.save()

            # Adding to Logs
            LogContent = "Added Item:(" + str(newItem.id) + "-" + newItem.Name + ")"
            CreateLog(request.user, LogContent)
            return HttpResponseRedirect('/inventory/allItems')
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
