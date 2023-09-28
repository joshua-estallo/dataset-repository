from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("anotherhome", views.anotherhome, name="anotherhome"),
  path("dataset/<str:pk>/", views.dataset, name="dataset"),
  path("upload/", views.upload, name="upload"),
  path("download/<str:pk>", views.download, name="download"),
]