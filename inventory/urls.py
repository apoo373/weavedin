from django.conf.urls import url
from inventory import views

urlpatterns = [
    url(r'^login/?$',           views.login,    name='login'),
    url(r'^logout/?$',           views.logout,    name='logout'),
]
