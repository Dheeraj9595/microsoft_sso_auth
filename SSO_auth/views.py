from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from SSO_auth.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token
from SSO_auth.graph_helper import fetch_user_data, get_user_view
from django.http import HttpResponseBadRequest
import requests

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
    token_result = get_token_from_code(request)
    if token_result:
        # Fetch user data
        user_data = fetch_user_data(token_result['access_token'], request)
        if user_data:
            # Store user data
            store_user(request, user_data)
            return redirect(f"http://localhost:3000/admin/")
    # If something went wrong, handle it here
    return HttpResponseBadRequest("Failed to fetch user data or token")