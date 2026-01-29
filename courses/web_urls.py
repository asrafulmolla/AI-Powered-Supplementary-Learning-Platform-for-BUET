from django.urls import path
from .views import (
    IndexView, ChatUIView, GeneratorUIView, DigitizerUIView, 
    VideoGeneratorUIView, QuizUIView, LibraryView, MaterialDetailUIView, 
    FlashcardView, KnowledgeGraphView, MaterialManagementListView,
    MaterialCreateView, MaterialUpdateView, MaterialDeleteView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat-ui/', ChatUIView.as_view(), name='chat_ui'),
    path('generator-ui/', GeneratorUIView.as_view(), name='generator_ui'),
    path('digitizer-ui/', DigitizerUIView.as_view(), name='digitizer_ui'),
    path('video-generator-ui/', VideoGeneratorUIView.as_view(), name='video_generator_ui'),
    path('quiz-ui/', QuizUIView.as_view(), name='quiz_ui'),
    path('library/<str:category>/', LibraryView.as_view(), name='library'),
    path('material-detail/<int:pk>/', MaterialDetailUIView.as_view(), name='material_detail'),
    path('flashcards/', FlashcardView.as_view(), name='flashcards'),
    path('graph/', KnowledgeGraphView.as_view(), name='graph'),
    
    # Material Management (CMS)
    path('manage/materials/', MaterialManagementListView.as_view(), name='manage-materials'),
    path('manage/materials/add/', MaterialCreateView.as_view(), name='material-add'),
    path('manage/materials/<int:pk>/edit/', MaterialUpdateView.as_view(), name='material-edit'),
    path('manage/materials/<int:pk>/delete/', MaterialDeleteView.as_view(), name='material-delete'),
]
