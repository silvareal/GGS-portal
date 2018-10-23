from import_export import resources
from import_export.widgets import (ForeignKeyWidget,
                                   BooleanWidget,
                                   IntegerWidget)
from import_export import fields

from .models import (User,
                     Student,
                     Class,
                     Session)


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = (
                  'user_permissions',
                  'is_superuser',
                  'profile_image',
                  'height_field',
                  'width_field',
                  'is_staff',
                  'is_active',
                  'date_joined'
                  'is_superuser',
                  'groups',
                  'last_login',
                  )

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student


class StudentTutionPaymentResource(resources.ModelResource):
    students = fields.Field(
        column_name='students',
        attribute='students',
        widget=ForeignKeyWidget(Student, 'students'))

    sessions = fields.Field(
        column_name='sessions',
        attribute='sessions',
        widget=ForeignKeyWidget(Session, 'name'))

    class_name = fields.Field(
        column_name='class_name',
        attribute='class_name',
        widget=ForeignKeyWidget(Class, 'name'))

    payment_completed = fields.Field(
        column_name='payment_completed',
        attribute='payment_completed',
        widget=BooleanWidget())

    school_fees = fields.Field(
        column_name='school_fees',
        attribute='school_fees',
        widget=IntegerWidget())

    total_payment = fields.Field(
        column_name='paid',
        attribute='paid',
        widget=IntegerWidget())
