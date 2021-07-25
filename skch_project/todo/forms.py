from django.forms import ModelForm
from .models import Todo

class TodoForm(ModelForm):
    class Meta:
        model=Todo        
        fields=['title','subject','memo','important','deadline']
        labels={
            "deadline":"Deadline (YYYY-MM-DD)"
        }


