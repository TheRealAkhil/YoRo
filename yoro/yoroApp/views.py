from django.shortcuts import render, redirect, render_to_response
from models import Note
import get_yo_main as helpers
from API_KEY import api_token, api_address
import main
import requests

def index(request):
	return render(request, 'index.html', {})

def yo(request):
	username = request.GET.get('username')
	location = request.GET.get('location')
	latitude = location.split(';')[0]
	longitude = location.split(';')[1]

	reminder_text = None

	for n in Note.objects.all():
		if (not n.flagRead) and username.lower() == n.user.lower():
			reminder_text = n.text_body
			yo_url = 'http://www.espn.com'
			# yo_url = helpers.get_yo_main(latitude, longitude, reminder_text)
			data={'api_token': api_token, 'username': username, 'link': yo_url}
			n.flagRead = True
			n.save()
			requests.post(api_address, data)
			break

	return redirect("index")

def createNote(request):

    username = request.POST['username']
    note = request.POST['note']

    date_time = helpers.get_datetime(note)

    newNote = Note(user=username, text_body=note, time=date_time)# TODO: START and EXPIRATION date objects
    newNote.save()

    # SHOULD REDIRECT TO LOGIN PAGE
    return redirect("index")