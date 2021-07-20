from django.shortcuts import render
from django.views.generic import DetailView
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.s


class ProfileDetail(DetailView):
    model = Profile
    template_name = "registration/profile.html"
    slug_field = 'url'


@login_required
def view_foo(request):
    user_profile = request.user.get_profile()
    url = user_profile.url
