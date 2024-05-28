from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from chat.views import MessageModelViewSet

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')

urlpatterns = [
    path(r'chat/', include(router.urls)),
]
