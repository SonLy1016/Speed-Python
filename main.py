
from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

hide_debug_information()
set_website_title("Speed Python")
set_website_framed(False)

# WEBSITE STYLING

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


# DATA CLASSES

@dataclass
class Question:
    topic: str
    question: str
    choices: list[str]
    correct_answer: str


@dataclass
class State:
    questions: list[Question]
    question_number: int
    score: int
    correct_answers: int
    submitted: bool
    selected_answer: str
    scores: list[int]


# QUESTION BANK

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
            Header(
                "Which Lessons Would You Like To Work On?", 2
            ),
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

    # Reset information for the new game
    state.questions = questions
    state.question_number = 0
    state.score = 0
    state.correct_answers = 0
    state.submitted = False
    state.selected_answer = ""

    return quiz(state)


# PAGE 3: QUIZ

@route
def quiz(state: State) -> Page:
    current = state.questions[state.question_number]

    content = [
        Header("Score: " + str(state.score)),
        Header(
            "Question " +
            str(state.question_number + 1) +
            " of " + str(len(state.questions)),
            3
        ),
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
                Text(
                    "Correct answer: " +
                    current.correct_answer
                )
            )

        content.append(Button("Next", "next_question"))

    return Page(state, content)


# CHECK ANSWER AND UPDATE SCORE

@route
def submit_answer(state: State, answer: str) -> Page:
    if not state.submitted:
        current = state.questions[state.question_number]

        state.selected_answer = answer
        state.submitted = True

        if answer == current.correct_answer:
            state.score += 10
            state.correct_answers += 1
        else:
            state.score -= 5

    return quiz(state)


# TIMER RUNS OUT

@route
def time_up(state: State) -> Page:
    if not state.submitted:
        state.submitted = True
        state.selected_answer = ""
        state.score -= 5

    return quiz(state)


# MOVE TO NEXT QUESTION

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

    percentage = round(
        state.correct_answers / total * 100, 1
    )

    return Page(state, [
        Header("Overall Results"),
        Header(
            str(state.correct_answers) +
            "/" + str(total),
            2
        ),
        Header(str(percentage) + "%", 2),
        Header(
            "Total Points: " + str(state.score),
            2
        ),
        Header("Topic Results", 3),
        Text(
            "Your total correct answers: " +
            str(state.correct_answers)
        ),
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


# ASSERT_EQUAL TESTS

# Test 1: Home page contains the correct title
home_state = State([], 0, 0, 0, False, "", [])

home_page = index(home_state)

assert_equal(home_page.state.score, 0)
assert_equal(home_page.state.scores, [])


# Test 2: Selecting Print Statements
print_state = State([], 0, 0, 0, False, "", [])

print_page = start_quiz(print_state, True, False)

assert_equal(print_page.state.questions, PRINT_QUESTIONS)
assert_equal(print_page.state.question_number, 0)
assert_equal(print_page.state.score, 0)
assert_equal(print_page.state.correct_answers, 0)


# Test 3: Selecting If Statements
if_state = State([], 0, 0, 0, False, "", [])

if_page = start_quiz(if_state, False, True)

assert_equal(if_page.state.questions, IF_QUESTIONS)


# Test 4: Selecting both topics
both_state = State([], 0, 0, 0, False, "", [])

both_page = start_quiz(both_state, True, True)

assert_equal(
    both_page.state.questions,
    PRINT_QUESTIONS + IF_QUESTIONS
)
assert_equal(len(both_page.state.questions), 6)


# Test 5: Correct answer gives 10 points
correct_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", []
)

submit_answer(correct_state, "Displays Hello")

assert_equal(correct_state.score, 10)
assert_equal(correct_state.correct_answers, 1)
assert_equal(correct_state.submitted, True)


# Test 6: Incorrect answer loses 5 points
wrong_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", []
)

submit_answer(wrong_state, "Nothing")

assert_equal(wrong_state.score, -5)
assert_equal(wrong_state.correct_answers, 0)
assert_equal(wrong_state.submitted, True)


# Test 7: Timer runs out and loses 5 points
timer_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", []
)

time_up(timer_state)

assert_equal(timer_state.score, -5)
assert_equal(timer_state.correct_answers, 0)
assert_equal(timer_state.submitted, True)


# Test 8: Cannot score twice on one question
double_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", []
)

submit_answer(double_state, "Displays Hello")
submit_answer(double_state, "Displays Hello")

assert_equal(double_state.score, 10)
assert_equal(double_state.correct_answers, 1)


# Test 9: Move to the next question
next_state = State(
    PRINT_QUESTIONS, 0, 10, 1,
    True, "Displays Hello", []
)

next_question(next_state)

assert_equal(next_state.question_number, 1)
assert_equal(next_state.score, 10)
assert_equal(next_state.correct_answers, 1)
assert_equal(next_state.submitted, False)
assert_equal(next_state.selected_answer, "")


# Test 10: Two correct answers give 20 points
two_correct = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", []
)

submit_answer(two_correct, "Displays Hello")
next_question(two_correct)
submit_answer(two_correct, "print(5)")

assert_equal(two_correct.score, 20)
assert_equal(two_correct.correct_answers, 2)


# Test 11: Final score is added to scoreboard
finished_state = State(
    PRINT_QUESTIONS, 2, 20, 2,
    True, "5", [10, 30]
)

next_question(finished_state)

assert_equal(finished_state.scores, [30, 20, 10])


# Test 12: Scoreboard displays only top 10
board_state = State(
    [], 0, 0, 0, False, "",
    [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5]
)

board_page = scoreboard(board_state)

assert_equal(
    board_page,
    Page(board_state, [
        Header("Scoreboard"),
        NumberedList(
            [15, 14, 13, 12, 11, 10, 9, 8, 7, 6]
        ),
        Button("Play Again?", "select_lessons")
    ])
)


# START THE WEBSITE
start_server(State([], 0, 0, 0, False, "", []))
