from django.shortcuts import render

def presence(request):
    return render(request, "app_presence/presence.html")
