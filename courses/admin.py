from django.contrib import admin
from .models import CourseMaterial, Topic

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'file_type', 'week', 'topic', 'created_at')
    list_filter = ('category', 'file_type', 'week', 'topic')
    search_fields = ('title', 'description', 'tags')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
