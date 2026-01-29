from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TopicViewSet, CourseMaterialViewSet, ChatView,
    GenerateMaterialView, DigitizeNoteView, VideoGeneratorView,
    QuizGeneratorView, FlashcardGeneratorAPI
)

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'materials', CourseMaterialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', ChatView.as_view(), name='api_chat'),
    path('generate/', GenerateMaterialView.as_view(), name='api_generate_material'),
    path('digitize/', DigitizeNoteView.as_view(), name='api_digitize'),
    path('video-script/', VideoGeneratorView.as_view(), name='api_video_script'),
    path('quiz/generate/', QuizGeneratorView.as_view(), name='api_quiz_generate'),
    path('flashcards/generate/', FlashcardGeneratorAPI.as_view(), name='api_flashcards_generate'),
]
