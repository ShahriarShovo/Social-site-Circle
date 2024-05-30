from django.shortcuts import render, redirect,get_object_or_404
from a_users.forms import Profileform
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse

# Create your views here.
@login_required
def profile_view(request, username=None):
    if username:
        profile= get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    
    context={
        'profile':profile
    }
    return render(request,'a_users/profile.html', context)

@login_required
def profile_edit(request):
    
    form = Profileform(instance=request.user.profile)
    
    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        template= 'a_users/profile_onboarding.html'
    else:
        template='a_users/profile_edit.html'
        
    return render(request, template, {'form':form,})



@login_required
def profile_delete_view(request):
    user=request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('index')
        
        
    return render(request, 'a_users/profile_delete.html')
