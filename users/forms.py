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
