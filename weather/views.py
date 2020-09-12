import requests
from django.shortcuts import render, redirect
from .models import City 
from .forms import CityForm


def index(request):

	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=7690c149e777e72e2147207a0435f25b'
	message = ""
	error_msg = ""

	if request.method == "POST":
		form = CityForm(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data['name']
			duplicate_city = City.objects.filter(name=new_city).count()
			if duplicate_city == 0:	
				r = requests.get(url.format(new_city)).json()
				if r['cod'] == 200:
					form.save()
				else:
					error_msg = "City is not existed!"
			else:
				error_msg = "City is already existed!"

		if error_msg:
			message = error_msg
		else:
			message	= "City added succesfully."

	else:
		form = CityForm()


	cities_list = []
	cities = City.objects.all()
	for city in cities: 
		r = requests.get(url.format(city)).json()		
		city_weather = {
			'City': city.name,
			'Weather': r['weather'][0]['description'],
			'Temperature': r['main']['temp'],
			'Wind': r['wind']['speed'],
			'Icon': r['weather'][0]['icon'],
		}

		cities_list.append(city_weather)

	context = {'cities_list': cities_list, 'form': form, 'message': message}
	return render(request, 'weather.html', context)


def delete(request, city_name):
	city = City.objects.get(name=city_name)
	city.delete()
	return redirect('home')