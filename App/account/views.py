from django.shortcuts import render, redirect

from .form import RegisterForm
from .models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

def register(request):

    if request.method == "POST":

        forms = RegisterForm(request.POST)

        if forms.is_valid():
            firstname = forms.cleaned_data['firstname']
            lastname = forms.cleaned_data['lastname']
            email= forms.cleaned_data['email']
            phone_number = forms.cleaned_data['phone_number']
            password = forms.cleaned_data['password']
            username = email.split("@")[0]


            user = Account.objects.create_user(
                username = username,
                email = email,
                firstname = firstname,
                lastname = lastname,
                password = password
            )
            user.phone_number = phone_number

            user.save()

            messages.success(request, "Account Created succesfully")
            return redirect("register")
    else:
        forms = RegisterForm()


    context = {"forms": forms}

    return render(request, "account/sign_up.html", context)


def log_in(request):

    if request.method == "POST":

        email = request.POST['email']
        pass1 = request.POST['password']

        user = authenticate(email= email, password = pass1)

        if user is not None:
            
            login(request,user)

            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("log_in")



    return render(request, "account/log_in.html")



@login_required(login_url="log_in")
def log_out(request):

    logout(request)
    messages.success(request, "Logi out")
    return redirect("log_in")