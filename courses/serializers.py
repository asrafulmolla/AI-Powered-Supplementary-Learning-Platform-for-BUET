from rest_framework import serializers
from .models import CourseMaterial, Topic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class CourseMaterialSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    
    class Meta:
        model = CourseMaterial
        fields = '__all__'
