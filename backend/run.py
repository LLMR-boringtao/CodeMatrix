import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from quart import Quart
from quart import Quart, Response, ResponseReturnValue
from backend.src.backend.blueprints.control import blueprint as control_blueprint
from backend.src.backend.lib.api_error import APIError
 
app = Quart(__name__)
app.config.from_prefixed_env(prefix="CodeMatrix")
app.register_blueprint(control_blueprint)


@app.errorhandler(APIError)  # type: ignore
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    return {"code": error.code}, error.status_code

@app.errorhandler(500)
async def handle_generic_error(error: Exception) -> ResponseReturnValue:
    return {"code": "INTERNAL_SERVER_ERROR"}, 500