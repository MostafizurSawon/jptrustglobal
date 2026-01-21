from django.urls import path
from .views import TableView, ClientServiceListView, ClientServiceDetailView, ClientServiceDeleteView, ServiceApplyView, ServiceApplicationListView, ServiceApplicationAdminListView, MyServiceApplyView, ServicePayAdminListView, ServiceApplicationPaymentView, NoticeListView, NoticeCreateView, NoticeUpdateView, NoticeDeleteView, PublicNoticeCreateView, PublicNoticeUpdateView, PublicNoticeDeleteView, EditLatestProgressView, AdminClientPaymentListView, EditClientPaymentView, EditDiscountView, PublicNoticeListView, generate_service_application_pdf
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "tables/basic/",
        login_required(TableView.as_view(template_name="tables_basic.html")),
        name="tables-basic",
    ),
    path(
        "tables/datatables_basic/",
        login_required(TableView.as_view(template_name="tables_datatables_basic.html")),
        name="tables-datatables-basic",
    ),
    path(
        "tables/datatables_advanced/",
        login_required(TableView.as_view(template_name="tables_datatables_advanced.html")),
        name="tables-datatables-advanced",
    ),
    path(
        "tables/datatables_extensions/",
        login_required(TableView.as_view(template_name="tables_datatables_extensions.html")),
        name="tables-datatables-extensions",
    ),
    # path('create-service/', ClientServiceCreateView.as_view(), name='create_service'),


    # Admin view for all applicaion edit/delete
    path("services-all/", login_required(ClientServiceListView.as_view()), name="client_services_list"),
    path('services/<int:pk>/', login_required(ClientServiceDetailView.as_view()), name='client_service_detail'),
    path('services/<int:pk>/delete/', login_required(ClientServiceDeleteView.as_view()), name='client_service_delete'),

    # guest / client
    path('apply/', login_required(ServiceApplyView.as_view()), name='service_apply'),
    path('my-applied/', login_required(MyServiceApplyView.as_view()), name='applied_service_apply'),


    # all applied services by clients
    path('service-applications/', ServiceApplicationListView.as_view(), name='service_application_list'),

    # pdf
    path('dashboard/service-applications/pdf/', generate_service_application_pdf, name='service_application_pdf'),


    # Admin edit service application (admin message and timeline)
    path('service-applications/edit-progress/<int:application_id>/', EditLatestProgressView.as_view(), name='edit_progress'),

    path('service-application-agent-list/', ServiceApplicationAdminListView.as_view(), name='service_application_admin_list'),

    # Admin edit discount
    path('service-applications/edit-discount/<int:application_id>/', EditDiscountView.as_view(), name='edit_discount'),



    # client payment from their id
    path('payment/<int:service_application_id>/', ServiceApplicationPaymentView.as_view(), name='service_application_client_payment'),



    # Admin payment Approval
    path('client-payments/', AdminClientPaymentListView.as_view(), name='admin_client_payment_list'),
    path('client-payments/edit/<int:pk>/', EditClientPaymentView.as_view(), name='admin_client_payment_edit'),






    # demo
    path(
        "office-staff/",
        login_required(TableView.as_view(template_name="hr.html")),
        name="office-staff",
    ),
    path(
        "staff-salary/",
        login_required(TableView.as_view(template_name="hr2.html")),
        name="staff-salary",
    ),
    path(
        "office-role/",
        login_required(TableView.as_view(template_name="hr3.html")),
        name="office-role",
    ),

    path(
        "sms-client/",
        login_required(TableView.as_view(template_name="sms.html")),
        name="sms-client",
    ),
    path(
        "sms-guest/",
        login_required(TableView.as_view(template_name="sms2.html")),
        name="sms-guest",
    ),
    path(
        "sms-client/",
        login_required(TableView.as_view(template_name="sms3.html")),
        name="sms-visitor",
    ),
    path(
        "sms-send/",
        login_required(TableView.as_view(template_name="sms4.html")),
        name="sms-send",
    ),
    path(
        "site/",
        login_required(TableView.as_view(template_name="demo/d1.html")),
        name="site",
    ),
    path(
        "slider/",
        login_required(TableView.as_view(template_name="demo/d2.html")),
        name="slider",
    ),
    path(
        "testimonials/",
        login_required(TableView.as_view(template_name="demo/d3.html")),
        name="testimonials",
    ),
    path(
        "services-fr/",
        login_required(TableView.as_view(template_name="demo/d4.html")),
        name="services-fr",
    ),

    # client view for notice
    path(
        "notice/",
        login_required(NoticeListView.as_view()), name='notice'),
    path(
        "public-notice/",
        login_required(PublicNoticeListView.as_view()), name='public_notice'),

    # admin
    path("notices/create/", login_required(NoticeCreateView.as_view()), name="notice_create"),
    path('notices/edit/<int:pk>/', login_required(NoticeUpdateView.as_view()), name='notice_edit'),
    path('notices/delete/<int:pk>/', login_required(NoticeDeleteView.as_view()), name='notice_delete'),

    # public notice
    path("public-notices/create/", login_required(PublicNoticeCreateView.as_view()), name="public_notice_create"),
    path('public-notices/edit/<int:pk>/', login_required(PublicNoticeUpdateView.as_view()), name='public_notice_edit'),
    path('public-notices/delete/<int:pk>/', login_required(PublicNoticeDeleteView.as_view()), name='public_notice_delete'),


    # demo

    path(
        "support/",
        login_required(TableView.as_view(template_name="demo/e2.html")),
        name="support",
    ),
    path(
        "pay/",
        login_required(TableView.as_view(template_name="demo/e3.html")),
        name="pay_demo",
    ),

    # Expense Demo
    path(
        "expense/",
        login_required(TableView.as_view(template_name="demo/ex.html")),
        name="ex",
    ),
    path(
        "ex2/",
        login_required(TableView.as_view(template_name="demo/ex2.html")),
        name="ex2",
    ),
    path(
        "ex3/",
        login_required(TableView.as_view(template_name="demo/ex3.html")),
        name="ex3",
    ),




    # Admin -> Client Payment
    path(
        "client-payment/",
        login_required(ServicePayAdminListView.as_view()),
        name="client-payment",
    ),
    # path('client-payment/', login_required(ServiceApplicationPaymentView.as_view()), name='service_application_payment'),
    path('client-payment/<int:service_application_id>/', login_required(ServiceApplicationPaymentView.as_view()), name='service_application_payment'),



    path(
        "client-payment2/",
        login_required(TableView.as_view(template_name="sms6.html")),
        name="client-payment2",
    ),
    path(
        "sms-send/",
        login_required(TableView.as_view(template_name="sms7.html")),
        name="client-payment3",
    ),
    path(
        "sms-send/",
        login_required(TableView.as_view(template_name="sms8.html")),
        name="client-payment4",
    ),
]
