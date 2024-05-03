from django.contrib import admin
from .models import AccountToken, LeaderUniqueToken, TeacherUniqueToken


admin.site.register(AccountToken)
admin.site.register(LeaderUniqueToken)
admin.site.register(TeacherUniqueToken)