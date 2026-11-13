
from bakery import assert_equal
from drafter import *
from dataclasses import dataclass


# WEBSITE SETTINGS

hide_debug_information()
set_website_title("Speed Python")
set_website_framed(False)

# These CSS rules control the appearance of the website.
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


# DATACLASSES

@dataclass
class Question:
    """Represent one Python quiz question."""
    topic: str
    question: str
    choices: list[str]
    correct_answer: str


@dataclass
class State:
    """Store information that changes during the game."""
    questions: list[Question]
    question_number: int
    score: int
    correct_answers: int
    submitted: bool
    selected_answer: str
    scores: list[int]
    answers: list[bool]


# QUESTION BANKS
# These lists are global constants.
# The game copies their questions but never changes them.

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


# HELPER FUNCTIONS

def count_topic_questions(questions: list[Question],
                          topic: str) -> int:
    """Count questions belonging to a particular topic."""
    count = 0

    for question in questions:
        if question.topic == topic:
            count += 1

    return count


def count_topic_correct(state: State, topic: str) -> int:
    """Count correct answers for a particular topic."""
    count = 0

    # Each answer corresponds to a question in the same position.
    for index, question in enumerate(state.questions):
        if question.topic == topic:
            if index < len(state.answers):
                if state.answers[index]:
                    count += 1

    return count


def topic_summary(state: State, topic: str) -> str:
    """Create a summary of the player's topic performance."""
    total = count_topic_questions(state.questions, topic)
    correct = count_topic_correct(state, topic)

    return topic + ": " + str(correct) + "/" + str(total) + " correct"


def accuracy_percentage(correct: int, total: int) -> float:
    """Calculate the percentage of correct answers."""
    if total == 0:
        return 0.0

    return round(correct / total * 100, 1)


def make_topic_results(state: State) -> list[str]:
    """Build results for each topic included in the quiz."""
    summaries = []

    topics = ["Print Statements", "If Statements"]

    for topic in topics:
        if count_topic_questions(state.questions, topic) > 0:
            summaries.append(topic_summary(state, topic))

    return summaries


def make_score_list(scores: list[int], limit: int) -> list[str]:
    """Convert the highest scores into displayable text."""
    display_scores = []

    for score in scores[:limit]:
        display_scores.append(str(score) + " points")

    return display_scores


# PAGE 1: HOME

@route
def index(state: State) -> Page:
    """Display the home page and the three highest scores."""
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
            BulletedList(make_score_list(state.scores, 3)),
            classes=["center"]
        )
    ])


# PAGE 2: LESSON SELECTION

@route
def select_lessons(state: State) -> Page:
    """Allow the player to choose Python topics."""
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
    """Start a new quiz using the selected topics."""
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

    # Reset the quiz without deleting previous high scores.
    state.questions = questions
    state.question_number = 0
    state.score = 0
    state.correct_answers = 0
    state.submitted = False
    state.selected_answer = ""
    state.answers = []

    return quiz(state)


# PAGE 3: QUIZ

@route
def quiz(state: State) -> Page:
    """Display the current question and its answer choices."""
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
        # Drafter's Timer uses milliseconds.
        # 30000 milliseconds equals 30 seconds.
        # Leaving this page stops its timer.
        content.append(Timer(30000, "time_up"))

        content.append(
            SelectBox("answer", current.choices)
        )

        content.append(
            Button("Submit", "submit_answer")
        )

    else:
        if state.selected_answer == current.correct_answer:
            content.append(Header("Correct! +10 points", 2))
        else:
            content.append(Header("Incorrect! -5 points", 2))
            content.append(
                Text("Correct answer: " + current.correct_answer)
            )

        content.append(Button("Next", "next_question"))

    return Page(state, content)


# ANSWER SUBMISSION

@route
def submit_answer(state: State, answer: str) -> Page:
    """Check the submitted answer and update the score."""
    if not state.submitted:
        current = state.questions[state.question_number]

        state.selected_answer = answer
        state.submitted = True

        if answer == current.correct_answer:
            state.score += 10
            state.correct_answers += 1
            state.answers.append(True)
        else:
            state.score -= 5
            state.answers.append(False)

    return quiz(state)


# TIMER

@route
def time_up(state: State) -> Page:
    """Subtract five points if the player runs out of time."""
    if not state.submitted:
        state.submitted = True
        state.selected_answer = ""
        state.score -= 5
        state.answers.append(False)

    return quiz(state)


# NEXT QUESTION

@route
def next_question(state: State) -> Page:
    """Advance to another question or finish the quiz."""
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
    """Display overall results and performance by topic."""
    total = len(state.questions)

    percentage = accuracy_percentage(
        state.correct_answers, total
    )

    topic_results = make_topic_results(state)

    return Page(state, [
        Header("Overall Results"),
        Header(
            str(state.correct_answers) + "/" + str(total),
            2
        ),
        Header(str(percentage) + "%", 2),
        Header("Total Points: " + str(state.score), 2),
        Header("Topic Results", 3),
        BulletedList(topic_results),
        Button("Choose Lessons", "select_lessons"),
        Button("View Scoreboard", "scoreboard")
    ])


# PAGE 5: SCOREBOARD

@route
def scoreboard(state: State) -> Page:
    """Display the ten highest point totals."""
    top_scores = make_score_list(state.scores, 10)

    return Page(state, [
        Header("Scoreboard"),
        NumberedList(top_scores),
        Button("Play Again?", "select_lessons")
    ])


# UNIT TESTS
# All tests are placed before start_server().


# TEST 1: Question counting helper

assert_equal(
    count_topic_questions(
        PRINT_QUESTIONS, "Print Statements"
    ),
    3
)

assert_equal(
    count_topic_questions(
        PRINT_QUESTIONS, "If Statements"
    ),
    0
)


# TEST 2: Accuracy helper

assert_equal(accuracy_percentage(2, 3), 66.7)
assert_equal(accuracy_percentage(3, 3), 100.0)
assert_equal(accuracy_percentage(0, 0), 0.0)


# TEST 3: Score list helper

assert_equal(
    make_score_list([30, 20, 10, 5], 3),
    ["30 points", "20 points", "10 points"]
)


# TEST 4: Home page route

home_state = State([], 0, 0, 0, False, "", [], [])

assert_equal(
    index(home_state),
    Page(home_state, [
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
            BulletedList([]),
            classes=["center"]
        )
    ])
)


# TEST 5: Lesson selection route

lesson_state = State([], 0, 0, 0, False, "", [], [])

assert_equal(
    select_lessons(lesson_state),
    Page(lesson_state, [
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
)


# TEST 6: Starting with no topics

empty_state = State([], 0, 0, 0, False, "", [], [])

assert_equal(
    start_quiz(empty_state, False, False),
    Page(empty_state, [
        Header("Please select at least one lesson."),
        Button("Back", "select_lessons")
    ])
)


# TEST 7: Starting with Print Statements

print_state = State([], 0, 0, 0, False, "", [], [])

print_page = start_quiz(print_state, True, False)

assert_equal(print_page.state.questions, PRINT_QUESTIONS)
assert_equal(print_page.state.score, 0)
assert_equal(print_page.state.correct_answers, 0)
assert_equal(print_page.state.answers, [])


# TEST 8: Starting with If Statements

if_state = State([], 0, 0, 0, False, "", [], [])

if_page = start_quiz(if_state, False, True)

assert_equal(if_page.state.questions, IF_QUESTIONS)


# TEST 9: Starting with both topics

both_state = State([], 0, 0, 0, False, "", [], [])

both_page = start_quiz(both_state, True, True)

assert_equal(
    both_page.state.questions,
    PRINT_QUESTIONS + IF_QUESTIONS
)

assert_equal(len(both_page.state.questions), 6)


# TEST 10: Quiz page route

quiz_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", [], []
)

assert_equal(
    quiz(quiz_state),
    Page(quiz_state, [
        Header("Score: 0"),
        Header("Question 1 of 3", 3),
        Div(
            Header("Print Statements", 3),
            Text("What does print('Hello') do?"),
            classes=["question-box"]
        ),
        Timer(30000, "time_up"),
        SelectBox("answer", PRINT_QUESTIONS[0].choices),
        Button("Submit", "submit_answer")
    ])
)


# TEST 11: Correct answer gives ten points

correct_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", [], []
)

correct_page = submit_answer(
    correct_state, "Displays Hello"
)

assert_equal(correct_page.state.score, 10)
assert_equal(correct_page.state.correct_answers, 1)
assert_equal(correct_page.state.answers, [True])
assert_equal(correct_page.state.submitted, True)


# TEST 12: Incorrect answer loses five points

wrong_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", [], []
)

wrong_page = submit_answer(wrong_state, "Nothing")

assert_equal(wrong_page.state.score, -5)
assert_equal(wrong_page.state.correct_answers, 0)
assert_equal(wrong_page.state.answers, [False])


# TEST 13: Cannot earn points twice on one question

double_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", [], []
)

submit_answer(double_state, "Displays Hello")
submit_answer(double_state, "Displays Hello")

assert_equal(double_state.score, 10)
assert_equal(double_state.correct_answers, 1)
assert_equal(double_state.answers, [True])


# TEST 14: Timer penalty

timer_state = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", [], []
)

timer_page = time_up(timer_state)

assert_equal(timer_page.state.score, -5)
assert_equal(timer_page.state.submitted, True)
assert_equal(timer_page.state.answers, [False])


# TEST 15: Timer cannot subtract points twice

time_up(timer_state)

assert_equal(timer_state.score, -5)
assert_equal(timer_state.answers, [False])


# TEST 16: Move to next question

next_state = State(
    PRINT_QUESTIONS, 0, 10, 1,
    True, "Displays Hello", [], [True]
)

next_page = next_question(next_state)

assert_equal(next_page.state.question_number, 1)
assert_equal(next_page.state.score, 10)
assert_equal(next_page.state.submitted, False)
assert_equal(next_page.state.selected_answer, "")


# TEST 17: Two correct answers

two_correct = State(
    PRINT_QUESTIONS, 0, 0, 0, False, "", [], []
)

submit_answer(two_correct, "Displays Hello")
next_question(two_correct)
submit_answer(two_correct, "print(5)")

assert_equal(two_correct.score, 20)
assert_equal(two_correct.correct_answers, 2)
assert_equal(two_correct.answers, [True, True])


# TEST 18: Count correct answers by topic

topic_state = State(
    PRINT_QUESTIONS + IF_QUESTIONS,
    6, 15, 3, False, "",
    [], [True, False, True, False, True, False]
)

assert_equal(
    count_topic_correct(topic_state, "Print Statements"),
    2
)

assert_equal(
    count_topic_correct(topic_state, "If Statements"),
    1
)


# TEST 19: Topic summaries

assert_equal(
    topic_summary(topic_state, "Print Statements"),
    "Print Statements: 2/3 correct"
)

assert_equal(
    topic_summary(topic_state, "If Statements"),
    "If Statements: 1/3 correct"
)

assert_equal(
    make_topic_results(topic_state),
    [
        "Print Statements: 2/3 correct",
        "If Statements: 1/3 correct"
    ]
)


# TEST 20: Results page route

results_state = State(
    PRINT_QUESTIONS, 3, 15, 2,
    False, "", [15], [True, False, True]
)

assert_equal(
    results(results_state),
    Page(results_state, [
        Header("Overall Results"),
        Header("2/3", 2),
        Header("66.7%", 2),
        Header("Total Points: 15", 2),
        Header("Topic Results", 3),
        BulletedList([
            "Print Statements: 2/3 correct"
        ]),
        Button("Choose Lessons", "select_lessons"),
        Button("View Scoreboard", "scoreboard")
    ])
)


# TEST 21: Finishing the quiz saves the score

finished_state = State(
    PRINT_QUESTIONS, 2, 20, 2,
    True, "5", [10, 30], [True, True, False]
)

finished_page = next_question(finished_state)

assert_equal(finished_page.state.question_number, 3)
assert_equal(finished_page.state.scores, [30, 20, 10])


# TEST 22: Scoreboard route

board_state = State(
    [], 0, 0, 0, False, "",
    [30, 20, 10], []
)

assert_equal(
    scoreboard(board_state),
    Page(board_state, [
        Header("Scoreboard"),
        NumberedList([
            "30 points",
            "20 points",
            "10 points"
        ]),
        Button("Play Again?", "select_lessons")
    ])
)


# TEST 23: Scoreboard keeps only ten scores

assert_equal(
    make_score_list(
        [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5],
        10
    ),
    [
        "15 points", "14 points", "13 points",
        "12 points", "11 points", "10 points",
        "9 points", "8 points", "7 points",
        "6 points"
    ]
)


# START THE GAME
# This must remain below all the tests.

start_server(
    State([], 0, 0, 0, False, "", [], [])
)
