from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet, FeedbackImageViewSet

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet)
router.register(r'images', FeedbackImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 