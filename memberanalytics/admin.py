from django.contrib import admin
from . import tasks
from memberanalytics.models import Owner, CharacterSessionRecord, CharacterDetails


admin.site.register(Owner)
#admin.site.register(CharacterSessionRecord)
admin.site.register(CharacterDetails)

@admin.register(CharacterSessionRecord)
class SessionRecordAdmin(admin.ModelAdmin):
    list_display = ("character", "session_start", "session_end")