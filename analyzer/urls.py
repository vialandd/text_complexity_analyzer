from django.urls import path
from . import views

urlpatterns = [
    path("", views.document_list, name="document_list"),
    path("document/<int:pk>/", views.document_detail, name="document_detail"),
    path("document/new/", views.document_create, name="document_create"),
]
