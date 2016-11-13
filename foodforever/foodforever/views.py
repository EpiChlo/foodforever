from django.shortcuts import render

def index(request):
    template_name = 'foodforever/index.html'
    return render(request, template_name)
