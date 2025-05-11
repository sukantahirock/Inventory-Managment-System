from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import AdminRegistrationForm, AdminLoginForm



def register_view(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AdminLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
def refresh_token(request):
    refresh_token = request.session.get('refresh')
    
    if not refresh_token:
        return redirect('login')
    
    response = requests.post(
        'http://127.0.0.1:8000/api/token/refresh/',
        data={'refresh': refresh_token}
    )
    
    if response.status_code == 200:
        request.session['access'] = response.json()['access']
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    else:
        return redirect('login')