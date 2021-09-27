from django.shortcuts import render

# Create your views here.

def landing(request):
    return render(request, 'single_pages/landing.html') #templates 에 html, 연결할 템플릿

def about_me(request):
    return render(request, 'single_pages/about_me.html')
