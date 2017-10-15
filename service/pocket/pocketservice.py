__author__ = 'tintin'
import requests
import json
from manager.Manager import Manager
from service.pocket.tasks import fetchandsavepage
import pdb
#pdb.set_trace()

class pocketService :

    def __init__(self, redirect_fn):
        self.index = "http://localhost:8000/index"
        self.username = None
        self.database = Manager.getDatabaseInstance()
        self.redirect_url = "http://localhost:9000/intermediate"
        self.data = {'consumer_key': '12160-a5732aa14bd49ef07c5a3628',
             "redirect_uri": self.redirect_url}
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Accept': 'application/json',
            }
        self.redirect_fn = redirect_fn
        self.crawler = Manager.getCrawlerInstance()

    def login(self):
        response = requests.post("https://getpocket.com/v3/oauth/request",
                                      data=json.dumps(self.data), headers=self.headers)
        print (response)
        request_token = response.json()['code']
        url = "https://getpocket.com/auth/authorize?request_token=" + \
                   request_token + "&redirect_uri=" + self.redirect_url+"/"+request_token
        self.redirect_fn(url)

    def authorize(self, request_token):
        data = {'consumer_key': '12160-a5732aa14bd49ef07c5a3628', 'code': request_token}
        authorization = requests.post("https://getpocket.com/v3/oauth/authorize",
                                           data=json.dumps(data), headers=self.headers)
        username = authorization.json()['username']
        access_token = authorization.json()['access_token']
        print (access_token)
        pagedata = {'consumer_key': '12160-a5732aa14bd49ef07c5a3628',
             'access_token': access_token, 'state': 'all'}
        print (pagedata)
        self.redirect_fn("http://localhost:9000/articles/"+ access_token + "+" + username)

    def getlinks(self, access_token, username):
        pagedata = {'consumer_key': '12160-a5732aa14bd49ef07c5a3628',
             'access_token': access_token, 'state': 'all'}
        gotlinks = requests.post("https://getpocket.com/v3/get",
                                   data=json.dumps(pagedata), headers=self.headers)
        #print self.gotlinks
        links = gotlinks.json()['list'].values()
        #print self.links

        pocketService.fetchandsavepage(json.dumps(gotlinks.json()), username)
        #print(links)
        return links

    @staticmethod
    def fetchandsavepage(links, username):
        fetchandsavepage.delay(links, username)


