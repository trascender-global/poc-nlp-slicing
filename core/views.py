from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'core/home.html')

def slicing(request):
    return render(request,'core/slicing.html')

def results(request):
    return render(request,'core/results.html')