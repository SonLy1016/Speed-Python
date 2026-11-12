from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Speed Python")
set_website_framed(False)
add_website_css(
    ".game-title",
    "text-align: center; font-size: 60px; "
    "font-weight: bold; line-height: 1.2;"
)


@dataclass
class State:
    pass


@route
def index(state: State) -> Page:
    return Page(state, [
        Div(
            Header("Speed", 1),
            Header("Python", 1),
            classes=["game-title"]
        )
    ])

assert_equal(index(State()), Page(State(), ["Speed Python"]))

start_server(State())
