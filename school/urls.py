from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from portal.views import index, student, teacher
from django.contrib.auth import views

from rest_framework import routers
from portal.api.views import StudentViewSet, StudentPaymentViewSet

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'student', StudentViewSet)
router.register(r'student_payment', StudentPaymentViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.


urlpatterns = [
    re_path('portal/dashboard/add_update_student/api/', include(router.urls)),
    re_path('portal/dashboard/student_payment/api/', include(router.urls)),

    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls')),
    path('', index.student_count),
    path('about-us/', index.AboutView.as_view(), name="about-us"),
    path('contact-us/', index.ContactView.as_view(), name="contact-us"),

    # Autenticate 3rd party
    path('portal/login/', views.LoginView.as_view(), name='login'),
    path('portal/logout/', views.LogoutView.as_view(), name='logout'),
    path('portal/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('portal/password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('portal/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('portal/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('portal/signup/student/', student.StudentSignUpView.as_view(), name='student_signup'),
    path('portal/signup/teacher/', teacher.TeacherSignUpView.as_view(), name='teacher_signup'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
