from django.shortcuts import render
from rest_framework import viewsets
from portal.models import Student, StudentTutionPayment
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from portal.api.serializers import StudentSerializer, StudentTutionPaymentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the s.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentPaymentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the states.
    """
    queryset = StudentTutionPayment.objects.all()
    serializer_class = StudentTutionPaymentSerializer

