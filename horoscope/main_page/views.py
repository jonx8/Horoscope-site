from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import *

# Create your views here.


def IndexView(request):
    return render(request, 'main_page/index.html')


class UserProfileDetail(DetailView):
    model = UserProfile
    template_name = "registration/profile.html"
    slug_field = 'url'