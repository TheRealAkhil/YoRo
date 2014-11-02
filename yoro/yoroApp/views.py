from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils import timezone
from models import Note
import get_yo_main as helpers
import main


def index(request):
    return render(request, 'index.html', {})

def yo(request):
	print "in yo"
	username = request.GET.get('username')
	
	location = request.GET.get('location')
	latitude = location.split(';')[0]
	longitude = location.split(';')[1]

	reminder_text = None

	for n in Note.objects.all():
		if (not n.flagRead) and username.lower() == n.user.lower():
			reminder_text = n.text_body
			n.flagRead = True
			print "what"
			n.save()
			break

	print reminder_text

	yo_url = helpers.get_yo_main(latitude, longitude, reminder_text)
	print yo_url

	return render_to_response(api_address, data={'api_token': api_token, 'username': username, 'link': 'http://www.espn.com'})

def createNote(request):

    username = request.POST['username']
    note = request.POST['note']

    date_time = helpers.get_datetime(note)

    newNote = Note(user=username, text_body=note, time=date_time)# TODO: START and EXPIRATION date objects
    newNote.save()

    # SHOULD REDIRECT TO LOGIN PAGE
    return redirect("index")