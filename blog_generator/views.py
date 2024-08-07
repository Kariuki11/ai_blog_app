import json
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
import os
import assemblyai as aai
import gemini

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
        
#         #Use gemini to generate the blog
        
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
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "Failed to get transcript"}, status=500)
        
        #Use OpenAI to generate the blog
        blog_content = generate_blog_from_transcription(treanscription)
        if not blog_content:
            return JsonResponse({'error': "Failed to generate blog"}, status=500)
        # save blog article to database.
        
        #Return blog aricle as a response.
        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
        
def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = "0e7f4fef0c264e569363fb4993f62b18"
    
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    
    return transcriber.text


def generate_blog_from_transcription(transcription):
    gemini.api_key = "AIzaSyB2rrGuPKXfyQHvATyyH67LJsyWcPTcUig"
    
    prompt = f"Based on the following transaction from a YouTube video, write a comprehensive blog article, write it based the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    
    response = gemini.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
    )
    
    generated_content = response.choices[0].text.strip()
    
    return generated_content

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
