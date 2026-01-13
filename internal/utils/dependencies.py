from fastapi import Depends, Request


def get_redis(request: Request):
    # get redis from request
    return request.app.state.redis
