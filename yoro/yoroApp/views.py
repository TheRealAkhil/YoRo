from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from models import Note

def index(request):
    return render(request, 'index.html', {})

def createNote(request):

    username = request.POST['username']
    note = request.POST['note']

    newNote = Note(user=username, text_body=note, start_date=timezone.now())# TODO: START and EXPIRATION date objects
    newNote.save()

    # SHOULD REDIRECT TO LOGIN PAGE
    return redirect("index")