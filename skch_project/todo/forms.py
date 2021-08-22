from django.forms import ModelForm
from .models import Todo,Question
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TodoForm(ModelForm):
    class Meta:
        model=Todo        
        fields=['title','subject','memo','important','deadline']
        labels={
            "deadline":"Deadline (YYYY-MM-DD)"
        }

class PQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['Question','urgent','subject']

class AQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['answer']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username','email', 'password1' ,'password2' )

