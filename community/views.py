from rest_framework import viewsets
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .bot_service import BotService

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = serializer.save()
        
        # Trigger Bot (Bonus Task: Bot Support)
        # In a real app, this would be a celery task. Here we do it inline for simplicity.
        if "?" in post.title or "?" in post.content:
            reply_content = BotService.generate_reply(post.content)
            Comment.objects.create(
                post=post,
                author_name="EduBot",
                content=reply_content,
                is_bot=True
            )
            post.has_bot_reply = True
            post.save()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommunityUIView(TemplateView):
    template_name = "community/feed.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created_at')
        return context
