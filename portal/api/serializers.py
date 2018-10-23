from rest_framework import serializers
from portal.models import Student, User, Class, Teacher, Session, StudentTutionPayment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('profile_image', 'username', 'first_name', 'last_name', 'phone_number',)


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    teachers = UserSerializer(required=True)

    class Meta:
        model = Teacher
        fields = ('teachers', 'title', 'status')

class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ('sessions',)


class ClassSerializer(serializers.HyperlinkedModelSerializer):
    teachers = TeacherSerializer(required=True)
    sessions = SessionSerializer()

    class Meta:

        model = Class
        fields = ('class_name', 'teachers', 'sessions')


class StudentSerializer(serializers.ModelSerializer):
    students = UserSerializer(required=True)
    class_name = ClassSerializer()

    class Meta:
        model = Student
        fields = ('students', 'parents_or_guidian_number', 'class_name', 'year_of_reg')


class StudentTutionPaymentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(required=True)
    sessions = SessionSerializer()
    class_name = ClassSerializer()

    class Meta:
        model = StudentTutionPayment
        fields = ('students', 'sessions',
                  'class_name', 'payment_completed',
                  'school_fees', 'paid',
                  'balance', 'date_of_payment',)
