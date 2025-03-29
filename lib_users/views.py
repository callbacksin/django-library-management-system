from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import DetailView
from django_filters.views import FilterView

from core.models import Item, ItemHistory
from .filters import ProfileFilter
from .forms import (UserForm, GroupForm, AssignBookInstanceForm,
                    UserFormWithoutPassword, ProfileForm, CustomSetPasswordForm, )
from .models import Profile


class ProfileViewFilter(FilterView):
    model = Profile
    paginate_by = 10
    template_name = "lib_users/students.html"
    filterset_class = ProfileFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProfileFilter(
            self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


class AdminUserDetailView(DetailView):
    model = User
    template_name = "lib_users/concrete_student.html"


class UserDetailView(DetailView):
    model = User
    template_name = "lib_users/user_books.html"


def user_books(request):
    return render(request, 'lib_users/user_books.html')


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def create_group(request):
    if request.method == 'POST':
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            messages.info(request, 'Group successfully created')
            return redirect('students')
        else:
            messages.info(request, 'Please correct the errors')
    else:
        group_form = GroupForm()
    return render(request, 'lib_users/create_group.html',
                  {'group_form': group_form, })


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def create_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            patronymic = user_form.cleaned_data.get('patronymic')
            birth_date = user_form.cleaned_data.get('birth_date')
            academy_group = user_form.cleaned_data.get('academy_group')
            Profile.objects.create(
                user=user,
                academy_group=academy_group,
                birth_date=birth_date,
                patronymic=patronymic,
            )
            messages.success(request, 'Profile was successfully created')
            return redirect('students')
        else:
            messages.info(request, 'Please correct the errors')
    else:
        user_form = UserForm()
    return render(request, 'lib_users/create_profile.html',
                  {'user_form': user_form, })


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def update_profile_without_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(Profile, user=user.pk)
    if request.method == "POST":
        user_form = UserFormWithoutPassword(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile was successfully updated')
            return redirect('students')
        else:
            messages.info(request, 'Please correct the errors')
    else:
        user_form = UserFormWithoutPassword(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'lib_users/update_profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def update_user_password_only(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Password for user {user.username} has been successfully changed')
            return redirect('core:operate')
        else:
            messages.info(request, 'Please correct the errors')
    else:
        form = CustomSetPasswordForm(user)
    return render(request, "lib_users/update_password.html",
                  {'form': form})


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def delete_profile(request, pk):
    user = User.objects.filter(pk=pk).get()
    last_name = user.last_name
    first_name = user.first_name
    if request.method == 'POST':
        if not Item.objects.filter(borrower=user):
            user.delete()
            messages.success(
                request,
                f'Profile of user {last_name} {first_name} was successfully deleted')
        else:
            messages.info(
                request,
                f'''User {last_name} {first_name} has books assigned to them.
                 These must be "unassigned" first.''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def assign_book_instance(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        book_instance_form = AssignBookInstanceForm(request.POST)
        book_instance_form.is_valid()
        book_instance = book_instance_form.cleaned_data.get(
            'inventory_number')
        if not book_instance:
            book_instance_qr = book_instance_form.cleaned_data.get('inventory')
            book_instance = Item.objects.filter(
                qr_code=book_instance_qr)
        if book_instance:
            if book_instance.status == 'A':
                messages.warning(
                    request,
                    'This book instance is already assigned to another user.')
            else:
                book_instance.operator = request.user
                book_instance.due_back = book_instance_form.cleaned_data.get(
                    'due_back')
                book_instance.borrower = user
                book_instance.status = 'A'
                book_instance.save()
                book_instance.book.free_quantity -= 1
                book_instance.book.save()
                messages.info(
                    request,
                    f'Book instance {book_instance.book.title} successfully assigned to user {user.last_name} {user.first_name}')
        else:
            messages.warning(request,
                             'Book instance with this inventory number not found')
    book_instance_form = AssignBookInstanceForm()
    return render(request, 'lib_users/assign_book_instance.html',
                  {'book_instance_form': book_instance_form, })


@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def unassign_book_instance(request, pk):
    book_instance = get_object_or_404(Item, pk=pk)
    inventory = book_instance.inventory_number
    if request.method == 'POST':
        ItemHistory.objects.create(
            item=book_instance,
            operator=book_instance.operator,
            inventory_number=book_instance.inventory_number,
            book=book_instance.book,
            status='H',
            due_back=datetime.now(),
            borrower=book_instance.borrower,
        )
        book_instance.borrower = None
        book_instance.due_back = None
        book_instance.status = 'F'
        book_instance.save()
        book_instance.book.free_quantity += 1
        book_instance.book.save()
        messages.info(
            request,
            f'Book instance with inventory number {inventory} successfully unassigned'
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
