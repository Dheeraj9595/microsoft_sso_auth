import requests
import json


def get_user(token):
    graph_endpoint = 'https://graph.microsoft.com/v1.0/me'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    try:
        breakpoint()
        response = requests.get(graph_endpoint, headers=headers)
        user_data = response.json()
        print(user_data)
        return user_data
    except Exception as e:
        # Handle any errors that occur during the API request
        print('Error fetching user data:', e)
        return None
