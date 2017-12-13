from django.contrib import admin
#from .models import Article
#from app.models import Sys_Button
import app.models as model

class ButtonAdmin(admin.ModelAdmin):
    list_display = ('KeyId', 'FullName', 'DateTime')

admin.site.register(model.Sys_Button,ButtonAdmin)
admin.site.register(model.Sys_Dictionary)
admin.site.register(model.Sys_ErrorLog)
admin.site.register(model.Sys_Menu)
admin.site.register(model.Sys_MenuButton)
admin.site.register(model.Sys_Organization)
admin.site.register(model.Sys_Role)
admin.site.register(model.Sys_RoleMenu)
admin.site.register(model.Sys_RoleMenuButton)
admin.site.register(model.Sys_User)
admin.site.register(model.Sys_UserRole)