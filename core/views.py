from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ParagraphForm, SliceForm
from .analysis import trascender_summary, union_bigram, union_trigram, sentiment
from .sliceParagraph import raw2parr

# Create your views here.
def home(request):
    return render(request,'core/home.html')

def slicing(request):
    if request.method=="POST":
        paragraph_form = SliceForm(data=request.POST)
        if paragraph_form.is_valid():
            text=request.POST.get('text','')
            number=request.POST.get('number','')
        return redirect(reverse('resultsSlicing')+'?'+number+text)
    else:
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

def resultsSlicing(request):
    text=""
    if request.method=="GET":
        for element in request.GET:
            text += element
        number=int(text[0])
        text=text[1:]
        text=raw2parr(text,number)
        summary_list=[]
        title2_list=[]
        title3_list=[]
        s_list=[]
        cb_list=[]
        ct_list=[]
        for p in text:
            summary,lw,cb,ct,s = trascender_summary(p)
            title2,cb = union_bigram(cb)
            title3,ct = union_trigram(ct)
            s = sentiment(s)
            summary_list.append(summary)
            title2_list.append(title2)
            title3_list.append(title3)
            s_list.append(s)
            cb_list.append(cb)
            ct_list.append(ct)
            output = zip(text, summary_list,title2_list,title3_list,cb_list,ct_list,s_list)
    # return render(request,'core/resultsSlicing.html',{'text':text,'summary':summary_list,'cb':cb_list,'ct':ct_list,'s':s_list,'title2':title2_list,'title3':title3_list})
    return render(request,'core/resultsSlicing.html',{'output':output})

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