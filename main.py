from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Speed" + "\n" + "Python")
set_website_framed(False)


@dataclass
class State:
    pass


@route
def index(state: State) -> Page:
    return Page(state, ["Speed Python"])

assert_equal(index(State()), Page(State(), ["Speed Python"]))

start_server(State())
