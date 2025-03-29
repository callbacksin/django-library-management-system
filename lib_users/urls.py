from django.urls import path
from .views import (
    ProfileViewFilter,
    AdminUserDetailView,
    create_profile,
    create_group,
    assign_book_instance,
    update_profile_without_password,
    update_user_password_only,
    delete_profile,
    unassign_book_instance,
    user_books,
)

urlpatterns = [
    path('', ProfileViewFilter.as_view(), name='students'),
    path('concrete/<pk>', AdminUserDetailView.as_view(), name='concrete'),
    path('create-user/', create_profile, name='create_profile'),
    path('update-user/<pk>', update_profile_without_password, name='update_profile'),
    path('update-user-password/<pk>', update_user_password_only, name='update_password_only'),
    path('delete-user/<pk>', delete_profile, name='delete_profile'),
    path('create-group/', create_group, name='create_group'),
    path('assign-item/<pk>', assign_book_instance, name='assign_item'),
    path('unassign-item/<pk>', unassign_book_instance, name='unassign_item'),
    path('my-books/', user_books, name='user_books'),
]
