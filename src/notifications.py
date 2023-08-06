from dataclasses import dataclass
from datetime import datetime
from functools import partial
from typing import List, Literal

from nicegui import ui
from nicegui.elements.menu import Menu
from pydantic import BaseModel


class NotificationType(BaseModel):
    id: int
    name: Literal["Profile Update", "First Donation", "Above Average Donation"]


class Notification(BaseModel):
    id: int
    type: int
    message: str
    user: int
    read: bool
    created_at: datetime
    read_at: datetime


@dataclass
class NotificationList:
    user: int
    notifications: List[Notification]
    show_read: bool = False
    menu: Menu = None

    def notify_menu(self):
        self.notify_list()

        button_color = "bg-red" if not any(x.read for x in self.notifications) else ""
        ui.button(on_click=lambda: self.menu_toggle()).classes(button_color).props("icon=notifications_none")

    def toogle_read(self, show: bool = False):
        self.show_read = show
        self.menu.clear()
        self.notify_list()

    def notify_list(self):
        self.menu.clear()
        with self.menu:
            all_read = True
            for notification in self.notifications:
                if notification.read and not self.show_read:
                    continue
                all_read = False
                color = "bg-gray-200" if notification.read else ""
                with ui.card().classes(f"w-80 rounded-none {color}"):
                    type_name = [ntype for ntype in demo_types if ntype.id == notification.type][0].name
                    ui.label(type_name).classes("font-bold")
                    ui.label(notification.message)
                    delete = partial(self.delete_notification, notification.id)
                    ui.button("Open", on_click=delete).props(("color=secondary" if notification.read else ""))
            if all_read:
                with ui.card().classes("w-80 rounded-none"):
                    ui.label("Everything is good").classes("font-bold")
            show = ui.switch("Show Read", value=self.show_read, on_change=lambda: self.toogle_read(show.value))

    def delete_notification(self, key):
        # This will actually update a database record
        for notification in self.notifications:
            if notification.id == key:
                notification.read = True
        self.menu.clear()
        self.notify_list()

    def menu_toggle(self):
        print(self.menu.value)
        if self.menu.value is True:
            self.menu.close()
        else:
            self.menu.open()


demo_types = [
    NotificationType(id=1, name="Profile Update"),
    NotificationType(id=2, name="First Donation"),
    NotificationType(id=3, name="Above Average Donation"),
]
