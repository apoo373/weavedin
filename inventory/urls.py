from django.conf.urls import url
from inventory import views

urlpatterns = [
    url(r'^login/?$',           views.login,    name='login'),
    url(r'^logout/?$',           views.logout,    name='logout'),
    url(r'^allItems/?$',           views.allItems,    name='allItems'),
    url(r'^item/(?P<item_id>[0-9]+)$', views.item_details, name='item-details'),
    url(r'^item/(?P<item_id>[0-9]+)/(?P<variant_id>[0-9]+)$', views.variant_details, name='variant-details'),
    url(r'^deleteProperty/(?P<property_id>[0-9]+)$', views.deleteProperty, name='delete-property'),
    url(r'^editProperty/(?P<property_id>[0-9]+)$', views.editProperty, name='edit-property'),
    url(r'^addProperty/(?P<item_id>[0-9]+)/(?P<variant_id>[0-9]+)$', views.addProperty, name='add-property'),
    url(r'^report/?$', views.generate_report, name='generate-report'),
]
