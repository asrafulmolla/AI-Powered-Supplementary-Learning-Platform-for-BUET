from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('INSTRUCTOR', 'Instructor'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'style': 'width: 100%; padding: 0.8rem 1rem; border-radius: 10px; border: 2px solid #f1f5f9; background: #f8fafc; font-size: 0.95rem; margin-bottom: 1rem;'
    }))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.role = self.cleaned_data['role']
        if user.role == 'INSTRUCTOR':
            user.is_staff = True # Optional: give instructor staff status for admin access if needed
        user.save()
        return user

from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'search-input', 'style': 'width:100%; margin-bottom:1rem;'}),
            'last_name': forms.TextInput(attrs={'class': 'search-input', 'style': 'width:100%; margin-bottom:1rem;'}),
            'email': forms.EmailInput(attrs={'class': 'search-input', 'style': 'width:100%; margin-bottom:1rem;'}),
            'bio': forms.Textarea(attrs={'class': 'search-input', 'style': 'width:100%; margin-bottom:1rem;', 'rows': 3}),
            'department': forms.TextInput(attrs={'class': 'search-input', 'style': 'width:100%; margin-bottom:1rem;'}),
        }
