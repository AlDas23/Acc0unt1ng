from functools import wraps
from flask import jsonify
from db_scripts.dbScripts import CheckDB


def db_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        status = CheckDB()
        if status > 0:  # Database does not exist or corrupt
            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"Database status code: {status}.",
                        "redirect": "/options/db",
                    }
                ),
                200,
            )
        else:
            return f(*args, **kwargs)

    return decorated_function
