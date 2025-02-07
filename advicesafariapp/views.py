
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from advicesafari import settings
from advicesafariapp.models import PasswordReset, Product
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



def home(request):
    products = Product.objects.all()  # Fetch all products
    return render(request,'home.html', {'products': products})

@login_required
def index(request):
    products = Product.objects.all()  # Fetch all products
    return render(request,'index.html', {'products': products})

def register(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        # Validation for required fields
        if not uname:
            error = "Username required"
            return render(request, 'register.html', {'message': error, 'username': uname, 'email': email, 'password1': pass1, 'password2': pass2})
        
        if not email:
            error = "Email field is required"
            return render(request, 'register.html', {'message': error, 'username': uname, 'email': email, 'password1': pass1, 'password2': pass2})
        
        if '@' not in email:
            error = "Invalid email address. It must contain an '@' symbol"
            return render(request, 'register.html', {'message': error, 'username': uname, 'email': email, 'password1': pass1, 'password2': pass2})
        
        if not pass1 or not pass2:
            error = "Password required"
            return render(request, 'register.html', {'message': error, 'username': uname, 'email': email, 'password1': pass1, 'password2': pass2})
        
        if len(pass1) < 8:
            error = "password must be Atleast 8 charecter"
            return render(request, 'register.html', {'message': error,'username': uname, 'email': email, 'password1': pass1, 'password2': pass2})
        
        # Check if passwords match
        if pass1 != pass2:
            error = "Passwords are not matching"
            return render(request, 'register.html', {'message': error, 'username': uname, 'email': email, 'password1': pass1, 'password2': pass2})
        
        if User.objects.filter(username=uname).exists():
            error = "This username already exists"
            return render(request, 'register.html', {'message': error, 'username': uname, 'email': email, 'password1': pass1, 'password2': pass2})
        
        if User.objects.filter(email=email).exists():
            error = "This email already exists"
            return render(request, 'register.html', {'message': error, 'username': uname, 'email': email, 'password1': pass1, 'password2': pass2})
        
        # Create the user
        try:
            user = User.objects.create_user(username=uname, password=pass1, email=email)
            user.save()
            success = "User created successfully"
            return render(request, 'register.html', {'success': success})
        except Exception as e:
            return HttpResponse(f"Error creating user: {str(e)}", status=400)
    
    return render(request, 'register.html')

from django.contrib.auth import login  # Import login function

def signin(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("Email:", email)
        print("Password:", password)
        
        #validation
        if not email:
             error = "Email field is required"
             return render(request, 'signin.html', {'message': error,'email': email, 'password': password})
        
        if '@' not in email:
            error = "Invalid email address. It must contain an '@' symbol"
            return render(request, 'signin.html', {'message': error,'email': email, 'password': password})
        
        if not password:
            error = "Password required"
            return render(request, 'signin.html', {'message': error,'email': email, 'password': password})
        
        if len(password) < 8:
            error = "password must be Atleast 8 charecter"
            return render(request, 'signin.html', {'message': error,'email': email, 'password': password})
        
       
        # Try to get the user by email
        try:
            # Query the User model based on email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        if user is not None and user.check_password(password):
            # If user is found and password is correct, authenticate and login
            login(request, user)
            print("Authentication successful")
            if request.user.is_authenticated:
                return redirect('index')  # Adjust to your actual home page URL
        else:
            # Authentication failed, add error message
            print("Authentication failed")
            error = "email and password is incorrect"
            return render(request, 'signin.html', {'message': error,'email': email, 'password': password})
    
    return render(request, 'signin.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Make sure 'index' exists in your urls.py

def forgot_password(request):
   
    if request.method == 'POST':
        email = request.POST.get('email') 
            
        try:
            user = User.objects.get(email=email)
            new_password_reset = PasswordReset(user = user)
            new_password_reset.save()
            password_reset_url = reverse('change_password',kwargs={'reset_id':new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
            
            email_message = EmailMessage(
                'Reset your password', #email subject
                email_body,
                settings.EMAIL_HOST_USER,#email sender
                [email] # receiver
            )
            
            email_message.fail_silently = True
            email_message.send()
            
            return redirect('password_reset_sent',reset_id=new_password_reset.reset_id)
        
                
        except User.DoesNotExist:
            error = f"No user with email '{email}' found."
            return render(request, 'forget_password/forget_password.html', {"message": error})
            
    return render(request, 'forget_password/forget_password.html')

def password_reset_sent(request,reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request,'forget_password/password_reset_sent.html')
    else:
        #redirect to forgot password page if code does not exist
        return redirect('forget_password')
    
def change_password(request,reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
        
        if request.method=="POST":
            password = request.POST.get('new_password1')
            confirm_password = request.POST.get('new_password2')
            
            password_have_error = False
            
            if not password:
                password_have_error = True
                error = "Password required"
                return render(request,'forget_password/change_password.html',{"message":error})
            
            if len(password) < 8:
                password_have_error = True
                error = "password must be Atleast 8 charecter"
                return render(request,'forget_password/change_password.html',{"message":error})
            
            if password != confirm_password:
                password_have_error = True
                error = "Password is not matching together"
                return render(request,'forget_password/change_password.html',{"message":error})
            
            
            
            expiration_time = password_reset_id.created_when + timedelta(minutes=10)
            
            if timezone.now() > expiration_time:
                password_have_error = True
                error = "reset link has expired"
                password_reset_id.delete()
                return render(request,'forget_password/change_password.html',{"message":error})
            
            if not password_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()
                
                #delete reset id after use
                password_reset_id.delete()
                
                return render(request,'forget_password/password_reset_complete.html')
            else:
                return redirect('change_password',reset_id=reset_id)
            
    except PasswordReset.DoesNotExist:
        return redirect('forget_password')
    
    return render(request,'forget_password/change_password.html')

def listyourproperty(request):
    products = Product.objects.all()  # Fetch all products
    return render(request,'listyourproperty.html', {'products': products})

@login_required
def booking(request):
    products = Product.objects.all()  # Fetch all products
    return render(request,'booking.html', {'products': products})



@login_required
def AddToCart(request):
    products = Product.objects.all()  # Fetch all products
    return render(request,'booking.html', {'products': products})







