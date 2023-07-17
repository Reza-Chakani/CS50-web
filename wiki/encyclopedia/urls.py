from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("save", views.save, name="save"),
    path("edit", views.edit, name="edit"),
    path("saveedit", views.saveedit, name="saveedit"),
    path("rand", views.rand, name="rand"),
]
