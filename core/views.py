from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ParagraphForm
from .analysis import trascender_summary, union_bigram, union_trigram, sentiment

# Create your views here.
def home(request):
    return render(request,'core/home.html')

def slicing(request):
    return render(request,'core/slicing.html')

def results(request):
    text=""
    if request.method=="GET":
        for element in request.GET:
            text += element   
    summary,lw,cb,ct,s = trascender_summary(text)
    title2,cb = union_bigram(cb)
    title3,ct = union_trigram(ct)
    s = sentiment(s)
    return render(request,'core/results.html',{'summary':summary,'lw':lw,'cb':cb,'ct':ct,'s':s,'title2':title2,'title3':title3})

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