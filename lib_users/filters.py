import django_filters

from .models import Group, Profile


class ProfileFilter(django_filters.FilterSet):
    user__last_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='By surname'
    )
    academy_group = django_filters.ModelChoiceFilter(
        empty_label='---Choose a group---',
        queryset=Group.objects.all(),
        label='By group'
    )

    class Meta:
        model = Profile
        fields = ['user__last_name', 'academy_group']
        ordering = ['-id']
