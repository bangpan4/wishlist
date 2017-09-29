from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^wishlist/logout$', views.logout),
    url(r'^wishlist/add$', views.additem),
    url(r'^createitem', views.createitem),
    url(r'^wishlist/item/(?P<item_id>\d+)$', views.item),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
    url(r'^addlist/(?P<item_id>\d+)$', views.addlist)
]