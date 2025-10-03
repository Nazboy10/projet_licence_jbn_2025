from django.shortcuts import render

def bulletin(request):
    return render(request, "app_bulletin/bulletin.html")
