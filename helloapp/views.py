from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests


OPENWEATHERMAP_API_KEY = 'b3fef8b95a14fae542ced6b78d77b2b2'

@api_view(['GET'])
def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = request.META.get('REMOTE_ADDR')


    # if client_ip == '127.0.0.1':
    #     client_ip = '8.8.8.8'

    
    location_response = requests.get(f"http://ip-api.com/json/{client_ip}")
    print(location_response.content)
    location_data = location_response.json()

    city = location_data.get('city', 'Unknown Location')
    if city == 'Unknown Location':
        temperature = "Unknown"
    else:
        weather_response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OPENWEATHERMAP_API_KEY}"
        )
        print(weather_response.content)
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp'] if 'main' in weather_data else "Unknown"

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    return JsonResponse({
        'client_ip': client_ip,
        'location': city,
        'greeting': greeting
    })

