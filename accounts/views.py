from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User 
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts_form.html', context)

def login(request):
    if request.method == "POST":
        form = CustomAthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:index')
    else: 
        form = CustomAthenticationForm()

    context = {
        'form':form,
    }

    return render(request, 'accounts_form.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

def profile(request, username):
    user_info = User.objects.get(username=username)

    context = {
        'user_info': user_info,
    }

    return render(request, 'profile.html', context)

def follows(request, username):
    me = request.user  # 동작을 실행한 사람
    you = User.objects.get(username=username)   # 내가 팔로우하고 싶은 사람

    # 이미 팔로잉이 되어있는 경우
    if you in me.followings.all():
    # == if me in you.followers.all():
        me.followings.remove(you)
    # 아직 팔로잉이 안되어있는 경우
    else:
        me.followings.add(you)

    return redirect('accounts:profile', username=username)
 


