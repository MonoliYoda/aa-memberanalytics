from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls


class MemberAnalyticsMenu(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""
    def __init__(self):
        MenuItemHook.__init__(
            self,
            _("Member Analytics"),
            "fas fa-chart-bar fa-fw",
            "memberanalytics:index",
            navactive=["memberanalytics:"],
        )

    def render(self, request):
        if request.user.has_perm("memberanalytics.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return MemberAnalyticsMenu()


@hooks.register("url_hook")
def register_url():
    return UrlHook(urls, "memberanalytics", r"^memberanalytics/")

