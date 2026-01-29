from django import forms
from .models import CourseMaterial, Topic

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'description', 'category', 'file_type', 'file', 'text_content', 'topic', 'week', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'search-input', 'style': 'width: 100%; border: 1px solid var(--border-color); background: #f8fafc; margin-bottom: 1rem;'}),
            'description': forms.Textarea(attrs={'class': 'search-input', 'rows': 3, 'style': 'width: 100%; border: 1px solid var(--border-color); background: #f8fafc; margin-bottom: 1rem;'}),
            'category': forms.Select(attrs={'class': 'search-input', 'style': 'width: 100%; border: 1px solid var(--border-color); background: #f8fafc; margin-bottom: 1rem;'}),
            'file_type': forms.Select(attrs={'class': 'search-input', 'style': 'width: 100%; border: 1px solid var(--border-color); background: #f8fafc; margin-bottom: 1rem;'}),
            'file': forms.FileInput(attrs={'style': 'margin-bottom: 1rem;'}),
            'text_content': forms.Textarea(attrs={'class': 'search-input', 'rows': 5, 'style': 'width: 100%; border: 1px solid var(--border-color); background: #f8fafc; margin-bottom: 1rem;'}),
            'topic': forms.Select(attrs={'class': 'search-input', 'style': 'width: 100%; border: 1px solid var(--border-color); background: #f8fafc; margin-bottom: 1rem;'}),
            'week': forms.NumberInput(attrs={'class': 'search-input', 'style': 'width: 100%; border: 1px solid var(--border-color); background: #f8fafc; margin-bottom: 1rem;'}),
            'tags': forms.TextInput(attrs={'class': 'search-input', 'placeholder': 'e.g. algorithms, assignment', 'style': 'width: 100%; border: 1px solid var(--border-color); background: #f8fafc; margin-bottom: 1rem;'}),
        }
