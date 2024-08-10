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
import anthropic
from .models import BlogPost

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
            print(f"Received YouTube link: {yt_link}")
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)

        try:
            # Get YouTube video title
            title = yt_title(yt_link)
            print(f"Video Title: {title}")

            # Get transcription
            transcription = get_transcription(yt_link)
            if not transcription:
                return JsonResponse({'error': "Failed to get transcript"}, status=500)

            # Use OpenAI to generate the blog
            blog_content = generate_blog_from_transcription(transcription)
            if not blog_content:
                return JsonResponse({'error': "Failed to generate blog"}, status=500)

            # Save blog article to the database
            new_blog_article = BlogPost.objects.create(
                user=request.user,
                youtube_title=title,
                youtube_link=yt_link,
                generated_content=blog_content,
            )
            new_blog_article.save()

            # Return blog article as a response
            return JsonResponse({'content': blog_content})

        except Exception as e:
            print(f"Error during blog generation: {e}")
            return JsonResponse({'error': 'Error during blog generation'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()  # Assign to a variable
    out_file = video.download(output_path=settings.MEDIA_ROOT)  # Download audio
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file  # Return the file path

def get_transcription(link):
    try:
        audio_file = download_audio(link)
        print(f"Audio file downloaded: {audio_file}")
        
        aai.settings.api_key = "your-assemblyai-api-key-here"  # Replace with your AssemblyAI API key
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        
        return transcript.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def generate_blog_from_transcription(transcription):
    try:
        anthropic.api_key = "your-anthropic-api-key-here"  # Replace with your Anthropic API key
        
        prompt = (
            f"Based on the following transcription from a YouTube video, "
            f"write a comprehensive blog article. Make it look like a proper blog article:\n\n"
            f"{transcription}\n\nArticle:"
        )
        
        response = anthropic.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=2048,
        )
        
        generated_content = response.choices[0].text.strip()
        return generated_content
    except Exception as e:
        print(f"Error during blog generation from transcription: {e}")
        return None

@login_required
def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "all-blogs.html", {'blog_articles': blog_articles})

@login_required
def blog_details(request, pk):
    try:
        blog_article_detail = BlogPost.objects.get(id=pk)
        if request.user == blog_article_detail.user:
            return render(request, 'blog-details.html', {'blog_article_detail': blog_article_detail})
        else:
            return redirect('/')
    except BlogPost.DoesNotExist:
        return redirect('/')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
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
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')
