from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect
import random
from blogs.models import Blog
from mailing.forms import MailingForm, ClientForm, MailingUpdateForm, MailingManagerUpdateForm
from mailing.models import Mailing, Client, MailingLog
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

from mailing.services import mail_status_change


def mailing_start():
    return call_command('mailing_start')


scheduler = BackgroundScheduler()
scheduler.add_job(mailing_start, 'interval', seconds=600)
scheduler.add_job(mail_status_change, 'interval', seconds=3600)
scheduler.start()


class IndexListView(ListView):
    model = Blog
    template_name = 'mailing/index.html'
    context_object_name = 'objects_list'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings_count = len(Mailing.objects.all())
        mailings_is_active_count = len(Mailing.objects.filter(is_active=True))
        unique_clients_count = Client.objects.values('email').distinct().count()
        context['mailings_count'] = mailings_count
        context['mailings_is_active_count'] = mailings_is_active_count
        context['unique_clients_count'] = unique_clients_count
        return context


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'objects_list'


class MailingCreateView(PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.add_mailing'

    def get(self, request, **kwargs):
        form = self.form_class(self.request.user, request.POST)
        context = {'form': form}
        return render(request, 'mailing/mailing_form.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            clients = form.cleaned_data.get('clients')
            if not clients:
                form.add_error('clients', 'Выберите хотя бы одного клиента.')
            mailing = form.save(commit=False)
            mailing.user = self.request.user
            mailing.save()
            form.save_m2m()
            return redirect(self.success_url)


class MailingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingUpdateForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.change_mailing'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        if self.request.user.groups.filter(name='manager').exists():
            return MailingManagerUpdateForm
        else:
            return MailingUpdateForm


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'


class MailingDeleteView(PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.delete_mailing'


class ClientCreateView(PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    permission_required = 'mailing.add_client'

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.user = user
        client.save()
        return super().form_valid(form)


class ClientListView(PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'objects_list'
    permission_required = 'mailing.view_client'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'


class ClientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    context_object_name = 'objects_list'
    success_url = reverse_lazy('mailing:client_list')
    permission_required = 'mailing.change_client'


class ClientDeleteView(PermissionRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_delete.html'
    success_url = reverse_lazy('mailing:client_list')
    permission_required = 'mailing.delete_client'


class MailingLogListView(ListView):
    model = MailingLog
    template_name = 'mailing/mailing_log_list.html'
    context_object_name = 'objects_list'