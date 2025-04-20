from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=username)
    return None


def setup_jwt(app):
    jwt = JWTManager(app)

    # Configures flask-jwt to resolve get_current_identity() to the corresponding user's ID
    @jwt.user_identity_loader
    def user_identity_lookup(username):
      return username


    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).first()

    return jwt



# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          username = get_jwt_identity()
          if username:
              current_user = User.query.filter_by(username=username).first()
              is_authenticated = current_user is not None
          else:
              current_user = None
              is_authenticated = False
      except Exception as e:
          print(e)
          current_user = None
          is_authenticated = False
      return dict(is_authenticated=is_authenticated, current_user=current_user)

@jwt_required()
def get_current_user():
  user_id = get_jwt_identity()
  return User.query.get(user_id)