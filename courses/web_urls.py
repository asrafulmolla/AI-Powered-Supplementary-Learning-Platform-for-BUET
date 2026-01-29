from django.urls import path
from .views import IndexView, ChatUIView, GeneratorUIView, DigitizerUIView, VideoGeneratorUIView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat-ui/', ChatUIView.as_view(), name='chat_ui'),
    path('generator-ui/', GeneratorUIView.as_view(), name='generator_ui'),
    path('digitizer-ui/', DigitizerUIView.as_view(), name='digitizer_ui'),
    path('video-generator-ui/', VideoGeneratorUIView.as_view(), name='video_generator_ui'),
]
