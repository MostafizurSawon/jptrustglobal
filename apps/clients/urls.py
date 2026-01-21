from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.clients.transaction_list.views import TransactionListView
from apps.clients.transaction_add.views import TransactionAddView
from apps.clients.transaction_update.views import TransactionUpdateView
from apps.clients.transaction_delete.views import TransactionDeleteView
from .views import AllGuestCvView, GuestCVDetailView, GuestCVEditView, AllClientCvView, AllClientPassportView, PassportInfoDetailView, PassportInfoEditView, PassportInfoByUserView, ClientPaymentListView, ClientPaymentDetailView, ApplicationStatusListView, PaymentInvoiceView, PaymentInvoiceSearchView, DeleteGuestCvView, ClientCVDeleteView, PassportDeleteView, PassportInfoEditAdminView, GuestCVDetailView2, CustomerSupportCreateView, CustomerSupportListView, CustomerSupportDetailView, SupportChatView, AdminSupportListView, AdminSupportChatView, update_status, AdminSupportEditView, AdminSupportDeleteView

urlpatterns = [

    path(
        "my-payment/services/list",
        login_required(ClientPaymentListView.as_view()),
        name="client_payment_list",
    ),

    path('my-payment/invoice/<int:payment_id>/', PaymentInvoiceView.as_view(), name='payment_invoice'),
    # path('my-payment/services/list/<int:pk>/', ClientPaymentDetailView.as_view(), name='client_payment_detail'),

    path(
        "services/application-status/",
        login_required(ApplicationStatusListView.as_view()),
        name="client_application_status",
    ),

    # invoice search from QR code
    path('invoice/search/', PaymentInvoiceSearchView.as_view(), name='invoice_search'),



    path(
        "transactions/list/",
        login_required(TransactionListView.as_view(template_name="transactions_list.html")),
        name="transactions",
    ),
    path(
        "transactions/add/",
        login_required(TransactionAddView.as_view(template_name="transactions_add.html")),
        name="transactions-add",
    ),
    path (
        "transactions/update/<int:pk>",
        login_required(TransactionUpdateView.as_view(template_name="transactions_update.html")),
        name="transactions-update",
    ),
    path (
        "transactions/delete/<int:pk>/",
        login_required(TransactionDeleteView.as_view()),
        name="transactions-delete",
    ),
    path(
        "client-cv/list/",
        login_required(AllClientCvView.as_view()),
        name="client_cv_list",
    ),
    path('guest-cv/delete/<int:pk>/', ClientCVDeleteView.as_view(), name='client_cv_delete'),

    path(
        "client-passport/list/",
        login_required(AllClientPassportView.as_view()),
        name="client_passport_list",
    ),
    path('passport/delete/<int:pk>/', PassportDeleteView.as_view(), name='passport_delete'),
    path('passport/<int:pk>/edit/', PassportInfoEditAdminView.as_view(), name='passport_info_edit_admin'),




    path('client-passport/list/<int:user_id>/', PassportInfoByUserView.as_view(), name='passport_info_detail_by_user'),


    path('passport-info-detail/<int:pk>/', login_required(PassportInfoDetailView.as_view()), name='passport_info_detail'),  # View passport info
    path('passport-info-edit/<int:pk>/', login_required(PassportInfoEditView.as_view()), name='passport_info_edit'),  # Edit passport info

    path(
        "guest-cv/list/",
        login_required(AllGuestCvView.as_view()),
        name="guest_cv_list",
    ),
    path('guest-cv/delete/<int:pk>/', DeleteGuestCvView.as_view(), name='guest_cv_delete'),



    path('guest-cvs/<int:pk>/', login_required(GuestCVDetailView.as_view()), name='guest_cv_detail'),
    path('guest-cvs2/<int:pk>/', login_required(GuestCVDetailView2.as_view()), name='guest_cv_detail2'),
    path('guest-cvs/<int:pk>/edit/', login_required(GuestCVEditView.as_view()), name='guest_cv_edit'),



    # Client Support
    path('support/create/', CustomerSupportCreateView.as_view(), name='support_create'),
    path('support/my-requests/', CustomerSupportListView.as_view(), name='support_list'),
    path('support/<int:pk>/detail/', CustomerSupportDetailView.as_view(), name='support_detail'),

    path('support/<int:pk>/chat/', SupportChatView.as_view(), name='support_chat'),


    # Admin part
    path('admin/support/', AdminSupportListView.as_view(), name='admin_support_list'),
    path('admin/support/<int:pk>/delete/', AdminSupportDeleteView.as_view(), name='admin_support_delete'),
    path('admin/support/<int:pk>/status/<str:status>/', update_status, name='admin_update_status'),

    path('admin/support/<int:pk>/chat/', AdminSupportChatView.as_view(), name='admin_support_chat'),

    path('admin/support/<int:pk>/edit/', AdminSupportEditView.as_view(), name='admin_support_edit'),




]
