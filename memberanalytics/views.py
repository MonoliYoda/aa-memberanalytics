from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseNotFound
from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCorporationInfo
from eveuniverse.models import EveEntity
from esi.decorators import token_required
from .models import Owner, CharacterSessionRecord, CharacterDetails
from . import tasks
from .managers import ExtendedTS3Manager


@login_required
@permission_required("memberanalytics.basic_access")
def index(request):
    characters = CharacterDetails.objects.all()
    ts3 = ExtendedTS3Manager()
    ts3.show_server()

    context = {"characters": characters}
    return render(request, "memberanalytics/index.html", context)


@login_required
@permission_required("memberanalytics.basic_access")
def member_details(request, id):
    character = EveEntity.objects.get(id=id)
    sessions = CharacterSessionRecord.objects.filter(character=character)
    avg_session_length = 0
    context = {"sessions": sessions, "character": character}
    return render(request, "memberanalytics/member_details.html", context)


@login_required
@permission_required("memberanalytics.basic_access")
@token_required(scopes='esi-corporations.track_members.v1')
def add_owner(request, token):
    try:
        character_ownership = request.user.character_ownerships.select_related(
            "character"
        ).get(character__character_id=token.character_id)
    except CharacterOwnership.DoesNotExist:
        return HttpResponseNotFound()
    try:
        corporation = EveCorporationInfo.objects.get(
            corporation_id=character_ownership.character.corporation_id
        )
    except EveCorporationInfo.DoesNotExist:
        corporation = EveCorporationInfo.objects.create_corporation(
            corp_id=character_ownership.character.corporation_id
        )
        corporation.save()

    owner, _ = Owner.objects.update_or_create(
        corporation=corporation,
        defaults={"character_ownership": character_ownership},
    )
    tasks.update_all_from_esi()
    #tasks.update_owner(owner.pk)
    # Messages and notifications here
    return redirect("memberanalytics:index")