from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ParagraphForm

# Create your views here.
def home(request):
    return render(request,'core/home.html')

def slicing(request):
    return render(request,'core/slicing.html')

def results(request):
    return render(request,'core/results.html')

def base(request):
    return render(request,'core/base.html')

def info(request):
    return render(request,'core/info.html')

def team(request):
    return render(request,'core/team.html')

def textAnalyticsDetails(request):
    if request.method=="POST":
        paragraph_form = ParagraphForm(data=request.POST)
        if paragraph_form.is_valid():
            text=request.POST.get('text','')
        return redirect(reverse('results')+'?'+text)
    else:
        return render(request,'core/textAnalyticsDetails.html')