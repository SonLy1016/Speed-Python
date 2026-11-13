
from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

hide_debug_information()
set_website_title("Speed Python")
set_website_framed(False)

# Website styling
add_website_css(
    ".game-title",
    "text-align: center;"
)

add_website_css(
    ".game-title h1",
    "font-size: 80px; margin: 0; "
    "font-weight: bold; line-height: 1.0;"
)

add_website_css(
    ".center",
    "text-align: center; margin: 20px;"
)

add_website_css(
    ".question-box",
    "background-color: #eeeeee; "
    "border: 1px solid gray; "
    "padding: 25px; text-align: center;"
)



# A question and its possible answers
@dataclass
class Question:
    topic: str
    question: str
    choices: list[str]
    correct_answer: str


# Information the game remembers
@dataclass
class State:
    questions: list[Question]
    question_number: int
    score: int
    submitted: bool
    selected_answer: str
    scores: list[int]


# Our first six questions
PRINT_QUESTIONS = [
    Question(
        "Print Statements",
        "What does print('Hello') do?",
        ["Displays Hello", "Creates a variable",
         "Deletes Hello", "Nothing"],
        "Displays Hello"
    ),
    Question(
        "Print Statements",
        "Which statement prints the number 5?",
        ["show(5)", "print(5)", "display(5)", "say(5)"],
        "print(5)"
    ),
    Question(
        "Print Statements",
        "What is printed by print(2 + 3)?",
        ["2 + 3", "23", "5", "Nothing"],
        "5"
    )
]

IF_QUESTIONS = [
    Question(
        "If Statements",
        "Which keyword begins a conditional statement?",
        ["when", "check", "if", "test"],
        "if"
    ),
    Question(
        "If Statements",
        "What does 5 > 3 evaluate to?",
        ["True", "False", "5", "3"],
        "True"
    ),
    Question(
        "If Statements",
        "What keyword provides an alternative branch?",
        ["otherwise", "else", "other", "instead"],
        "else"
    )
]


# PAGE 1: HOME
@route
def index(state: State) -> Page:
    return Page(state, [
        Div(
            Header("Speed", 1),
            Header("Python", 1),
            classes=["game-title"]
        ),
        Div(
            Button("Continue", "select_lessons"),
            classes=["center"]
        ),
        Div(
            Header("Top 3 Scores", 3),
            BulletedList(state.scores[:3]),
            classes=["center"]
        )
    ])


# PAGE 2: LESSON SELECTION
@route
def select_lessons(state: State) -> Page:
    return Page(state, [
        Div(
            Header("Which Lessons Would You Like To Work On?", 2),
            classes=["center"]
        ),
        CheckBox("print_statements", False),
        "Print Statements",
        LineBreak(),
        CheckBox("if_statements", False),
        "If Statements",
        LineBreak(),
        Button("START", "start_quiz")
    ])


@route
def start_quiz(state: State,
               print_statements: bool = False,
               if_statements: bool = False) -> Page:

    questions = []

    if print_statements:
        questions.extend(PRINT_QUESTIONS)

    if if_statements:
        questions.extend(IF_QUESTIONS)

    if len(questions) == 0:
        return Page(state, [
            Header("Please select at least one lesson."),
            Button("Back", "select_lessons")
        ])

    state.questions = questions
    state.question_number = 0
    state.score = 0
    state.submitted = False
    state.selected_answer = ""

    return quiz(state)


# PAGE 3: QUIZ
@route
def quiz(state: State) -> Page:
    current = state.questions[state.question_number]

    content = [
        Header("Score: " + str(state.score)),
        Header("Question " +
               str(state.question_number + 1) +
               " of " + str(len(state.questions)), 3),
        Div(
            Header(current.topic, 3),
            Text(current.question),
            classes=["question-box"]
        )
    ]

    if not state.submitted:
        content.append(Timer(30000, "time_up"))
        content.append(
            SelectBox("answer", current.choices)
        )
        content.append(
            Button("Submit", "submit_answer")
        )
    else:
        if state.selected_answer == current.correct_answer:
            content.append(Header("Correct!", 2))
        else:
            content.append(Header("Incorrect!", 2))
            content.append(
                Text("Correct answer: " + current.correct_answer)
            )

        content.append(Button("Next", "next_question"))

    return Page(state, content)


@route
def submit_answer(state: State, answer: str) -> Page:
    if not state.submitted:
        current = state.questions[state.question_number]

        state.selected_answer = answer
        state.submitted = True

        if answer == current.correct_answer:
            state.score += 1

    return quiz(state)


@route
def time_up(state: State) -> Page:
    if not state.submitted:
        state.submitted = True
        state.selected_answer = ""
    return quiz(state)


@route
def next_question(state: State) -> Page:
    state.question_number += 1
    state.submitted = False
    state.selected_answer = ""

    if state.question_number >= len(state.questions):
        state.scores.append(state.score)
        state.scores.sort(reverse=True)
        return results(state)

    return quiz(state)


# PAGE 4: RESULTS
@route
def results(state: State) -> Page:
    total = len(state.questions)
    percentage = round(state.score / total * 100, 1)

    return Page(state, [
        Header("Overall Results"),
        Header(str(state.score) + "/" + str(total), 2),
        Header(str(percentage) + "%", 2),
        Header("Topic Results", 3),
        Text("Your total correct answers: " + str(state.score)),
        Button("Choose Lessons", "select_lessons"),
        Button("View Scoreboard", "scoreboard")
    ])


# PAGE 5: SCOREBOARD
@route
def scoreboard(state: State) -> Page:
    top_scores = state.scores[:10]

    return Page(state, [
        Header("Scoreboard"),
        NumberedList(top_scores),
        Button("Play Again?", "select_lessons")
    ])


# Start the game
start_server(State([], 0, 0, False, "", []))
