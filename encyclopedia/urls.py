from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("new", views.new, name='new'),
    path("random", views.page, name='random'),
    path("<str:title>/edit", views.edit, name='edit'),
    path("<str:title>", views.page, name='page')   
]
