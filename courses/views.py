from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import CourseMaterial, Topic
from .serializers import CourseMaterialSerializer, TopicSerializer
from .rag_service import RAGService
from .video_service import VideoService

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class CourseMaterialViewSet(viewsets.ModelViewSet):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags', 'topic__name', 'text_content']

class ChatView(APIView):
    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({"error": "Query required"}, status=400)
        
        rag = RAGService()
        response = rag.generate_answer(query)
        return Response(response)

class GenerateMaterialView(APIView):
    def post(self, request):
        topic = request.data.get('topic')
        material_type = request.data.get('type', 'NOTE')
        
        rag = RAGService()
        result = rag.generate_learning_material(topic, material_type)
        return Response(result)

class IndexView(TemplateView):
    template_name = "courses/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_materials'] = CourseMaterial.objects.all().order_by('-created_at')[:6]
        return context

class ChatUIView(TemplateView):
    template_name = "courses/chat.html"

class GeneratorUIView(TemplateView):
    template_name = "courses/generator.html"

class VideoGeneratorUIView(TemplateView):
    template_name = "courses/video_generator.html"

class DigitizerUIView(TemplateView):
    template_name = "courses/digitizer.html"

from .digitization import DigitizationService
from rest_framework.parsers import MultiPartParser, FormParser

class DigitizeNoteView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)
        
        service = DigitizationService()
        result = service.digitize(file_obj)
        return Response({"content": result})

class VideoGeneratorView(APIView):
    def post(self, request):
        topic = request.data.get('topic')
        if not topic:
            return Response({"error": "Topic required"}, status=400)
        
        service = VideoService()
        result = service.generate_video_script(topic)
        return Response(result)
