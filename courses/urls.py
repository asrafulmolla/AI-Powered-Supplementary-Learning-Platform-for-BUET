from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseMaterialViewSet, TopicViewSet, ChatView, GenerateMaterialView, DigitizeNoteView, VideoGeneratorView

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'materials', CourseMaterialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', ChatView.as_view(), name='chat'),
    path('generate/', GenerateMaterialView.as_view(), name='generate'),
    path('digitize/', DigitizeNoteView.as_view(), name='digitize'),
    path('video-script/', VideoGeneratorView.as_view(), name='video_script'),
]
