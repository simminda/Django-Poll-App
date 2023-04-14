from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, PasswordChangeForm 
from django.core.paginator import Paginator

# Poll views
def home(request):
    return render(request, 'polls/home.html', {})

def poll(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, "polls/poll.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice']
    )
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Return an HttpResponseRedirect after successfully dealing with POST data.
        return HttpResponseRedirect(
            reverse('results', args=(question_id,)) # not 'poll:results' because did not specify app name in urls.py
        )

def search_polls(request):
    
    if request.method == "POST":
        searched = request.POST['searched']
        polls = Question.objects.filter(question_text__contains=searched)
	
        return render(request, 
		'polls/search_polls.html', {'searched':searched, 'polls':polls})
    else:
        return render(request, 'polls/search_polls.html', {})

# Authentication
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Thank you for Logging in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error Logging In - Please Try Again'))
            return redirect('login')
    else:
        return render(request, 'polls/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been Logged Out...'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You Have Registered...'))
            return redirect('home')
    else:
        form = SignUpForm()
    
    context = {'form': form}
    return render(request, 'polls/register.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You Have Edited Your Profile...'))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'polls/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)    # Stay Logged in after Password Change
            messages.success(request, ('You Have Edited Your Password...'))
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {'form': form}
    return render(request, 'polls/change_password.html', context)

# Legacy views
def blog(request):
    return render(request, 'polls/blog.html', {})

def post(request):
    return render(request, 'polls/post.html', {})