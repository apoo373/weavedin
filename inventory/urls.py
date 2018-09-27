from django.conf.urls import url
from inventory import views

urlpatterns = [
    url(r'^login/?$',           views.login,    name='login'),
    url(r'^logout/?$',           views.logout,    name='logout'),
    # Retrieving Objects
    url(r'^allItems/?$',           views.allItems,    name='allItems'),
    url(r'^item/(?P<item_id>[0-9]+)$', views.item_details, name='item-details'),
    url(r'^item/(?P<item_id>[0-9]+)/(?P<variant_id>[0-9]+)$', views.variant_details, name='variant-details'),
    # Variant Operations
    url(r'^deleteVariant/(?P<variant_id>[0-9]+)$', views.delete_variant, name='delete-variant'),
    url(r'^editVariant/(?P<variant_id>[0-9]+)$', views.edit_variant, name='edit-variant'),
    url(r'^addVariant/(?P<item_id>[0-9]+)$', views.add_variant, name='add-variant'),
    # Property Related Operations
    url(r'^deleteProperty/(?P<property_id>[0-9]+)$', views.delete_property, name='delete-property'),
    url(r'^editProperty/(?P<property_id>[0-9]+)$', views.edit_property, name='edit-property'),
    url(r'^addProperty/(?P<item_id>[0-9]+)/(?P<variant_id>[0-9]+)$', views.add_property, name='add-property'),
    url(r'^report/?$', views.generate_report, name='generate-report'),
]
