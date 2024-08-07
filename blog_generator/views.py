import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

# @csrf_exempt
# def generate_blog(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             yt_link = data['link']
#             return JsonResponse({'content': yt_link})
#         except(KeyError, json.JSONDecodeError):
#             return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
#         #get yt title
        
#         #get transcript
        
#         #Use OpenAI to generate the blog
        
#         #save blog article to data base
        
#         #return blog article as a response.
        
#     else:
#         return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)


        # get yt title
        title = yt_title(yt_link)
        
        # get transcript.
        
        #Use OpenAI to generate the blog
        
        # save blog article to database.
        
        #Return blog aricle as a response.
        
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
        
def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid name or password"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password,)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message:error_message'})
        else:
            error_message = 'Password do not match'
            return render(request, 'signup.html', {'error_message:error_message'})
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')
