# drafter-deployment-template-v1
Your first Drafter website!

Ai was slightly used to clear any misunderstood information when it came to if I was missing any requirements, changing my score to increase by 10 if answered correctly and decrease by 5 if answered incorrectly, and understanding what was wrong with my initilal title screen.

i would like the space between Speed and Python to be a little smaller if we could make it a bit smaller
Absolutely! We can make Speed and Python closer together without changing their size or position.

The large gap is most likely caused by the default spacing that Drafter gives to Header() components.

1. Change your CSS code
Replace your current .game-title h1 styling with this:

add_website_css(
    ".game-title h1",
    "font-size: 60px; margin: 0; line-height: 1.1;"
)

2. Keep your index function the same
@route
def index(state: State) -> Page:
    return Page(state, [
        Div(
            Header("Speed", 1),
            Header("Python", 1),
            classes=["game-title"]
        )
    ])

3. What changed?
margin: 0; removes the extra space around each heading.

line-height: 1.1; controls how closely the text lines sit together.

font-size: 60px; keeps the title large.

Adjust the spacing yourself
You can experiment with these values:

Line height

Appearance

1.5

More space

1.2

Normal spacing

1.1

Close together

1.0

Very close together

My suggestion: Start with 1.1. That should give your Speed Python title a more compact, game-like appearance while keeping it centered at the top.

 I would like to change the score of the originally gained to 10 while making the score decrease if the answer was incorrect
Absolutely! We can change the scoring system in Speed Python so that players earn 10 points for a correct answer and lose points for an incorrect answer.

Since you haven't specified how many points an incorrect answer should deduct, I'll use −5 points as an example.

1. Our new scoring system
Player's answer

Points

 Correct

+10

 Incorrect

−5

 Time runs out

−5

For example, if a player gets three correct answers and two incorrect answers:

(
3
×
10
)
−
(
2
×
5
)
=
20
(3×10)−(2×5)=20
Their final score would be 20 points.

2. Modify your submit_answer() function
Find your current function:

@route
def submit_answer(state: State, answer: str) -> Page:
    if not state.submitted:
        current = state.questions[state.question_number]

        state.selected_answer = answer
        state.submitted = True

        if answer == current.correct_answer:
            state.score += 1

    return quiz(state)

Replace it with:

@route
def submit_answer(state: State, answer: str) -> Page:
    if not state.submitted:
        current = state.questions[state.question_number]

        state.selected_answer = answer
        state.submitted = True

        if answer == current.correct_answer:
            state.score += 10
        else:
            state.score -= 5

    return quiz(state)

What changed?
state.score += 10 adds 10 points for a correct answer.

state.score -= 5 subtracts 5 points for an incorrect answer.

else runs when the answer isn't correct.

if not state.submitted prevents the same question from being scored twice.

3. Update your timer function
If you want players to lose 5 points when they run out of time, change your time_up() function to:

@route
def time_up(state: State) -> Page:
    if not state.submitted:
        state.submitted = True
        state.selected_answer = ""
        state.score -= 5

    return quiz(state)

This means that when the timer runs out, the player receives the same penalty as an incorrect answer.

does this fill these requirements?
Final Project Roadmap
The final project will involve creating a web application with Drafter. The different steps of the project will be spread across the last several weeks of class.
- Week 10: Brainstorming & Ideation - You will come up with an idea for your web application. You will brainstorm its goal, details, and functionality.
- Week 11: Design - You will plan how the site will look and how you will implement the requirements listed on this page.
- Week 12: Development & Deployment - You will develop the code for your website and deploy it.
- Week 13: User Testing - You will show your website to peers and get feedback on their experiences using it.
- Week 14: Updates based on Feedback - You will make updates based on the feedback you receive and reflect on the process of creating your web application.
- Site Functionality Requirements
Below are the requirements that your site must fulfill. Plan ahead so that meeting these requirements is easier as you develop your project.
- At least 7 routes.
- At least 5 Pages, or 10 , or a combination thereof.
- The implementation of the State dataclass must have at least 4 fields.
  - At least one field must be a list of class instances or a dictionary of class instances.
    - This means that there must be a second dataclass.
  - At least 4 state fields, including the list or dictionary of class instances, must each be meaningfully modified in at least one route; those 4 state fields cannot be constants.
- At least 3 input fields (TextBox, CheckBox, SelectBox, TextArea). They don't have to be the same type.
- At least 3 meaningful if statements.
- At least 1 loop that iterates over an attribute of the list of class instances or dictionary of class instances in a meaningful way.
- The site should have a legitimate purpose or functionality.
- No global variables ( are fine).
- You must use the Drafter library.
- Any advanced coding techniques (i.e. that weren't covered in this course) used are thoroughly documented in the code.
More creative and impressive designs are given flexibility on the above requirements - impress us! However, impressive websites tend to do more than the above requirements. Further, if you miss more than 2 requirements, you will get no credit for that submission, and therefore would fail the class per . For example, missing a second dataclass means you would be missing not only that requirement, but also the list or dictionary of such dataclass instances, and the loop iterating over that list. This would mean that the submission would get a zero.
Code Requirements
Make sure your program and website runs; broken programs do not earn points. This means that if your program contains a syntax error or runs and doesn't deploy a website, you get zero points for this assignment, and may fail the class under the rules highlighted in .

Once you are finished with your project code, check over the following:
- Chosen good variable names (check last two sections of )
- Unit tested your functions where possible, being : each route must have at least one unit test, if possible (routes that have randomization are difficult to unit test, so they are not required to).
  - If a function can't be unit tested, you must note as much in a docstring or comment.
- Broke up excessively long lines (80 characters is a good rule of thumb, but we'll be strict about not exceeding 120 characters)
- Included types in your function headers
- Included good as the first line of your function's body
- Decomposed complicated functions with helper functions
Your TA will be grading your code's quality based on the ideas above.















Speed Python is close, but it does not meet every requirement yet. The good news is that your game already has most of the important pieces. We can fix the missing requirements without starting over.

I'm comparing the complete version of your code from my previous message against the rubric you provided.
1. Site functionality requirements
Requirements met
7 of 10



Based on the code as written, not a verified deployment. Some items still need testing.
Requirement	Status	Explanation
At least 7 routes	Met	You have 9 @route functions.
At least 5 Pages	Met	Home, lessons, quiz, results, and scoreboard are five distinct page views.
State has at least 4 fields	Met	Your State has 7 fields.
Second dataclass and list of instances	Met	Question and questions: list[Question].
At least 4 State fields meaningfully modified	Met	questions, question_number, score, correct_answers, and others change.
At least 3 input fields	Met	Two CheckBox fields and one SelectBox.
At least 3 meaningful if statements	Met	You have several for lesson selection, scoring, and navigation.
Loop over list of dataclass instances	Missing	You don't currently have a for loop over your questions.
Legitimate purpose	Met	Your website teaches introductory Python.
No global variables, use Drafter, document advanced code	Review	You use Drafter and global question banks as constants. You should document the timer and CSS helpers.

One important detail: PRINT_QUESTIONS and IF_QUESTIONS are global question banks. They are intended to be constants, which the rubric permits. Keep them unchanged during gameplay.
2. Code quality requirements
Requirement	Status	What to improve
Good variable names	Met	Names like correct_answers, question_number, and selected_answer are clear.
Unit test every route	Partial	Some routes aren't directly tested yet.
Lines no longer than 120 characters	Likely met	Your lines are generally short.
Type annotations	Met	Your route functions have parameter and return types.
Docstrings	Missing	Your route functions need docstrings.
Helper functions	Improve	A helper for calculating topic results would be useful.
Website runs and deploys	Not verified	We need to run and test the actual website.

3. The most important missing requirement: a loop
Your rubric specifically requires:
At least 1 loop that iterates over an attribute of the list of class instances or dictionary of class instances in a meaningful way.

We can satisfy this by writing a function that counts how many questions belong to a particular topic.

Add this function above your routes:
def count_topic_questions(questions: list[Question],                          topic: str) -> int:    """Count how many questions belong to the given topic."""    count = 0    for question in questions:        if question.topic == topic:            count += 1    return count



This is a meaningful loop because:
- questions is a list of Question dataclass instances.
- for question in questions visits each question.
- question.topic accesses an attribute of a Question.
- The function counts questions matching a topic.
Then, inside your results() function, you could use:
print_total = count_topic_questions(    state.questions, "Print Statements")if_total = count_topic_questions(    state.questions, "If Statements")



And display those totals on the results page.

Important: To fully satisfy the rubric, the loop should contribute to actual website functionality, not exist only for a test. Using it to calculate topic results accomplishes that.
4. Add docstrings to every route
Your rubric specifically requires docstrings as the first line inside each function.

For example, change:
@routedef index(state: State) -> Page:    return Page(state, [        # Page content    ])



To:
@routedef index(state: State) -> Page:    """Display the home page and the top three scores."""    return Page(state, [        # Page content    ])



Here are suitable docstrings for your existing routes:
Function	Suggested docstring
index	"""Display the home page and top three scores."""
select_lessons	"""Display the available lesson choices."""
start_quiz	"""Create a quiz using the selected lessons."""
quiz	"""Display the current question and answer choices."""
submit_answer	"""Check an answer and update the player's score."""
time_up	"""Apply a penalty when the question timer expires."""
next_question	"""Move to the next question or show the results."""
results	"""Display the player's final score and accuracy."""
scoreboard	"""Display the ten highest scores."""

5. Add tests for every route
Your current tests are a strong start, but your rubric requires at least one unit test per route whenever possible.

You have nine routes:
Unit test checklist

6 of 9 marked

Mark each route once you've verified its assert_equal() test.[x] index()
[ ] select_lessons()
[x] start_quiz()
[ ] quiz()
[x] submit_answer()
[x] time_up()
[x] next_question()
[ ] results()
[x] scoreboard()

The three routes I would prioritize testing directly are select_lessons(), quiz(), and results(). We should also test the new count_topic_questions() helper.

For example:
# Test the topic-counting helperassert_equal(    count_topic_questions(PRINT_QUESTIONS, "Print Statements"),    3)assert_equal(    count_topic_questions(IF_QUESTIONS, "If Statements"),    3)assert_equal(    count_topic_questions(PRINT_QUESTIONS, "If Statements"),    0)



6. One more important issue: your results page
Your results page currently displays the heading "Topic Results", but it doesn't actually calculate how many answers were correct for each topic.

This is a great opportunity to satisfy several requirements at once.

By adding per-topic results, we can:
- Use a meaningful for loop over Question objects.
- Add helper functions to keep your routes short.
- Make your results page match your original drawing.
- Add more meaningful assert_equal() tests.
- Give players useful feedback about which Python topics need more practice.
My recommendation
I would make these changes before submitting:
1. Add the meaningful question loop and use it on the results page.
2. Add docstrings to all nine routes.
3. Complete the missing route tests using assert_equal().
4. Verify the timer, scoring, navigation, and deployment by playing a full game.
One final caution: the code includes Timer(30000, "time_up"), but I haven't verified that this component works in your installed Drafter version. We should check it when testing the website, because the rubric makes a working deployment essential.

Bottom line: Speed Python already meets most of the functionality requirements, but I would not submit it yet. The loop, docstrings, complete tests, and runtime verification are the main things to address.

The next change I'd tackle is adding the per-topic results and the required loop together, since that improves your game while helping satisfy the rubric.
