from django.urls import path
from .views import SampleView
from .views import DashboardsView, ServiceApplyViewDashboard, ExpenseDashboardView, ExpenseCategoryView, ExpenseCategoryView, ExpenseListView,generate_expense_pdf
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # path(
    #     "",
    #     SampleView.as_view(template_name="index.html"),
    #     name="index",
    # ),
    # path(
    #     "",
    #     login_required(DashboardsView.as_view(template_name="dashboard_crm.html")),
    #     name="index",
    # ),
    path(
        "",
        login_required(ServiceApplyViewDashboard.as_view()),
        name="index",
    ),
    path(
        "page_2/",
        SampleView.as_view(template_name="page_2.html"),
        name="page-2",
    ),


    path("expenses/all/", ExpenseListView.as_view(), name="expense_list"),

    # edit
    path("expenses/all/edit/<int:pk>/", ExpenseListView.as_view(), name="edit_expense"),


    # pdf
    path("dashboard/expenses/pdf/", generate_expense_pdf, name="expense_pdf"),


    path('expenses/create/', ExpenseDashboardView.as_view(), name='create_expense'),

    path('expenses/edit/<int:pk>/', ExpenseDashboardView.as_view(), name='edit_expense'),

    # category
    path("expenses/categories/", ExpenseCategoryView.as_view(), name="expense_category_list"),
    path("expenses/categories/edit/<int:pk>/", ExpenseCategoryView.as_view(), name="expense_category_edit"),



]
