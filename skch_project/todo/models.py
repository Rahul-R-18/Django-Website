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
        
class Question(models.Model):
    
    Question = models.TextField()

    answer = models.TextField(blank=True)
    
    posted = models.DateTimeField(auto_now_add=True)

    answered = models.DateTimeField(null=True, blank=True)

    urgent = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete = models.CASCADE)#v imp for us

    subject_choices = (('cs','CS'),('math','MATH'),('physics','PHYSICS'),('chem','CHEM'))

    subject = models.CharField(max_length=10, choices=subject_choices, default='cs')

    def __str__(self):
        return self.Question


class Qbank(models.Model):
    question=models.TextField(max_length=500)
    choice1=models.TextField(max_length=200)
    choice2=models.TextField(max_length=200)
    choice3=models.TextField(max_length=200)
    choice4=models.TextField(max_length=200)
    answer=models.CharField(max_length=1)

class Python_Test_Status(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    status=models.TextField()
    test_date=models.DateTimeField(auto_now_add=True)
    marks=models.IntegerField()    
        
    def __str__(self):
        return f"{self.test_date} {self.status} {self.marks}"
