from django.shortcuts import render

from .form import RegisterForm
from .models import Account

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
    else:
        forms = RegisterForm()


    context = {"forms": forms}

    return render(request, "account/sign_up.html", context)


def log_in(request):

    return render(request, "account/log_in.html")