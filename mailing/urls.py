from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import MailingConfig
from .views import MailingListView, MailingCreateView, ClientCreateView, MailingUpdateView, \
    MailingDeleteView, MailingDetailView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    IndexListView, MailingLogListView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_detail/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('mailing_log_list/', MailingLogListView.as_view(), name='mailing_log_list'),
    ]