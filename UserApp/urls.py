from rest_framework import routers

from UserApp import views

router = routers.DefaultRouter()
router.register("users/", views.UserViewSet())
