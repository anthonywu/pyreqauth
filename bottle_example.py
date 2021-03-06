import bottle
from reqauth import RequireAuth

def get_user():
    return {
        "name": "Fake User",
        "description": "Usually you would look up a user with a session cookie"
        }

def mock_get_no_user():
    return None

def unauthorized():
    bottle.response.status = 403
    return "You can't access this resource"

# One-Liner: declare how you want to get your user and how you'd like to handle unauthorized access
require_user = RequireAuth(get_user, unauthorized)

@bottle.get('/')
def index():
    return "This is the public home page"

@bottle.get('/magic/resource/<resource_id>')
@require_user # <-- this is the awesome magic
def user_account(user, resource_id): # <-- the 'user' arg is provided by the decorator
    # notice the user object is automagically available
    return "Hi %s - welcome to resource %s" % (user["name"], resource_id)

mock_no_user = RequireAuth(mock_get_no_user, unauthorized)

@bottle.get('/rejected')
@mock_no_user
def no_user_account(user):
    return "This flow will never be called"

# Usually you'd do something like this:
@bottle.get('/nomagic/resource/<resource_id>')
def user_account_oldschool(resource_id):
    user = get_user() # this step is automatically handled in user_account above
    if user:
        return "%s - isn't this tedious?" % user["name"]
    else:
        bottle.response = 403

bottle.debug()
bottle.run(host="localhost", port=8888, server="auto")

# after starting the server, visit
#  - http://localhost:8888/
#  - http://localhost:8888/magic/resource/123
#  - http://localhost:8888/nomagic/resource/123
#  - http://localhost:8888/rejected
