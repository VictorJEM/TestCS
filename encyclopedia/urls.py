from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new-page", views.new_page, name="new_page"),
    path("random-page", views.random_page, name="random_page"),
    path("process-edit-page", views.process_edit_page, name="process_edit_page"),
    path("<str:title>", views.entry_page, name="entry_page"),
    path("edit-page/<str:title>", views.edit_page, name="edit_page"),
]