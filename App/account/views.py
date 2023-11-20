from django.shortcuts import render, redirect

from .form import RegisterForm
from .models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
#variafication 

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



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

            #user.save()

            current_site = get_current_site(request)

            


            to_email = email
            subject = "Please activate your account"
            message = render_to_string("account/activation.html", {
                'user':user,
                "domain": current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                "token":default_token_generator.make_token(user),


                                        })
            
            send_mail = EmailMessage(subject,message, to=[to_email])
             

            send_mail.send()

            
            #messages.success(request, "Thank you for registering. We hove sent you an email, Please check your email to varify")
            return redirect("/account/log_in/?command=varification&email="+email)
        
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



def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()

        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user= None
    

    if user is not None and default_token_generator.check_token(user, token):

        user.is_active = True

        user.save()
        messages.success(request, "Congratulation!")

        return redirect("log_in") 
    
    else:

        messages.error(request, "invalid activation link")
        return redirect("register")

