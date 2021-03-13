from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.views.generic import UpdateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully")
            return redirect('login')
        else:
            print("Form Invalid")
            print(form.errors)
    else:
        form=UserRegistrationForm()
    return render(request,'users/register.html',{"form":form})

# Used Update view from django.views.generic to handle update operations of Profile model
# Mixins are available in django.contrib.auth.mixins 
# LoginRequiredMixin is used when it is necessary to be Logged In before a particular task
# UserPassesTestMixin is used to validate a condition.This condition is mentioned in test_func function and the view is called only if function returns True

class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Profile
    fields=['image','location','title','contact']
    success_url='/'                         #Redirect to this URL after successfully updating the model
    template_name='users/profile.html'
    context_object_name='profile'

    def test_func(self):                    #If the profile is of the same user that is logged in
        profile=self.get_object()
        print(profile.user,self.request.user)
        if profile.user == self.request.user:
            return True
        return False

