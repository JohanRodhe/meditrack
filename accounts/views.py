from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from accounts.forms import UserRegisterForm
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
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
        

class CustomLoginView(LoginView):
    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        response = super().form_valid(form)
        if self.request.headers.get('HX-Request') == 'true':
            response = HttpResponseRedirect(self.get_success_url())
            response['HX-Redirect'] = 'true'
        return response