from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from SSO_auth.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token
from SSO_auth.graph_helper import *

def home(request):
    try:
        context ={'user':request.session['user']}
    except:
        context ={}
    return render(request, 'home.html', context)

def initialize_context(request):
    context = {}
    error = request.session.pop('flash_error', None)
    if error != None:
      context['errors'] = []
    context['errors'].append(error)
    # Check for user in the session
    context['user'] = request.session.get('user',{'is_authenticated': False})
    return context

def sign_in(request):
    # Get the sign-in flow
    flow = get_sign_in_flow()
    # Save the expected flow so we can use it in the callback
    try:
        request.session['auth_flow'] = flow
    except Exception as e:
        print(e)
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(flow['auth_uri'])


def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)
    return HttpResponseRedirect(reverse('home'))


def callback(request):
    # Make the token request
    breakpoint()
    result = get_token_from_code(request)
    #Get the user's profile from graph_helper.py script
    user = get_user(result['access_token']) 
    # Store user from auth_helper.py script
    store_user(request, user)
    return redirect(f"token?access_token={result['access_token']}")

import msal
def get_power_bi_access_token(request):

    breakpoint()
    
    access_token = request.GET.get('access_token') # Replace with your SSO access token
    report_id = 'd2d09420-8cce-40f1-9447-a1b04daaf5d3'  # Replace with the Power BI report ID
    group_id = '5d01b1d3-4f41-4857-9cda-e6b914f633e4'

    # Define the API endpoint for requesting an embed token
    endpoint = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/GenerateToken'

    # Set up the request headers with the access token
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
    }

    # Define the request body (if needed)
    request_body = {
    "accessLevel": "View",
    }


    try:
        response = requests.post(endpoint, headers=headers, json=request_body)
        if response.status_code == 200:
            embed_token = response.json()['token']
            # You now have the embed token to use for embedding the report.
            return render(request, 'power_bi_report.html', {'access_token': embed_token})
        else:
            print(f'Error requesting embed token: {response.status_code}')
            return render(request, 'power_bi_report.html', {'access_token': access_token})
    except Exception as e:
        print(f'Error: {e}')
        return render(request, 'error.html', {'error_message': 'Failed to obtain Power BI access token'})
    #     return render(request, 'power_bi_report.html', {'access_token': access_token})
    # else:
    #     return render(request, 'error.html', {'error_message': 'Failed to obtain Power BI access token'})

def power_bi_proxy(request):
    # URL to the Power BI report
    breakpoint()
    power_bi_url = 'https://api.powerbi.com/v1.0/5d01b1d3-4f41-4857-9cda-e6b914f633e4/reports/d2d09420-8cce-40f1-9447-a1b04daaf5d3/GenerateToken'  # Replace with your report URL

    # Include the access token in the request headers
    headers = {
        'Authorization': f'Bearer {request.GET["access_token"]}',
        'Content-Type': 'application/json',
        'X-CSRFToken': request.GET['csrf']
    }

    # Make a request to the Power BI URL using the requests library
    response = requests.post(power_bi_url, headers=headers)

    # Return the response content with appropriate headers
    return JsonResponse(response.text, safe=False, status=response.status_code)
