from .models import Account
from django import forms

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={

       "placeholder":"password",
        "class" : "form-control"
    }
    
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"confirm password",
        "class" : "form-control"
    }))


    class Meta:
        model = Account
        fields = ['firstname', "lastname", "email", "phone_number", "password"]

    def clean(self):

        clean_data = super(RegisterForm, self).clean()

        pass1 = clean_data.get("password")
        pass2 = clean_data.get('confirm_password')

        if pass1 != pass2:
            raise forms.ValidationError(
                "password doesn't match"
            )



    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__( *args, **kwargs)
        self.fields["firstname"].widget.attrs["placeholder"] = "First name"
        self.fields["lastname"].widget.attrs["placeholder"] = "Last name"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        for field in self.fields:

            self.fields[field].widget.attrs["class"] = "form-control"
    