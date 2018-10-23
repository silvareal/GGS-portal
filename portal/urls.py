from django.urls import path, include

from .views import index

app_name = 'portal'

urlpatterns = [
    path('signup/', index.PortalIndex.as_view(), name='portal-index'),

    #portal urls
    path('dashboard/', index.dashboard, name='portal-dashboard'),
    path('dashboard/add_update_student/', index.add_update, name='portal-dashboard-add'),
    path('dashboard/student_payment/', index.student_payment, name='portal-student-payment'),
    path('dashboard/Send_mail/', index.send_mail_to, name='portal-dashboard-mail'),
    #End portal Url
]
