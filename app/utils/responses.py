from fastapi.responses import JSONResponse


COMMON_MESSAGES = {
    400: "Bad Request: {}",
    401: "Unauthorized: {}",
    404: "Not Found: {}",
    409: "Conflict: {}",
    500: "Internal Server Error: {}",
    200: "Success: {}",
    201: "Created: {}",
    403: "Forbidden: {}",
}


def response(status_code, *args, **kwargs):
    message_template = COMMON_MESSAGES.get(status_code, "Unknown Error: {}")
    if not args:
        args = ("",)
    message = message_template.format(*args)
    _response = {"status": status_code, "message": message}

    for key, value in kwargs.items():
        _response[key] = value

    return JSONResponse(content=_response, status_code=status_code)


def is_suceess(response):
    return response["status"] < 400
