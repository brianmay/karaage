# Copyright 2007-2014 VPAC
#
# This file is part of Karaage.
#
# Karaage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage  If not, see <http://www.gnu.org/licenses/>.
import django_tables2 as tables
from django_tables2.columns.linkcolumn import BaseLinkColumn
from django_tables2.utils import A

import django_filters

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import Person, Group


class PeopleColumn(BaseLinkColumn):
    def render(self, value):
        people = []
        for person in value.all():
            url = reverse("kg_person_detail", args=[person.username])
            link = self.render_link(url, text=unicode(person))
            people.append(link)
        return mark_safe(", ".join(people))


class PersonFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_type="icontains")
    full_name = django_filters.CharFilter(lookup_type="icontains")
    email = django_filters.CharFilter(lookup_type="icontains")
    no_last_usage = django_filters.BooleanFilter(name="last_usage__isnull")
    begin_last_usage = django_filters.DateFilter(
        name="last_usage", lookup_type="gte")
    end_last_usage = django_filters.DateFilter(
        name="last_usage", lookup_type="lte")
    begin_date_approved = django_filters.DateFilter(
        name="date_approved", lookup_type="gte")
    end_date_approved = django_filters.DateFilter(
        name="date_approved", lookup_type="lte")

    class Meta:
        model = Person
        fields = ("username", "full_name", "email", "institute",
                  "is_active", "is_admin", "login_enabled")


class PersonTable(tables.Table):
    username = tables.LinkColumn(
        'kg_person_detail', args=[A('username')])
    institute = tables.LinkColumn(
        'kg_institute_detail', args=[A('institute.pk')])

    class Meta:
        model = Person
        fields = ("username", "full_name", "institute",
                  "is_active", "is_admin", "last_usage", "date_approved")


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type="icontains")
    description = django_filters.CharFilter(lookup_type="icontains")

    class Meta:
        model = Group
        fields = ("name", "description")


class GroupTable(tables.Table):
    name = tables.LinkColumn(
        'kg_group_detail', args=[A('name')])
    members = PeopleColumn(orderable=False)

    class Meta:
        model = Group
        fields = ("name", "description")
