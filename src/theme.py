from contextlib import contextmanager
from typing import TYPE_CHECKING

from nicegui import ui

from .menu import menu

if TYPE_CHECKING:
    from nicegui.page_layout import LeftDrawer


def left_drawer():
    # return ui.left_drawer().classes("bg-zinc-800").props("width=200 bordered")
    return ui.left_drawer().classes("bg-zinc-200").props("width=200 bordered")


@contextmanager
def frame(navtitle: str, scopes: list[str] = [], left_drawer: "LeftDrawer" = None):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary="#6E93D6", secondary="#53B689", accent="#111B1E", positive="#53B689")
    with ui.header().classes("justify-between text-white pt"):
        if left_drawer:
            ui.button(on_click=lambda: left_drawer.toggle()).props("flat color=white icon=menu")
        ui.label(navtitle).classes("font-bold mt-2")
        with ui.row():
            menu(scopes)
    with ui.row():  #.classes("mx-auto"):  # content-center"):
        yield


feed_tags = "rounded-full bg-blue px-2 py--1 font-medium text-gray-200"
feed_card = "p-1 bg-slate-200 hover:bg-slate-300 w-96 min-width-full"
feed_labels = "rounded-full px-2 py--1 font-medium"
person_tags = feed_labels


done = "rounded-full px-2 py--1 font-medium bg-white text-gray-500"
note = "rounded-full px-2 py--1 font-medium bg-purple text-gray-200"
