from django.forms import ModelForm
from .models import Todo,Question

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
