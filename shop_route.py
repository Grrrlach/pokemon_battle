from . import bp as api
from app.blueprints.auth.auth import token_auth


################################
# CATEGORY API Routes
################################

# get all the categories
@api.get('/category')
token_auth.login_required()






################################
# ITEM API Routes#
################################
