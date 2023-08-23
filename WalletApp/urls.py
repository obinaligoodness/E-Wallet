from rest_framework.routers import DefaultRouter

from WalletApp import views

router = DefaultRouter()
router.register('transactions', views.TransactionViewSet, basename='transactions')
urlpatterns = router.urls
