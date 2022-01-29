from django.contrib import admin
from .models import Todo,Qbank,Question,Python_Test_Status

class TodoAdmin(admin.ModelAdmin):
    readonly_fields=('created',)

admin.site.register(Todo,TodoAdmin)
admin.site.register(Qbank)
admin.site.register(Question)
admin.site.register(Python_Test_Status)
