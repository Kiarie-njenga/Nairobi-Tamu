













from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from blog.models import Post

from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm, ContactForm
from .models import User, Profile


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            check_user = User.objects.filter(
                Q(username=data['username']) | Q(email=data['email'])
            )
            if not check_user:
                user = User.objects.create_user(
                    data['email'], data['username'], data['password']
                )
                return redirect('user_login')
    else:
        form = UserRegistrationForm()
    context = {'title':'Signup', 'form':form}
    return render(request, 'register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = UserLoginForm()
    context = {'title':'Login', 'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('user_login')








def profile(request, username):
    user = get_object_or_404(User, username=username)
    related_profiles=Profile.objects.filter(location=user.profile.location)
    posts=Post.objects.filter(author__username=username)
    context = {
        'user': user,
        'posts':posts,
        'related_profiles':related_profiles,
        
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)
    context = {'title': 'Edit Profile', 'form': form}
    return render(request, 'edit_profile.html', context)

