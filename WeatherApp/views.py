from django.http import HttpResponse
import requests
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c2074136cb20370ffb649990ce49a17e'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "This city is already shown")

    form = CityForm()

    cities = City.objects.all().order_by('-id')

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'Weather/index.html', context)

def deletee(request,city): 
    City.objects.get(name=city).delete()
    return redirect('index')
