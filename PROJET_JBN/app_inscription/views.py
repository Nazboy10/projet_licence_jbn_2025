from django.shortcuts import render

def inscription(request):
    return render(request, "app_inscription/inscription.html")