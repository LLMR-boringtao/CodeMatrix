import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
from subprocess import call
from urllib.parse import urlparse 

from quart import Quart, Response, ResponseReturnValue
from quart_auth import QuartAuth
from quart_rate_limiter import RateLimiter
from quart_rate_limiter import RateLimitExceeded
from quart_schema import QuartSchema
from quart_schema import RequestSchemaValidationError
from quart_db import QuartDB

from backend.src.backend.blueprints.control import blueprint as control_blueprint
from backend.src.backend.lib.api_error import APIError


app = Quart(__name__)
app.config.from_prefixed_env(prefix="CodeMatrix")
app.register_blueprint(control_blueprint)
auth_manager = QuartAuth(app)
rate_limiter = RateLimiter(app)
schema = QuartSchema(app, convert_casing=True)


@app.errorhandler(APIError)
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    return {"code": error.code}, error.status_code

@app.errorhandler(500)
async def handle_generic_error(error: Exception) -> ResponseReturnValue:
    return {"code": "INTERNAL_SERVER_ERROR"}, 500
 
@app.errorhandler(RateLimitExceeded)
async def handle_rate_limit_exceeded_error(
    error: RateLimitExceeded,
) -> ResponseReturnValue:
    return {}, error.get_headers(), 429

@app.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(
    error: RequestSchemaValidationError,
) -> ResponseReturnValue:
    if isinstance(error.validation_error, TypeError):
        return {"errors": str(error.validation_error)}, 400
    else:
        return {"errors": error.validation_error.json()}, 400
    
@app.cli.command("recreate_db")
def recreate_db() -> None:
    db_url = urlparse(os.environ["CODEMATRIX_QUART_DB_DATABASE_URL"])
    call(
        ["psql", "-U", "postgres", "-c", f"DROP DATABASE IF EXISTS {db_url.path.removeprefix('/')}"],
    )
    call(
        ["psql", "-U", "postgres", "-c", f"DROP USER IF EXISTS {db_url.username}"],
    )
    call(
        ["psql", "-U", "postgres", "-c", f"CREATE USER {db_url.username} LOGIN PASSWORD '{db_url.password}' CREATEDB"],
    )
    call(
        ["psql", "-U", "postgres", "-c", f"CREATE DATABASE {db_url.path.removeprefix('/')}"],
    )