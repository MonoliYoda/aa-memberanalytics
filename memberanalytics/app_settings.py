from django.conf import settings

AA_MEMBERANALYTICS_ENABLE_ESI_STATS = getattr(settings, 'AA_MEMBERANALYTICS_ENABLE_ESI_STATS', True)
AA_MEMBERANALYTICS_ENABLE_TS3_STATS = getattr(settings, 'AA_MEMBERANALYTICS_ENABLE_TS3_STATS', True)

