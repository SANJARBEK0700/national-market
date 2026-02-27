from django.shortcuts import render



from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django import forms

from .forms import RegisterForm, ProfileUpdateForm
from .models import User
from .utils import send_otp_email

from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)

        user.is_active = False
        user.save()

        user.generate_otp()
        send_otp_email(user)

        self.request.session["verify_user_id"] = user.id

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("verify_otp")




from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages


class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True  # login bo‘lgan user qayta login sahifaga kira olmaydi


    def form_valid(self, form):
        messages.success(self.request, "Xush kelibsiz!")
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy("index")

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profilingiz muvaffaqiyatli yangilandi!")
        return super().form_valid(form)


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class VerifyOTPView(FormView):
    template_name = "users/verify_otp.html"
    form_class = OTPForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user_id = self.request.session.get("verify_user_id")
        user = get_object_or_404(User, id=user_id)

        if user.otp_code == form.cleaned_data["otp"]:
            user.is_active = True
            user.is_verified = True
            user.otp_code = ""
            user.save()

            login(self.request, user)
            messages.success(self.request, "Account verified!")

            return super().form_valid(form)

        messages.error(self.request, "OTP noto‘g‘ri")
        return redirect("verify_otp")