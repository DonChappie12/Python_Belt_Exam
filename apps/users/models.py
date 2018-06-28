from django.db import models
import bcrypt
import re
EMAIL_REGEX=re.compile(r"[^@]+@[^@]+\.[^@]+")

class UserManager(models.Manager):
    def validateRegistration(self, postData):
        result={}
        errors=[]
        if len(postData['first_name'])<1:
            errors.append('cannot leave first name field blank')
        if len(postData['last_name'])<1:
            errors.append('cannot leave last name field blank')
        if len(postData['email'])<1:
            errors.append('cannot leave email field blank')
        if len(postData['pw'])<1:
            errors.append('cannot leave password field blank')
        if len(postData['pw'])<7:
            errors.append('password must contain at least 8 characters')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('please enter a valid email')
        if postData['pw'] != postData['cw']:
            errors.append('password dont match')
        if len(User.objects.filter(email=postData['email']))>0:
            errors.append('email already exists')
        if len(errors)>0:
            result['errors']=errors
        else:
            result['user_id']=User.objects.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt()).decode()
            ).id
        return result

    def validateLogin(self, postData):
        result={}
        errors=[]
        existing_user_list=User.objects.filter(email=postData['email'])
        if len(existing_user_list)>0:
            if bcrypt.checkpw(postData['pw'].encode(), existing_user_list[0].password.encode()):
                result['user_id']=existing_user_list[0].id
            else:
                errors.append('Invalid email/password combonation')
        else:
            errors.append('Invalid email/password combonation')
        if len(errors)>0:
            result['errors']=errors
        return result

class JobManager(models.Manager):
    def validateJob(self, postData, user_id):
        errors=[]
        me=User.objects.get(id=user_id)
        if len(postData['title'])<1:
            errors.append('cannot leave title entry empty')
        if len(postData['description'])<1:
            errors.append('cannot leave description entry empty')
        if len(postData['location'])<1:
            errors.append('cannot leave location entry empty')
        if len(errors)==0:
            Job.objects.create(
            title=postData['title'],
            description=postData['description'],
            location=postData['location'],
            created_by=User.objects.get(id=user_id)
            ).plan_job.add(me)
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Job(models.Model):
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_job')
    plan_job=models.ManyToManyField(User, related_name='plan_job')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=JobManager()