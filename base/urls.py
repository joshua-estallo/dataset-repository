from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("anotherdataset/<int:pk>", views.anotherdataset, name="anotherdataset"),
  path("dataset/<str:pk>/", views.dataset, name="dataset"),
  path("upload/", views.upload, name="upload"),
  path("download/<str:pk>", views.download, name="download"),
]