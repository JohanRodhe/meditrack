from django.contrib import messages
from django.shortcuts import redirect, render
from accounts.forms import UserRegisterForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! You are now able to log in"
            )
            return redirect("login")
        else:
            form = UserRegisterForm()
            return render(request, "accounts/register.html", {"form": form})

    else:
        form = UserRegisterForm()
        return render(request, "accounts/register.html", {"form": form})