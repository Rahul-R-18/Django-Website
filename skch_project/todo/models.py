from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    SUBJECT_CHOICES=(
        ("Physics","Physics"),
        ("Chemistry","Chemistry",),
        ("Computer Science","Computer Science"),
        ("Maths","Maths"),
        ("English","English")
    )
    title=models.CharField(max_length=100)
    memo=models.TextField(blank=True)
    subject=models.CharField(max_length=100,blank=True,choices=SUBJECT_CHOICES,default="Physics")
    created=models.DateTimeField(auto_now_add=True)      
    datecompleted=models.DateTimeField(null=True, blank=True)  
    important=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)  
    deadline=models.DateField(null=True, blank=True) 

    
    def __str__(self):
        return f"{self.title} { self.important} {self.subject}"
