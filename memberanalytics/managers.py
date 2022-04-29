from allianceauth.services.modules.teamspeak3.manager import Teamspeak3Manager

class ExtendedTS3Manager(Teamspeak3Manager):
    def show_server(self):
        print(self.connect())