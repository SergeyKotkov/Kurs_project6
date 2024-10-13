from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserManagerForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verification')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            send_mail(
                subject='Подтверждение почты',
                message=f'Код {new_user.ver_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)


class VerificationView(TemplateView):
    template_name = 'users/send_mail_code.html'

    def post(self, request):
        ver_code = request.POST.get('ver_code')
        user_code = User.objects.filter(ver_code=ver_code).first()

        if user_code is not None and user_code.ver_code == ver_code:
            user_code.is_active = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:verification_email_error')


class ErrorVerification(TemplateView):
    template_name = 'users/verification_email_error.html'
    success_url = reverse_lazy('users:send_mail_code')


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailing:index')

    def get_object(self, queryset=None):
        return self.request.user


class UserManagerProfileView(UpdateView):
    model = User
    form_class = UserManagerForm
    template_name = 'users/manager_profile.html'
    success_url = reverse_lazy('users:users_list')


class UserManagerListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'objects_list'