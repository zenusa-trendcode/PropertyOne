from django.urls import path

from . import views

app_name = 'pms'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('maintenance/<int:pk>/transition/<str:status>/', views.WorkOrderTransitionView.as_view(), name='work_order_transition'),
    path('<str:module>/', views.ModuleListView.as_view(), name='module_list'),
    path('<str:module>/new/', views.ModuleCreateView.as_view(), name='module_create'),
    path('<str:module>/<int:pk>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('<str:module>/<int:pk>/edit/', views.ModuleUpdateView.as_view(), name='module_update'),
]
