import bottle
from reqauth import RequireAuth

def get_user():
    return {
        "name": "Fake User",
        "description": "Usually you would look up a user with a session cookie"
        }

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

@bottle.get('/nomagic/resource/<resource_id>')
def user_account_oldschool(resource_id):
    user = get_user() # this step is automatically handled in user_account above
    return "%s - isn't this tedious?" % user["name"]

bottle.run(host="0.0.0.0", port=8888)
