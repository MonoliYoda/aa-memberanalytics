from django.contrib import admin
from . import tasks
from memberanalytics.models import Owner, CharacterSessionRecord


admin.site.register(Owner)
admin.site.register(CharacterSessionRecord)