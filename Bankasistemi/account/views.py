from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_request(request):
    if request.user.is_authenticated:
        return redirect("anasayfa")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("anasayfa")
        else:
            return render(request, "account/login.html", {"error": "Kullanıcı adı ya da parola yanlış !"})

    return render(request, "account/login.html")

def diyetisyenlogin_request(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "account/diyetisyenlogin.html", {"error": "Doktor adı ya da parola yanlış !"})

    return render(request, "account/diyetisyenlogin.html")

def register_request(request):
    if request.user.is_authenticated:
        return redirect("anasayfa")
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        
        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", 
                {
                    "error": "Kullanıcı adı kullanılıyor !",
                    "username":username,
                    "email":email,
                    "firstname":firstname,
                    "lastname":lastname
                })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", 
                    {
                        "error": "Mail kullanılıyor !",
                        "username":username,
                        "email":email,
                        "firstname":firstname,
                        "lastname":lastname
                    })

                else:
                    user = User.objects.create_user(username=username, email=email, first_name=firstname, last_name=lastname,password=password) 
                    user.save()
                    return redirect("login")
        else:
            return render(request, "account/register.html", 
            {
                "error": "Parola eşleşmiyor !",
                "username":username,
                "email":email,
                "firstname":firstname,
                "lastname":lastname
            })
            
    return render(request, "account/register.html")

def logout_request(request):
    logout(request)
    return redirect("anasayfa")

"""
    from django.shortcuts import render, redirect
    from .forms import UserForm, DoctorForm

    def register_user(request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = UserForm()
        return render(request, 'register_user.html', {'form': form})

    def register_doctor(request):
        if request.method == 'POST':
            form = DoctorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DoctorForm()
        return render(request, 'register_doctor.html', {'form': form})
"""