# Create your views here.
from django.http import HttpResponse

def home(req):
    return HttpResponse('homepage')

def login(req):
    return HttpResponse('login')
