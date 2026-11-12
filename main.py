from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Speed Python")
set_website_framed(False)
add_website_css(
    ".game-title",
    "text-align: center;"
)

add_website_css(
    ".game-title h1",
    "margin: 0; "
    "font-weight: bold; "
    "line-height: 1.0;"
)

@dataclass
class State:
    pass


@route
def index(state: State) -> Page:
    return Page(state, [
        Div(
            Header("Speed", 1, style_font_size="40px"),
            Header("Python", 1, style_font_size="40px"),
            classes=["game-title"]
        )
    ])

assert_equal(
    index(State()),
    Page(State(), [
        Div(
            Header("Speed", 1, style_font_size="40px"),
            Header("Python", 1, style_font_size="40px"),
            classes=["game-title"]
        )
    ])
)

start_server(State())
