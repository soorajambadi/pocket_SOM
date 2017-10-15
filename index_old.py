from service.pocket import pocketservice

__author__ = 'tintin'
from bottle import run, Bottle, redirect

pocket = Bottle()
user = pocketservice.pocketService(redirect)
''' Here we are creating a pocket user with page after authentication passed as argument'''
#Redesign with session and cookie support


@pocket.route('/index')
def index():
    try:
        if user:
            return 'Welcome to Pocket Recommendation Engine ' + user.username
    except:
        return "Welcome to Pocket Recommendation Engine Stranger"


@pocket.route('/login')
def login():
    print(user)
    if user.username is None:
        user.login()
    else:
        redirect("http://localhost:9000/articles")


@pocket.route('/intermediate/<token>')
def intermediate(token):
    user.authorize(token)


@pocket.route('/articles/<tokenusername>')
def displayarticles(tokenusername):
    token, username = tokenusername.split("+")
    print ("Hello Everyone " + token + " username is " + username)
    links = user.getlinks(token, username)
    output=[]
    for link in links:
        try:
            #print(link['resolved_url'])
            output.append(link['resolved_url'])
        except:
            pass
    return '    '.join(output)
    #print user.links
    #fetch contents from redis


run(pocket, host='localhost', port=9000, debug=True)