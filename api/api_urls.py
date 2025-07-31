from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeetingViewSet, MeetingMinutesViewSet, TaskViewSet, UserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'meetings', MeetingViewSet)
router.register(r'minutes', MeetingMinutesViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
