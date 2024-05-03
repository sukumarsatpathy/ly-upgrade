from django.urls import path, re_path as url
from . import views


urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Membership Card
    path('membership-card/<int:mid>', views.membershipCard, name='membership-card'),
    path('remove/<int:mid>', views.remove, name='remove'),

    # Visiting Card
    path('visiting-card/<int:mid>', views.visitingCard, name='visiting-card'),
    path('remove-vc/<int:mid>', views.removeVC, name='remove-vc'),

    # Certificate Card
    path('leader-certificate/<int:mid>', views.leaderCertificate, name='leader-certificate'),
    path('remove-clylc/<int:mid>', views.removeCLYLC, name='remove-clylc'),

    path('edit-profile/', views.editProfile, name='edit-profile'),
    url(r'^export-exl/$', views.export, name='export'),
    url(r'^export-csv/$', views.export, name='export'),
    path('work-in-progress/', views.workinProgress, name='work-in-progress'),

    # Self User Creation URL
    path('self-leader-creation/<str:args>/', views.selfLeaderCreation, name='self-leader-creation'),
    path('self-teacher-creation/<str:args>/', views.selfTeacherCreation, name='self-teacher-creation'),

    # New Leader Registration
    path('leaders-registration/', views.LeaderRegistration, name='leaders-registration'),
    path('leaders-registration/charge/', views.charge, name='charge'),
    path('success/<str:args>/', views.successMsg, name='success'),

    # New Teacher Registration
    path('teachers-registration/', views.teacherRegistration, name='teacher-registration'),
    path('teachers-registration/charge/', views.teacherCharge, name='teacher-charge'),
    path('teacher-success/<str:args>/', views.teacherSuccessMsg, name='teacher-success'),

    # Forgot Password
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    # Change Password
    path('change_password/', views.change_password, name='change_password'),

    # User Management
    path('list/', views.userListView, name='userList'), # Read
    path('add/', views.userAddView, name='userAdd'), # Create
    path('view/<int:pk>', views.userView, name='userView'), # View
    path('edit/<int:pk>', views.userEditView, name='userEdit'), # Update
    path('delete/<int:pk>', views.userDeleteView, name='userDelete'), # Delete

]
