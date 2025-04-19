# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .landlord import landlord_views
from .tenant import tenant_views
views = [user_views, index_views, auth_views,landlord_views,tenant_views] 
# blueprints must be added to this list