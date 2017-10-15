__author__ = 'tintin'

from service.pocket.pocketservice import pocketService


class ServiceManager:
    global pocketservice

    pocketservice = pocketService()

    def getPocketServiceInstance(self):
        return pocketservice