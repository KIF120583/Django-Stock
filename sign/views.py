from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request , "index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        if username == "admin" and password == "password":
            return HttpResponse("login success!")
        else:
            return render(request, "index.html" , {'error':'username or password error !'})