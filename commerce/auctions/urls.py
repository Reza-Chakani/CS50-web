from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("category/<int:pk>", views.catlist, name="catlist"),
    path("newlist", views.newlist, name="newlist"),
    path("<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove", views.remove, name="remove"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("comment/<int:id>", views.comment, name="comment"),
]