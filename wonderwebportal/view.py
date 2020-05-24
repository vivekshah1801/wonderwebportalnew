from bs4 import BeautifulSoup
from django.shortcuts import render,redirect
from wonderwebportal.templates import *
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from submission.models import submissions
from http.client import HTTPResponse

default_tag_cost = 100

price_list = {
    'h1':800,
    'h2':800,
    'h3':800,
    'h4':400,
    'h5':400,
    'h6':400,
    'script':1000,
    'img':9000,
    'p':300,
    'div':1000,
    'span':500,
    'br':100,
    'a':80,
    'b':50,
    'i':50,
    'u':50,
    'strong':50,
    'big':50,
    'body':20,
    'button':20,
    'center':400,
    'table':800,
    'tr':100,
    'td':100,
    'th':200,
    'thead':50,
    'tbody':50,
    'form':6000,
    'style':40,
    'link':100,
    'textarea':100,
    'ul':40,
    'ol':40,
    'li':20,
}

@csrf_exempt
def getresult(request):
    htmltext = request.POST.get('code')
    soup = BeautifulSoup(htmltext)

    result = {}
 
    tag_used = set([tag.name for tag in soup.find_all(True)])
    
    if len(htmltext)<=0:
        result["status"] = 'invalid_nocode'
        result["msg"] = 'The code is empty'
        return JsonResponse(result)

    elif 'script' in tag_used:
        result["status"] = 'invalid_script'
        result["msg"] = 'Please remove script tags from your scripts'
        return JsonResponse(result)

    else:
        result["cost_table"] = []
        for tag in tag_used:
            tag_name = tag
            tag_times_used = len(soup.find_all(tag)) 

            if tag in price_list.keys():
                tag_cost = price_list[tag]
            else:
                tag_cost = default_tag_cost

            result["cost_table"].append([tag_name,tag_cost,tag_times_used])

        result["status"] = "success"
        result["msg"] = "Code Analysed Successfully"
        return JsonResponse(result)    
    

def home(request):
    return render(request,'analyse.html')    

def index(request):
    return render(request, 'index.html')

def submit(request):
    if request.method == "GET":
        print('render')
        return render(request,'submit.html')
    else:
        name= request.POST.get('name','')
        id  = request.POST.get('secretkey','')
        file = request.FILES['submission']
        try:
            temp = submissions.objects.get(id=id)
            return JsonResponse({'status':'already'})
        except:
            s = submissions(name=name,id=id,file=file)
            s.save()
            return JsonResponse({'status':'saved'})