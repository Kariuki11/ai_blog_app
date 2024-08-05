from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_login(request):
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            pass
        else:
            error_message = 'Password do not match'
            return render(request, 'signup.html' {'error_message:error_message'})
    return render(request, 'signup.html')

def user_logout(request):
    return render(request, 'signup.html')
