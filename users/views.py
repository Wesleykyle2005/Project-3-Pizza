from django.shortcuts import render
from .forms import RegistrationForm

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html', {'user': user})
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})

