from django.urls import path
from . import views

# This app_name variable helps Django distinguish URL names between apps
app_name = 'listings'

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property-detail'),
    path('dashboard/', views.seller_dashboard, name='seller-dashboard'),
    path('add/', views.add_property_view, name='add-property'),
    path('edit/<int:pk>/', views.edit_property_view, name='edit-property'),
    path('delete/<int:pk>/', views.delete_property_view, name='delete-property'),
    path('confirm-delete/<int:pk>/', views.confirm_delete_property_view, name='confirm-delete-property'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('inbox/<int:user_id>/', views.conversation_view, name='conversation-detail'),
    path('buyer_dashboard/', views.property_list, name='property-list'),
    path('property/<int:pk>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('help/', views.help_center_view, name='help-center'),

]
