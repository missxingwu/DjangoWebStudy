from django.contrib import admin
#from .models import Article
#from app.models import Sys_Button
import app.models as model

class ButtonAdmin(admin.ModelAdmin):
    list_display = ('KeyId', 'FullName', 'DateTime')

admin.site.register(model.Sys_Button,ButtonAdmin)