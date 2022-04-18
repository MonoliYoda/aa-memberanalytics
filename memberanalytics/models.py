from django.db import models
from eveuniverse.models import EveEntity
from allianceauth.eveonline.models import EveCorporationInfo
from allianceauth.authentication.models import CharacterOwnership
from esi.models import Token
from .providers import esi

# Create your models here.


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)

class CharacterDetails(models.Model):
    character = models.ForeignKey(EveEntity, on_delete=models.CASCADE, help_text="EVE Character")
    joined_corp = models.DateTimeField()
    ship_type_id = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.character.name}"

class CharacterSessionRecord(models.Model):
    character = models.ForeignKey(EveEntity, on_delete=models.CASCADE, help_text="EVE Character")
    location_id = models.IntegerField()
    ship_type_id = models.IntegerField()
    session_start = models.DateTimeField(null=False, default=None, help_text="Time this character last logged on")
    session_end = models.DateTimeField(null=True, default=None, help_text="Time this character last logged off")

    def __str__(self) -> str:
        return f"{self.session_start}"

    def time_logged_on(self) -> int:
        if self.session_end is not None:
            return self.session_end - self.session_start
        else:
            return 0

class Owner(models.Model):
    # pk
    corporation = models.OneToOneField(
        EveCorporationInfo,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="mining_corporation",
    )
    # regular
    character_ownership = models.ForeignKey(
        CharacterOwnership,
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="+",
        help_text="character used to sync this corporation from ESI",
    )

    def fetch_token(self) -> Token:
        """Return valid token for this mining corp or raise exception on any error."""
        if not self.character_ownership:
            raise RuntimeError("This owner has no character configured.")
        token = (
            Token.objects.filter(
                character_id=self.character_ownership.character.character_id
            )
            .require_scopes('esi-corporations.track_members.v1')
            .require_valid()
            .first()
        )
        if not token:
            raise Token.DoesNotExist(f"{self}: No valid token found.")
        return token
    
    def fetch_tracking_data_from_esi(self):
        members = esi.client.Corporation.get_corporations_corporation_id_membertracking(
            corporation_id=self.corporation.corporation_id,
            token=self.fetch_token().valid_access_token()
        ).results()
        print(len(members))
        for member in members:
            print(member['character_id'])

