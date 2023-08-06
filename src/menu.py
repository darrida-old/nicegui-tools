from nicegui import ui
from pydantic import BaseModel

notifications_toggle = False
if notifications_toggle:
    from .notifications import Notification, NotificationList


class MenuItem(BaseModel):
    name: str
    link: str
    allowed: list = []
    order: int = 99


menu_links = [
    MenuItem(name="Home", link="/home", allowed=["user", "admin"], order=1),
    MenuItem(name="Admin", link="/admin", allowed=["admin"], order=2),
    MenuItem(name="HA", link="/matter", allowed=["admin"], order=3),
]


def menu(scopes: list = None) -> None:
    scopes = [] if scopes is None else scopes

    # for dev
    scopes: list = ["user", "admin"]

    menu_items = sorted(menu_links, key=lambda x: x.order)
    for m in menu_items:
        if m.allowed:
            if any(scope in scopes for scope in m.allowed):
                ui.link(m.name, m.link).classes(replace="text-white mt-2")
        else:
            ui.link(m.name, m.link).classes(replace="text-white mt-2")
    if notifications_toggle:
        notification_list = NotificationList(user=1, notifications=demo_notifications)
        with ui.column().classes():
            notification_list.menu = ui.menu().classes("rounded")
            notification_list.notify_menu()

if notifications_toggle:
    demo_notifications = [
        Notification(
            id=100,
            type=1,
            message="Ben Hammond updated his email address.",
            user=1,
            read=False,
            created_at="2023-03-27 12:00:00",
            read_at="2023-04-01 12:00:00",
        ),
        Notification(
            id=101,
            type=2,
            message="Adam Hammond made a first donation.",
            user=1,
            read=False,
            created_at="2023-03-27 12:00:00",
            read_at="2023-04-01 12:00:00",
        ),
        Notification(
            id=102,
            type=3,
            message="Sarah Hammond made higher than usual donation.",
            user=1,
            read=False,
            created_at="2023-03-27 12:00:00",
            read_at="2023-04-01 12:00:00",
        ),
    ]
