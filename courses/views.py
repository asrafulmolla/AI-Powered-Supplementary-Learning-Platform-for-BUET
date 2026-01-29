from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CourseMaterial, Topic
from .forms import CourseMaterialForm
from .serializers import CourseMaterialSerializer, TopicSerializer
from .rag_service import RAGService
from .video_service import VideoService
from rest_framework import viewsets, filters, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role in ['INSTRUCTOR', 'TA'] or request.user.is_superuser)

class InstructorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.role in ['INSTRUCTOR', 'TA'] or self.request.user.is_superuser)

class StudentRequiredMixin(LoginRequiredMixin):
    pass

class MaterialManagementListView(InstructorRequiredMixin, ListView):
    model = CourseMaterial
    template_name = "courses/manage_materials_list.html"
    context_object_name = "materials"
    paginate_by = 10

class MaterialCreateView(InstructorRequiredMixin, CreateView):
    model = CourseMaterial
    form_class = CourseMaterialForm
    template_name = "courses/manage_material_form.html"
    success_url = reverse_lazy('manage-materials')

class MaterialUpdateView(InstructorRequiredMixin, UpdateView):
    model = CourseMaterial
    form_class = CourseMaterialForm
    template_name = "courses/manage_material_form.html"
    success_url = reverse_lazy('manage-materials')

class MaterialDeleteView(InstructorRequiredMixin, DeleteView):
    model = CourseMaterial
    template_name = "courses/manage_material_confirm_delete.html"
    success_url = reverse_lazy('manage-materials')

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class CourseMaterialViewSet(viewsets.ModelViewSet):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags', 'topic__name', 'text_content']

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        query = request.data.get('query')
        bangla_mode = request.data.get('bangla_mode', False)
        
        if not query:
            return Response({"error": "Query required"}, status=400)
        
        rag = RAGService()
        
        if bangla_mode:
            # Multi-mode: Explain in Bangla
            answer = rag.provide_bangla_explanation(query)
            return Response({"answer": answer})
        else:
            response = rag.generate_answer(query)
            return Response(response)

class GenerateMaterialView(APIView):
    permission_classes = [IsInstructor]
    def post(self, request):
        topic = request.data.get('topic')
        material_type = request.data.get('type', 'NOTE')
        
        rag = RAGService()
        result = rag.generate_learning_material(topic, material_type)
        return Response(result)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "courses/index.html"
    
    def get_context_data(self, **kwargs):
        from community.models import Post
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'topics': Topic.objects.count(),
            'materials': CourseMaterial.objects.count(),
            'posts': Post.objects.count(),
            'ai_usage': 128 # Mocked cumulative AI interactions
        }
        context['recent_materials'] = CourseMaterial.objects.all().order_by('-id')[:6]
        return context

class ChatUIView(StudentRequiredMixin, TemplateView):
    template_name = "courses/chat.html"

class GeneratorUIView(InstructorRequiredMixin, TemplateView):
    template_name = "courses/generator.html"

class VideoGeneratorUIView(StudentRequiredMixin, TemplateView):
    template_name = "courses/video_generator.html"

class QuizUIView(StudentRequiredMixin, TemplateView):
    template_name = "courses/quiz.html"

class LibraryView(LoginRequiredMixin, TemplateView):
    template_name = "courses/library.html"

    def get_context_data(self, **kwargs):
        category = self.kwargs.get('category', 'theory')
        context = super().get_context_data(**kwargs)
        
        if category == 'lab':
            # Lab category filters for CODE files
            materials = CourseMaterial.objects.filter(file_type='CODE')
            context['title'] = "Lab Repository (Code)"
        else:
            # Theory category filters for anything NOT CODE
            materials = CourseMaterial.objects.exclude(file_type='CODE')
            context['title'] = "Theory & Lecture Notes"
            
        context['materials'] = materials
        context['category'] = category
        return context

class MaterialDetailUIView(TemplateView):
    template_name = "courses/material_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material_id = self.kwargs.get('pk')
        material = CourseMaterial.objects.get(pk=material_id)
        context['material'] = material
        # Fetch up to 3 related materials in the same topic, excluding the current one
        context['related_materials'] = CourseMaterial.objects.filter(
            topic=material.topic
        ).exclude(pk=material_id)[:3]
        return context

class KnowledgeGraphView(StudentRequiredMixin, TemplateView):
    template_name = "courses/graph.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topics = Topic.objects.all()
        nodes = []
        links = []
        for t in topics:
            nodes.append({"id": t.id, "label": t.name, "type": "topic"})
            materials = t.materials.all()
            for m in materials:
                nodes.append({"id": f"m{m.id}", "label": m.title, "type": "material"})
                links.append({"source": t.id, "target": f"m{m.id}"})
        
        context['graph_data'] = {"nodes": nodes, "links": links}
        return context

class FlashcardView(StudentRequiredMixin, TemplateView):
    template_name = "courses/flashcards.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context

class FlashcardGeneratorAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        topic_id = request.data.get('topic_id')
        topic = Topic.objects.get(id=topic_id)
        rag = RAGService()
        cards = rag.generate_flashcards(topic.name)
        return Response({"cards": cards})

class DigitizerUIView(StudentRequiredMixin, TemplateView):
    template_name = "courses/digitizer.html"

from .digitization import DigitizationService
from rest_framework.parsers import MultiPartParser, FormParser

class DigitizeNoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)
        
        service = DigitizationService()
        result = service.digitize(file_obj)
        return Response({"content": result})

class VideoGeneratorView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        topic = request.data.get('topic')
        if not topic:
            return Response({"error": "Topic required"}, status=400)
        
        service = VideoService()
        result = service.generate_video_script(topic)
        return Response(result)

class QuizGeneratorView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        topic = request.data.get('topic')
        if not topic:
            return Response({"error": "Topic required"}, status=400)
        
        rag = RAGService()
        quiz = rag.generate_quiz(topic)
        return Response(quiz)
