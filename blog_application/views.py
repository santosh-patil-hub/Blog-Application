from django.shortcuts import render,redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Blog, Comment
from django.core.paginator import Paginator
from django.utils import timezone

def blog_view(request):
    blogs = Blog.objects.all()
    user = request.user

    # Set up pagination
    paginator = Paginator(blogs, 6)  # Show 6 blogs per page
    page_number = request.GET.get('page')  # Get the page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the blogs for the requested page

    context = {
        'page_obj': page_obj,
        'user': user,  # Pass the current user to the template
    }
    return render(request, 'common/blog.html', context)



# User Registration View
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # Check if passwords match
        if password == password2:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
            # Check if the email is already registered
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
            else:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'User registered successfully')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'auth/register.html')

# User Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('blog')  # Redirect to the home page after login
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'auth/login.html')


# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Blog

def profile_view(request):
    user = request.user
    user_blogs = Blog.objects.filter(author=user)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:  # Basic validation
            blog = Blog(title=title, content=content, author=user)
            blog.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('profile')  # Redirect to the profile page

    context = {
        'user_blogs': user_blogs,
    }
    return render(request, 'common/profile.html', context)

def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)  # Ensure the user is the author

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.date = timezone.now()  # Update the date

        blog.save()
        messages.success(request, 'Blog updated successfully!')
        return redirect('profile')  # Redirect to the profile page or wherever you want

    return render(request, 'common/update_blog.html', {'blog': blog})


def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)  # Ensure the user is the author

    if request.method == "POST":
        blog.delete()
        messages.success(request, 'Blog deleted successfully!')
        return redirect('profile')  # Redirect to the profile page or wherever you want

    return render(request, 'common/delete_blog.html', {'blog': blog})



 # Ensure you have the Comment model imported

def blog_detail_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Handle comment submission
    if request.method == 'POST':
        content = request.POST.get('comment')
        Comment.objects.create(blog=blog, user=request.user, content=content)
        return redirect('blog_detail', blog_id=blog.id)  # Redirect to the same blog detail page

    # Fetch comments for the blog
    comments = blog.comments.all()  # Use the related manager to get comments

    return render(request, 'common/blog_details.html', {'blog': blog, 'comments': comments})