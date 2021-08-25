from django.shortcuts import redirect, render

# Create your views here.


def index(request):
    context = {}
    return render(request, 'cat/index.html', context)
