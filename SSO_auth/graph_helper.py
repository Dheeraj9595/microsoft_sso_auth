import requests
import json
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth import login


# def get_user(token):
#     graph_endpoint = 'https://graph.microsoft.com/v1.0/me'
#     headers = {
#         'Authorization': 'Bearer ' + token
#     }
#     try:
#             response = requests.get(graph_endpoint, headers=headers)
#             response.raise_for_status()  # Raise an exception for bad responses
#             user_data = response.json()
#             user_obj = User.objects.get(email=user_data['email'])
#             # Assuming `request` is available within the class
#             login(self.request, user_obj)
#             return user_data
#         except Exception as e:
#             # Handle any errors that occur during the API request
#             print('Error fetching user data:', e)
#             return None


def get_user_view(request):
    token = request.session.get('access_token')
    if token:
        user_data = fetch_user_data(token, request)
        if user_data:
            return redirect('http://localhost:3000/admin/')
    return HttpResponseBadRequest("Invalid credentials or token not found in cache.")

def fetch_user_data(token, request):
    breakpoint()
    graph_endpoint = 'https://graph.microsoft.com/v1.0/me'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    try:
        response = requests.get(graph_endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses
        user_data = response.json()
        breakpoint()
        user_obj = User.objects.get(email=user_data['mail'])
        # Assuming `request` is available within the function
        login(request, user_obj)
        return user_data
    except Exception as e:
        # Handle any errors that occur during the API request
        print('Error fetching user data:', e)
        return None
