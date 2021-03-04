from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('login', views.login),
    path('add_quote', views.addQuote),
    path('quote/<int:id>/delete', views.delete),
    path('quote/<int:id>', views.posterQuotes),
    path('quote/<int:id>/liked_quote', views.likeQuote),
    path('quote/<int:id>/updatePage', views.updatePage),
    path('quote/<int:id>/update', views.editMyAccount)
]
