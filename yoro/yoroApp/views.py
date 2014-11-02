from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from models import Note
import get_yo_main as helpers

def index(request):
    return render(request, 'index.html', {})

def createNote(request):

    username = request.POST['username']
    note = request.POST['note']

    date_time = helpers.get_datetime(note)

    newNote = Note(user=username, text_body=note, time=date_time)# TODO: START and EXPIRATION date objects
    newNote.save()

    # SHOULD REDIRECT TO LOGIN PAGE
    return redirect("index")