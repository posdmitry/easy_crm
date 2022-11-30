from django.shortcuts import render
from django.views import generic

from .models import Clients


class MainPageView(generic.ListView):
    model = Clients
    template_name = 'clients/index.html'
