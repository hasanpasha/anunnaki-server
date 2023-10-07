from quart import Blueprint

from anunnaki_server.loader import views


loader_blueprint = Blueprint('loader_blueprint', __name__)

loader_blueprint.add_url_rule('/<string:method_name>/', 
                              view_func=views.source_method, methods=["POST"])