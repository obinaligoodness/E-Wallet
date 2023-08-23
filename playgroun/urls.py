from django.urls import path

from playgroun import views

urlpatterns = [
    path("play",views.playground)
]