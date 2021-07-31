from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm,PQuestionForm,AQuestionForm
from .models import Todo,Question
from django.utils import timezone
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'todo/home.html')
    
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        print(request.POST)
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',{'form':UserCreationForm(),"error":"Username already exists"})
        else:
            
            return render(request, 'todo/signupuser.html',{'form':UserCreationForm(),"error":"Passwords didn't match"})

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
            return redirect('currenttodos')

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
