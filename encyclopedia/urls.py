from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("new", views.new, name='new'),
    path("random", views.random_page, name='random'),
    path("search", views.search, name='search'),
    path("<str:title>/edit", views.edit, name='edit'),
    path("<str:title>", views.page, name='page')   
]
