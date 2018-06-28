from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Job

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    me=User.objects.get(id=request.session['user_id'])
    context={
        'user' : me,
        'all_jobs' : Job.objects.all(),
        'my_jobs' : Job.objects.filter(plan_job=me)
    }
    return render(request, 'dashboard.html', context)

def register(request):
    response=User.objects.validateRegistration(request.POST)
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id']=response['user_id']
        return redirect('/dashboard')

def login(request):
    response=User.objects.validateLogin(request.POST)
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id']=response['user_id']
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def addJob(request):
    return render(request, 'addjob.html')

def createJob(request):
    errors=Job.objects.validateJob(request.POST, request.session['user_id'])
    if len(errors)>0:
        for error in errors:
            messages.error(request, error)
        return redirect('/addJob')
    else:
        return redirect('/dashboard')

def view(request, job_id):
    context={
        'jobs' : Job.objects.filter(id=job_id),
        'users' : User.objects.filter(plan_job=job_id)
    }
    return render(request, 'view.html', context)

def edit(request, job_id):
    context={
        'job' : Job.objects.get(id=job_id)
    }
    return render(request, 'edit.html', context)

def update(request, job_id):
    job=Job.objects.get(id=job_id)
    job.title=request.POST['title']
    job.description=request.POST['description']
    job.location=request.POST['location']
    job.save()
    return redirect('/dashboard')

def join(request, job_id):
    job=Job.objects.get(id=job_id)
    me=User.objects.get(id=request.session['user_id'])
    job.plan_job.add(me)
    job.save()
    return redirect('/dashboard')

def delete(request, job_id):
    Job.objects.get(id=job_id).delete()
    return redirect('/dashboard')