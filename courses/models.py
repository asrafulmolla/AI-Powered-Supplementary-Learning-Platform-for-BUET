from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CourseMaterial(models.Model):
    CATEGORY_CHOICES = [
        ('THEORY', 'Theory'),
        ('LAB', 'Lab'),
    ]

    FILE_TYPE_CHOICES = [
        ('SLIDE', 'Lecture Slide'),
        ('PDF', 'PDF Document'),
        ('CODE', 'Code File'),
        ('NOTE', 'Note/Reference'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='THEORY')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='OTHER')
    
    file = models.FileField(upload_to='course_materials/', blank=True, null=True)
    text_content = models.TextField(blank=True, help_text="For notes or code snippets if no file is uploaded")
    
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    week = models.PositiveIntegerField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
