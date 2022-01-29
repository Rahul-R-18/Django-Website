from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm,PQuestionForm,AQuestionForm,UserForm
from .models import Todo,Question,Qbank,Python_Test_Status
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import random
import re



def home(request):
    return render(request, 'todo/home.html')
    

def signupuser(request):
    if request.method=="GET":
        return render(request,'todo/signupuser.html',{'form':UserForm()})
    else:        
        print(request.POST)
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()            
            return redirect('loginuser')
        else:
            err=form.errors
            return render(request,'todo/signupuser.html',{'form':UserForm(),'error':err})

@login_required
def currenttodos(request):
    todos=Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html',{'todos':todos})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',{'form':AuthenticationForm(),'error':'incorrect username or password'})
        else:
            login(request,user)
            return redirect('about')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)            
            newtodo=form.save(commit=False)
            newtodo.user=request.user            
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',{'form':TodoForm(),'error':'Bad Data passed in'})

@login_required
def viewtodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk,user=request.user)

    """
    other 3 ways to achieve the same as above
    todo=Todo.objects.get(pk=todo_pk)
    todo=Todo.objects.filter(pk=todo_pk)[0]
    todo=Todo.objects.filter(user=request.user).get(pk=todo_pk)
    """

    # print(todo,type(todo))

    if request.method=='GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html',{'todo':todo,'form':form})
    else:        
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            print("error")
            return render(request, 'todo/viewtodo.html',{'todo':todo,'form':form,'error':'Bad Data passed in'})

@login_required
def completetodo(request, todo_pk):
    todo  = get_object_or_404(Todo, pk=todo_pk,user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo  = get_object_or_404(Todo, pk=todo_pk,user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.delete()
        return redirect('currenttodos')
        
@login_required
def completedtodos(request):
    todos=Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html',{'todos':todos})


#####################################################################################




def notes(request):
    return render(request, 'todo/notes.html')

def about(request):
    return render(request, 'todo/about.html')


@login_required
def postq(request):
    if request.method == 'GET':
        return render(request, 'todo/postq.html', {'form':PQuestionForm()})
    else:
        try:
            form = PQuestionForm(request.POST)
            newq = form.save(commit=False)
            newq.user = request.user
            newq.save()
            return redirect('unanswered')
        except ValueError:
            return render(request, 'todo/postq.html', {'form':PQuestionForm(), 'error':'Bad data Passed in'})

@login_required 
def answered(request):
    questions = Question.objects.filter(answered__isnull=False)
        
    return render(request, 'todo/answered.html',{'questions':questions})

@login_required
def unanswered(request):
    questions = Question.objects.filter(answered__isnull=True)
    return render(request, 'todo/unanswered.html',{'questions':questions})

@login_required
def answer(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)

    if request.method == 'GET':
        form = AQuestionForm(instance=question)
        return render(request, 'todo/answer.html',{'question':question, 'form':form})           
    else:
        try:
            form = AQuestionForm(request.POST, instance=question)
            form.save()
            question.answered = timezone.now()
            question.save()
            return redirect('unanswered')
        except ValueError:
            return render(request, 'todo/answer.html',{'question':question, 'form':form, 'error': 'Bad info'})



@login_required
def mcqpython(request):   
    
    #number of questions to be asked in the test
    questions_in_test=5

    if request.method=='GET':
        #sending random questions from the question bank
        print("within GET",request.GET,type(request.GET))
        all_questions=Qbank.objects.all()
        print("all questions",all_questions,type(all_questions))
        random_questions=random.sample(list(all_questions),questions_in_test)
        print("Questions picked",random_questions,type(random_questions))
        return render(request,'todo/mcqpython_view.html',{"questions":random_questions,"number_qs":questions_in_test})
    else:
        print("within POST",request.POST,type(request.POST))
        marks=0                
        try:          
            questions_list={}
            #Extracting the answers submitted by the user and storing as dictionary
            for key in request.POST.keys():
                if re.search("Qn",key):
                    questions_list[key]=request.POST[key]
            print("answers submitted",questions_list)            
            total_questions=len(questions_list)

            for question in questions_list.keys():
                dummy=question.split("Qn")  #all form variable names will be of the form "Qn<x>", where x is the primary key of the qbank                 
                record=Qbank.objects.get(pk=int(dummy[1]))         
                print(record)       
                correct_answer=record.answer                             
                if questions_list[question]==correct_answer:
                    marks=marks+1
                    print("Correct")
                else:
                    print("Wrong")
        except:
            error="Some Exception happened."            
            all_questions=Qbank.objects.all()
            random_questions=random.sample(list(all_questions),questions_in_test)            
            return render(request,'todo/mcqpython_view.html',{"questions":random_questions,"error":error,"number_qs":questions_in_test})

        #calculating the marks
        score = marks / questions_in_test * 100 
        
        #checking for pass/fail
        if score>=40:
            result=1
        else:
            result=0
        
        #adding a entry to Python_Test_Status table
        new_entry = Python_Test_Status()
        new_entry.user=request.user
        new_entry.marks=int(score)
        print(int(score))

        if result==1:
            new_entry.status="Pass"
        else:
            new_entry.status="Fail"

        print("Printing the new entry to be inserted into the python status table")
        print(new_entry,type(new_entry))

        new_entry.save()

        #returning the result to the user
        return render(request,'todo/passfail.html',{"result":result,"score":round(score)})



@login_required
def mcqpython_status(request):
    test_entries=Python_Test_Status.objects.filter(user=request.user)
    return render(request, 'todo/test_entries.html',{'test_entries':test_entries})
