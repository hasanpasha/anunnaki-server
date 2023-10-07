from quart import Blueprint
from anunnaki_server.ext_manager import views # import extensions_list, extension_operation


mn_blueprint = Blueprint('manager_blueprint', __name__)

mn_blueprint.add_url_rule('/<int:id>' , view_func=views.extension_operation_by_id, methods=["GET"])
mn_blueprint.add_url_rule('/', view_func=views.extensions_list, methods=["GET"])
mn_blueprint.add_url_rule('/', view_func=views.extension_operation, methods=["POST"])