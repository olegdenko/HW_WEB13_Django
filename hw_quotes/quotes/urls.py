from django.urls import path

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name="root"),
    path('author/<str:author_id>/', views.author_detail, name='author_detail'),
    path("quotes/", views.main, name="quotes"),
    path("quotes/edit/<int:quote_id>/", views.edit_quote, name="edit_quote"),
    path("quotes/remove/<int:quote_id>", views.delete_quote, name="remove"),
    path('<int:page>', views.main, name="root_paginate"),
    path("login/", views.login, name="SignIn"),
    path('tag/<str:tag>/', views.tag_quotes, name='tag_quotes'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
]
