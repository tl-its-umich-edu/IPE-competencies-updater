def response_none_check(classname, response, message):
    if response is None:
        raise Exception(f"{type(classname).__name__}: {message}")