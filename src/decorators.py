import inspect
from contextlib import contextmanager
from functools import wraps
from typing import Dict

import diskcache
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import SecurityScopes
from loguru import logger
from nicegui import ui
from nicegui.element import Element

session_info: Dict[str, Dict] = {}

dc = diskcache.Cache("cache")


def permission_required(permissions: list = []):
    def inner(func):
        logger.info("Got to permissions decorator")

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
            if (
                "id" not in kwargs["request"].session
                or kwargs["request"].session["id"] not in session_info
                or "access_token" not in session_info[kwargs["request"].session["id"]]
            ):
                raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": "/login"})
            token = session_info[kwargs["request"].session["id"]]["access_token"]
            if auth_state := dc.get(token):
                user_permissions_l = [a.name for a in auth_state.access]
                kwargs["request"].session["scopes"] = user_permissions_l
                if not permissions or "admin" in user_permissions_l:
                    pass
                elif any([x.name in permissions for x in auth_state.access]):
                    logger.info(auth_state.username, auth_state.disabled, [a.name for a in auth_state.access])
                else:
                    raise HTTPException(
                        status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": "/not_allowed"}
                    )
            elif auth_state := None: # auth_views.get_current_user_synchronous(SecurityScopes(scopes=permissions), token):
                dc.set(token, auth_state, expire=360)
                logger.info(auth_state.username, auth_state.disabled, [a.name for a in auth_state.access])
            else:
                raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": "/login"})
            return func(*args, **kwargs)

        return wrapper

    return inner


def ui_spinner(type: str = "default", size: str = "xl", thickness: int = 5, color: str = "primary"):
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if inspect.iscoroutinefunction(func) is False:
                raise TypeError("Function decorated by `nicegui_apps.ui_spinner` must be async")

            # Pull ui.spinner arguments from kwargs
            if "element" in kwargs:
                element: Element = kwargs["element"]
                del kwargs["element"]
            else:
                raise TypeError(
                    "`element` (ui.element or some sort) arguement must be passed to function decorated with "
                    "`nicegui_apps.ui_spinner`, or to the decorator itself."
                )

            element.clear()
            with element:
                ui.spinner(type=type, size=size, thickness=thickness, color=color)
            result = await func(*args, **kwargs)
            element.clear()
            return result

        return wrapper

    return inner


# def admin_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if "site-administrator" not in kwargs["request"].session.get("permissions"):
#             print("Not an administrator.")
#             raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": "/not_allowed"})
#         return func(*args, **kwargs)

#     return wrapper


####################################################
# WINNER OPTION BY FAR
####################################################
@contextmanager
def spinner(element: Element, **kwargs):
    """Turns ui.spinner into context manager
    - Clears "element", initializes spinner inside "element, then clears again during context manager cleanup
    - In addition to "element", this also accepts any keyword arguments that ui.spinner accepts.
      - See `nicegui.ui.spinner` docs: https://nicegui.io/documentation/spinner
    - Functions used in context manager must be async and awaited
      - Note: Entire app does not need to be async. The example below shows how to tuck the async function 
      inside a async button click handler. In this case only the button click handler, and the function it calls, 
      need to be async.
    
    Args:
        element (Element): Element to clear and populate with spinner
        **kwargs: Any keyword arguments that ui.spinner accepts
    
    Returns: None

    - Example usage:
    ```python
    import asyncio
    from nicegui import ui
    
    async def takes_time(row: ui.row) -> str:
        with spinner(element=row, type="hourglass", size="2em"):
            await asyncio.sleep(4)
        with row:
            ui.label("After...")

    @ui.page("/")
    def sample():
        async def button_load_label():
            await takes_time(row)

        row = ui.row()
        with row:
            ui.label("Before...")
        ui.button("Load new label", on_click=button_load_label)

    ui.run()
    ```
    """
    try:
        element.clear()
        with element:
            ui.spinner(**kwargs)
            yield
    finally:
        element.clear()