import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def fix():
    # 1. Ensure the default Site exists
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={'domain': '127.0.0.1:8000', 'name': 'BUET Learning Platform'}
    )
    if not created:
        site.domain = '127.0.0.1:8000'
        site.name = 'BUET Learning Platform'
        site.save()

    # 2. Ensure Google SocialApp exists (Dummy data)
    # Note: For actual Google login to work, the user needs to provide a real Client ID and Secret in Admin
    app, created = SocialApp.objects.get_or_create(
        provider='google',
        name='Google Auth',
        defaults={
            'client_id': 'YOUR_GOOGLE_CLIENT_ID_HERE',
            'secret': 'YOUR_GOOGLE_SECRET_HERE',
        }
    )
    app.sites.add(site)

    print("Authentication system fixed. Site and SocialApp records created.")

if __name__ == "__main__":
    fix()
