from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileUpdateForm, UserRegisterUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    # register user
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hello {username} you created an account! \n You are able to log in')
            form.save()
            return redirect('informations-home')
    else:
        form = UserRegisterForm()
    return render(request, 'register_user_form.html', {'form_register_user': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form_register = UserRegisterUpdateForm(request.POST, instance=request.user)
        # allows to add files
        form_profile = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form_register.is_valid() and form_profile.is_valid():
            # joins two forms
            username = form_register.cleaned_data.get('username')
            form_register.save()
            form_profile.save()
            messages.success(request, f'{username} you updated an account!')
            return redirect('informations-home')
    else:
        form_register = UserRegisterUpdateForm(instance=request.user)
        form_profile = UserProfileUpdateForm(instance=request.user.profile)

    context = {
        'form_register': form_register,
        'form_profile': form_profile
    }
    return render(request, 'profile.html', context)
