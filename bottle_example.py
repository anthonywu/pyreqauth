import bottle
from reqauth import RequireAuth

def get_user():
    return {
        "name": "Fake User",
        "description": "Usually you would look up a user with a session cookie"
        }

def unauthorized():
    bottle.response = 403

require_user = RequireAuth(get_user, unauthorized)

@bottle.get('/')
def index():
    return "This is the public home page"

@bottle.get('/magic/resource/<resource_id>')
@require_user
def user_account(user, resource_id):
    # notice the user object is automagically available
    return "Hi %s - welcome to resource %s" % (user["name"], resource_id)

@bottle.get('/nomagic/resource/<resource_id>')
def user_account_oldschool(resource_id):
    user = get_user() # this step is automatically handled in user_account above
    return "%s - isn't this tedious?" % user["name"]

bottle.run(host="0.0.0.0", port=8888)