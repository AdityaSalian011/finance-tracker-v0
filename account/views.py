# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib import messages
# # Create your views here.

# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password1']
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already taken!')
#             return redirect('sign_up')
#         user = User.objects.create_user(username=username, password=password)
#         login(request, user)
#         return redirect('add_income')
#     return render(request, 'account/signup.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('add_income')
#         else:
#             messages.error(request, 'Incorrect Credentials!')
#             return redirect('log_in')
#     return render(request, 'account/login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('log_in')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model


# login 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('add_income')
    else:
        form = AuthenticationForm(request)

    return render(request, 'account/login.html', {'form': form})

# logout
def logout_view(request):
    logout(request)
    return redirect('login')

# signUp/ registration
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'account/signup.html', {'form':form})

# password change if user logged In 
@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'account/passwordChange.html', {'form': form})

@login_required
def password_change_done_view(request):
    return render(request, 'account/passwordChangeDone.html')
        
# password reset is user forgets
def password_reset_view(request):  ## asks user for email and checks if email exist 
    if request.method == 'POST':   ## if yes, it sends a token via default_token_generator
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': None,
                'email_template_name': 'account/passwordResetEmail.html',
                'request': request
            }
            form.save(**opts)
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'account/passwordResetForm.html', {'form': form})

def password_reset_done_view(request):  ## To let user know that a link has been sent to their email
    return render(request, 'account/passwordResetDone.html')

def password_reset_confirm_view(request, uidb64, token):  ## After user clicks the link on email they land here
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)

    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)

        return render(request, 'account/passwordResetConfirm.html', {'form': form})
    else:
        return render(request, 'account/passwordResetConfirm.html', {'invalid_link': True})

def password_reset_complete_view(request):
    return render(request, 'account/passwordResetComplete.html')