# localconnect/forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]

    # CATEGORY_CHOICES = [
    #     ('it', 'IT'),
    #     ('marketing', 'Marketing'),
    #     ('finance', 'Finance'),
    #     ('hr', 'HR'),
    #     ('other','other')
    #     # add other categories
    # ]
    
    CATEGORY_CHOICES = [
    ('it', 'IT / Software'),
    ('marketing', 'Marketing / Sales'),
    ('finance', 'Finance / Accounting'),
    ('hr', 'Human Resources'),
    ('education', 'Education / Training'),
    ('healthcare', 'Healthcare / Medical'),
    ('design', 'Design / Creative'),
    ('engineering', 'Engineering'),
    ('legal', 'Legal / Compliance'),
    ('operations', 'Operations / Admin'),
    ('customer_service', 'Customer Service'),
    ('other', 'Other')
    ]
    
    job_type = forms.ChoiceField(choices=JOB_TYPE_CHOICES, widget=forms.Select())
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select())
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'category', 'vacancies', 'salary', 'description', 'location', 'contact']


from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'price', 'description', 'location', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows':3, 'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }
# from django import forms
# from .models import Job

# class JobForm(forms.ModelForm):
#     class Meta:
#         model = Job
#         fields = ['title', 'type', 'category', 'vacancies', 'salary', 'description', 'location', 'contact']
#         widgets = {
#             'type': forms.Select(attrs={'class': 'form-select'}),
#             'category': forms.Select(attrs={'class': 'form-select'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'vacancies': forms.NumberInput(attrs={'class': 'form-control'}),
#             'salary': forms.TextInput(attrs={'class': 'form-control'}),
#             'location': forms.TextInput(attrs={'class': 'form-control'}),
#             'contact': forms.TextInput(attrs={'class': 'form-control'}),
#         }


from .models import MapItem
from django.contrib.auth.models import User

class MapItemForm(forms.ModelForm):
    class Meta:
        model = MapItem
        fields = ['title', 'description', 'location', 'category', 'price', 'image', 'latitude', 'longitude', 'category']

# class LoginForm(forms.Form):
#     username_or_email = forms.CharField(label="Username or Email")
#     password = forms.CharField(widget=forms.PasswordInput)
    
class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

import re
class SignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="First Name")
    last_name = forms.CharField(max_length=50, required=True, label="Last Name")
    username = forms.CharField(max_length=50, required=True, label="Username")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")
    location = forms.CharField(max_length=100, required=True, label="Location")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Validate password strength
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Password must contain at least one special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")

    #     if password != confirm_password:
    #         raise forms.ValidationError("Passwords do not match!")
        
        
# from .models import Profile

# class ProfileForm(forms.ModelForm):
#     username = forms.CharField(max_length=150)
#     first_name = forms.CharField(max_length=150, required=False)
#     last_name = forms.CharField(max_length=150, required=False)

#     class Meta:
#         model = Profile
#         fields = ['profile_image', 'location']
    
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Profile
        fields = ['profile_image', 'location']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
        
        
        
        
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image', 'document', 'video']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a message...'})
        }