from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from school import settings

from django.db import models
from .utils import (upload_location,
                    phone_regex,
                    school_session_regex,
					intcomma
                    )


# uplaod image to the media location
class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,
                                                 blank=True,
                                                 null=True
                                                 )  # user type
    date_of_birth = models.DateField(blank=True,  null=True)
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=11,
                                    blank=True
                                    )  # validators should be a list
    residential_address = models.CharField(max_length=100,  blank=True)
    profile_image = models.ImageField(upload_to=upload_location,
                                      blank=True,
                                      default='test.png',
                                      height_field='height_field',
                                      width_field='width_field',
                                      )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Users"

class Teacher(models.Model):
    teachers = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    TITLE_CHOICES = (
      ('MR', 'Mr'),
      ('MRS', 'Mrs'),
      ('MISS', 'Miss'),
    )
    title = models.CharField(max_length=4, choices=TITLE_CHOICES)

    STATUS_CHOICES = (
      ('SINGLE', 'Single'),
      ('MARRIED', 'Married'),
    )
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)

    class Meta:
        verbose_name_plural = "Teachers"

    def __str__(self):
        return f'{self.title} {self.teachers}'


class Session(models.Model):
    sessions = models.CharField(validators=[school_session_regex],
                            max_length=9,
                            help_text="use the following format: \
                                       <em>YYYY/YYY</em>. eg(2017/2018)"
                            )  # validators should be a list

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        return self.sessions


class Term(models.Model):
    terms = models.CharField(max_length=20)
    sessions = models.ForeignKey('Session', on_delete=models.CASCADE,)

    class Meta:
        verbose_name = "Term"
        verbose_name_plural = "Terms"

    def __str__(self):
        return f'{self.term}({self.sessions})'


class Class(models.Model):
    class_name = models.CharField(max_length=20)
    teachers = models.OneToOneField(Teacher, models.SET_NULL, null=True)
    sessions = models.ForeignKey('Session',
                                models.SET_NULL,
                                null=True,)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return f'{self.class_name}({self.sessions})'


class Subject(models.Model):
    subjects = models.CharField(max_length=20)
    teachers = models.ForeignKey('Teacher',
                                models.SET_NULL,
                                null=True,
                                )

    class Meta:
        verbose_name_plural = "subjectss"

    def __str__(self):
        return self.subjects


class Student(models.Model):
    students = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    parents_or_guidian_number = models.CharField(validators=[phone_regex],
                                                 max_length=11)
    class_name = models.ForeignKey('Class',
                                 models.SET_NULL,
                                 null=True,
                                 )
    subjects = models.ManyToManyField(Subject)
    year_of_reg = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Students"

    def __str__(self):
        return str(self.students)


class StudentTutionPayment(models.Model):
    students = models.ForeignKey('Student', on_delete=models.CASCADE)
    sessions = models.ForeignKey('Session', on_delete=models.CASCADE)
    class_name = models.ForeignKey('Class', on_delete=models.CASCADE)
    payment_completed = models.BooleanField(default=False)
    school_fees = models.IntegerField(help_text="Input the tuition fees")
    paid = models.IntegerField(help_text="Input the amount paid")
    date_of_payment = models.DateField(auto_now_add=True)

    def _get_balance(self):  # "Calculated" balance field
        fees = self.school_fees
        paid_amount = self.paid
        get_balance = intcomma(fees - paid_amount)
        return f'₦ {get_balance}.00'  # returns the balance

    balance = property(_get_balance)

    class Meta:
        verbose_name_plural = "StudentTutionPayments"

    def __str__(self):
        return f'{self.students} + ({self.sessions})=> {self.payment_completed}'


# create student signal 'to save the User.user_type instance as 1'
@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        instance.students.user_type = 1  # create instance of student choice 1


@receiver(post_save, sender=Student)
def save_student_profile(sender, instance, **kwargs):
    instance.students.save()  # save the instance of Student choice (1, 'Student')


# create teacher signal 'to save the User.user_type instance as 2'
@receiver(post_save, sender=Teacher)
def create_Teacher_profile(sender, instance, created, **kwargs):
    if created:
        instance.teachers.user_type = 2  # create instance of Teacher choice 2


@receiver(post_save, sender=Teacher)
def save_Teacher_profile(sender, instance, **kwargs):
    instance.teachers.save()  # save the instance of Teacher choice (2, 'Teacher')
