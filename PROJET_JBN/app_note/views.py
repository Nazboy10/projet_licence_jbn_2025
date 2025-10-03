from django.shortcuts import render

def note(request):
    return render(request, "app_note/note.html")
