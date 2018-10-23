from django.contrib import admin
from django.shortcuts import render
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _, gettext_lazy
from django.contrib.auth.models import Group
from django.utils.html import format_html
from import_export.admin import (ExportActionModelAdmin,
                                 ImportExportActionModelAdmin)
from .resources import UserResource, StudentTutionPaymentResource
from django.contrib.auth.admin import UserAdmin

from .models import (Teacher, Student,
                     User, Class, StudentTutionPayment,
                     Session, Subject, Term)
from .utils import intcomma


# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(ExportActionModelAdmin):
    list_display = ['teachers_id',
                    'user_profile_image',
                    'teachers',
                    'user_personal_number',
                    'status'
                    ]
    ordering = ('teachers',)

    # get the profile image from User(AbstarctUser)
    def user_profile_image(self, obj):
        height = 50
        width = 50
        border_radius = 100
        if obj.teachers.profile_image:
            return format_html(f'<img style="height: {height}px;\
                                width: {width}px; \
                                border-radius: {border_radius}%" \
                                src="{obj.teachers.profile_image.url}">')
        else:
            return format_html(f'<img style="height: {height}px; \
                                width: {width}px;\
                                border-radius: {border_radius}%"\
                                src="https://encrypted-tbn0.gstatic.com/\
                                images?\q=tbn:ANd9GcTtAnWXwSHisKlipWhuvSU5\
                                _kXYb7UBejOTZTaHpMTdwlklRrYv">')
    user_profile_image.short_description = 'profile image'

    # oneToone field of user from User get 'username'
    def user_personal_number(self, obj):
            return obj.teachers.phone_number
    user_personal_number.short_description = 'personal number 📞'


@admin.register(Student)
class StudentAdmin(ExportActionModelAdmin):
    list_display = ('students_id',
                    'user_profile_image',
                    'students',
                    'user_personal_number',
                    'parents_or_guidian_number',
                    'class_name',
                    'year_of_reg',
                    )
    list_filter = ('class_name',)
    search_fields = ('user__id', 'user__username')  # search field for students
    date_hierarchy = 'year_of_reg'
    filter_horizontal = ('subjects',)

    # oneToone field of user from User get 'profile image'
    def user_profile_image(self, obj):
        height = 50
        width = 50
        border_radius = 100
        if obj.students.profile_image:
            return format_html(f'<img style="height:{height}px; width:{width}px; \
                               border-radius:{border_radius}%" \
                               src="{obj.students.profile_image.url}">')
        else:
            return format_html(f'<img style="height:{height}px; width:{width}px; \
                               border-radius: {border_radius}%" \
                               src="https://encrypted-tbn0.gstatic.com/\
                               images?q=tbn:ANd9GcTtAnWXwSHisKlipWhuvSU\
                               5_kXYb7UBejOTZTaHpMTdwlklRrYv">')
    user_profile_image.short_description = 'profile image'

    # oneToone field of user from User get 'username'
    def user_personal_number(self, obj):
            return obj.students.phone_number
    user_personal_number.short_description = 'personal number 📞'

@admin.register(StudentTutionPayment)
class studentsTuitionAdmin(ImportExportActionModelAdmin):
    resource_class = StudentTutionPaymentResource

    def school_fees_tag(self, obj):
        if obj.school_fees:
            fees_to_thousands = intcomma(obj.school_fees)
            return format_html(f'₦ { fees_to_thousands }')

    school_fees_tag.short_description = 'School fees'

    def paid_tag(self, obj):
        if obj.paid:
            fees_to_thousands = intcomma(obj.paid)
            return format_html(f'₦ {fees_to_thousands}')

    paid_tag.short_description = 'Amount Paid'

    list_display = ('students_id',
                    'students',
                    'sessions',
                    'class_name',
                    'payment_completed',
                    'school_fees_tag',
                    'paid_tag',
                    'balance'
                    )

    list_per_page = 20
    search_fields = ('students', 'class_name', 'sessions')
    list_filter = ('sessions', 'class_name',)
    show_full_result_count = False
    readonly_fields = ('date_of_payment',)
    ordering = ('students_id',)

    actions = ["payment_completed"]

    def payment_completed(self, request, queryset):
        queryset.update(payment_completed=True)

@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin, UserAdmin):
    resource_class = UserResource

    def profile_image_tag(self, obj):
        height = 50
        width = 50
        border_radius = 100
        if obj.profile_image:
            return format_html(f'<img style="height: {height}px;\
                               width: {width}px;\
                               border-radius: {border_radius}%"\
                               src="{obj.profile_image.url}">')
        else:
            return format_html(f'<img style="height: {height}px;\
                               width: {width}px; \
                               border-radius: {border_radius}%" \
                               src="https://encrypted-tbn0.gstatic.com/\
                               images?q=tbn:ANd9GcTtAnWXwSHisKlipWhuvSU5\
                               _kXYb7UBejOTZTaHpMTdwlklRrYv">')

    profile_image_tag.short_description = 'Profile image'

    list_per_page = 20
    list_display = ('id',
                    'profile_image_tag',
                    'username',
                    'first_name',
                    'last_name',
                    'is_active',
                    'is_superuser',
                    'user_type',
                    'date_joined',
                    )

    search_fields = ('id', 'username', 'first_name', 'last_name')
    list_filter = ('user_type', 'is_active',)
    show_full_result_count = False
    readonly_fields = ('date_joined',)
    ordering = ('id',)

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        ('Personal details', {
            'fields': ('username', 'email', 'password',
                      'first_name', 'last_name', 'date_of_birth',)
        }),
        ('contact details', {
            'fields': ('phone_number', 'residential_address', 'profile_image')
        }),
        ('user permission', {
            'fields':  [('user_type', 'is_active'),
                        ('date_joined', 'last_login'), 'user_permissions']
        }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    actions = ["deactivate_selected_users", "activate_selected_users"]

    # Deactivate selected user
    def deactivate_selected_users(self, request, queryset):
        queryset.update(is_active=False)

    # Activate selected user
    def activate_selected_users(self, request, queryset):
        queryset.update(is_active=True)


admin.site.register(Class, ExportActionModelAdmin)
admin.site.register(Session)
admin.site.register(Term)
admin.site.register(Subject, ExportActionModelAdmin)
admin.site.unregister(Group)

# Disable the 'delete_selected' action
admin.site.disable_action('delete_selected')

AdminSite.site_title = gettext_lazy('Golden Gate School')

# Text to put in each page's <h1>.
AdminSite.site_header = gettext_lazy('Golden Gate School Administration')

# Text to put at the top of the admin index page.
AdminSite.index_title = gettext_lazy('Golden Gate School Administration')
