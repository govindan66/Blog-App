from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CreateUserForm, LoginForm as AuthenticationForm, BlogsForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
import random
from .models import BlogPost
from django.contrib.auth.models import User

# Homepage View


def index(request):
    if not request.user.is_authenticated:
        check_session(request)
    featured_post = BlogPost.objects.filter(featured=True)
    index = random.shuffle(featured_post)
    blogs = BlogPost.objects.all()
    # print(request.user)
    context = {
        'blogs': blogs,
        'featured': featured_post,
    }
    return render(request, 'blogs/index.html', context)

# View for Signup


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='Author')
                user.groups.add(group)
                messages.success(request, 'Account Created successfully')
                return redirect('/login/')
        else:
            form = CreateUserForm()
        return render(request, 'blogs/signup.html', context={'form': form})
    else:
        return redirect('/profile/')

# Check Session authentication
def check_session(request):
    if 'username' in request.session and 'password' in request.session:
        user = authenticate(request,
            password=request.session.get('password'),
            username=request.session.get('username'))
        # print(request.session['username'],request.session['password'])
        if user is not None:
            login(request, user)
            messages.success(request,'You are logged in')
            # if 'next' in request.POST:
            #     return redirect(request.POST.get('next'))
            # return redirect('/')

# View for Login

def login_view(request):
    if not request.user.is_authenticated:
        check_session(request)
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                print(username, password)
                user = authenticate(username=username, password=password)
                if user is not None:
                    if True in request.POST.getlist('remember'):
                        request.session['username'] = username
                        request.session['password'] = password

                    login(request, user)
                    messages.success(request, "you are logged in successfully")
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    return redirect('/profile/')
        else:
            form = AuthenticationForm()  #Request is GET
        return render(request, 'blogs/login.html', {'form': form})
    else:
        return redirect('/profile/')

# View for Logout


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    request.session.flush()
    messages.info(request, 'You are Logged out!')
    return redirect('/')

# View for profile Dashboard


@login_required(login_url='/login/')
def profile(request):
    if request.user.is_authenticated:
        blogs = BlogPost.objects.all()
        return render(request, 'blogs/profile.html', context={'posts': blogs})
    else:
        return redirect('/login/')

# view for About page


def about(request):
    return render(request, 'blogs/about.html')

# VIew for Contact Page


def contact(request):
    return render(request, 'blogs/contact.html')

# View for Change Password


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed')
            return redirect('/profile/')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'blogs/changePassword.html', {'form': form})

# Add Blogs View


@login_required(login_url='/login/')
def addBlogs(request):
    if request.method == 'POST':
        form = BlogsForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            blog.author = request.user
            messages.success(request, 'Blogs has been added successfully')
            form = BlogsForm()
    else:
        form = BlogsForm()
    return render(request, 'blogs/addBlogs.html', {'form': form})

# Edit Post View


@login_required(login_url='/login/')
def updateBlogs(request, id):
    if request.method == 'POST':
        blog = BlogPost.objects.get(pk=id)
        form = BlogsForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            if request.POST['id_featured']:
                blog.featured = True
                blog.save()
            messages.success(request, 'Blog updated successfully')
            return redirect('/profile/')
    else:
        blog = BlogPost.objects.get(pk=id)
        form = BlogsForm(instance=blog)
    return render(request, 'blogs/updateBlogs.html', context={'form': form})


# Delete Post View
@login_required(login_url='/login/')
@permission_required('blogs.delete_blogPost')
def deleteBlogs(request, id):
    if request.method == 'POST':
        blog = BlogPost.objects.get(pk=id)
        blog.delete()
        messages.success(request, "Blog deleted successfully")
        return redirect('/profile/')
    return redirect('/profile/')


def viewBlogs(request, id):
    blog = BlogPost.objects.get(pk=id)
    user = User.objects.get(pk=blog.author.pk)
    return render(request, 'blogs/blog.html', context={
        'blog': blog,
        'author': user
    })

def allBlogs(request):
    blogs = BlogPost.objects.all()
    return render(request,'blogs/bloglist.html',{'blogs':blogs})
