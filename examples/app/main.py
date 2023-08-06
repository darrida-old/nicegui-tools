from nicegui import app, ui
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from . import example_c, home_page, theme


# Start/Stop Heroku Postgres Connection Pool
@app.on_event("startup")
def open_pool():
    ...


@app.on_event("shutdown")
def close_pool():
    ...


# Root endpoint to check for up status
class ServiceStatus(BaseModel):
    greeting: str = "I'm here!"


# here we use our custom page decorator directly and just put the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        home_page.content()


# we can also use the APIRouter as described in https://nicegui.io/documentation/page#modularize_with_apirouter
app.include_router(example_c.router)


def main():
    https_only = True
    app.add_middleware(SessionMiddleware, secret_key="SECRET", https_only=https_only)
    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    main()
