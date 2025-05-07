import os  # Needed for secret key
import random

from flask import Flask, render_template, request, session

from config import settings

app = Flask(__name__)
# A secret key is needed to use sessions
# Use a strong, random key in production. For development, os.urandom(24) is fine.
app.secret_key = os.urandom(24)


def generate_questions(num_questions=None, multiply_by=None, division_prob=None):
    """Generates a list of multiplication questions with answers."""
    # Use settings if parameters are not provided
    num_questions = (
        num_questions if num_questions is not None else settings.num_questions
    )
    multiply_by = multiply_by if multiply_by is not None else settings.multiply_by
    division_prob = (
        division_prob if division_prob is not None else settings.division_prob
    )

    questions = []
    already_asked = set()
    while len(questions) < num_questions:
        a = random.choices(multiply_by[0], multiply_by[1])[0] or random.randint(1, 10)
        b = random.randint(1, 10)
        if random.random() < division_prob:
            if (a, b, "divide") in already_asked:
                continue
            questions.append(
                {
                    "a": a,
                    "b": b,
                    "question_str": f"{a*b} ÷ {a} = ",
                    "answer": b,
                }
            )
            already_asked.add((a, b, "divide"))
            continue
        if multiply_by and random.random() < 0.5:
            a, b = b, a
        if (a, b, "mutiply") in already_asked:
            continue
        already_asked.add((a, b, "multiply"))
        correct_answer = a * b
        questions.append(
            {"a": a, "b": b, "question_str": f"{a} x {b} = ", "answer": correct_answer}
        )
    return questions


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    show_reward = False
    reward_gif_url = None  # Initialize reward GIF URL

    if request.method == "POST":
        user_answers_str = request.form.getlist("answers")
        stored_questions = session.get("questions", [])

        if not stored_questions:
            # Should not happen if session is working, but handle defensively
            result = "Error: Could not find the questions. Please try again."
            questions = generate_questions()
            session["questions"] = questions
            return render_template(
                "index.html",
                questions=questions,
                result=result,
                show_reward=show_reward,
                reward_gif_url=reward_gif_url,
            )

        if len(user_answers_str) != len(stored_questions):
            result = "Error: Number of answers submitted does not match the number of questions."
            questions_for_template = stored_questions
            session["questions"] = stored_questions  # Re-store just in case
            return render_template(
                "index.html",
                questions=questions_for_template,
                result=result,
                show_reward=show_reward,
                reward_gif_url=reward_gif_url,
            )

        all_correct = True
        try:
            for i, user_answer_str in enumerate(user_answers_str):
                user_answer = int(user_answer_str)  # Convert user input to integer
                if user_answer != stored_questions[i]["answer"]:
                    all_correct = False
                    break  # No need to check further
        except ValueError:
            # Handle cases where input is not a valid number
            all_correct = False
            result = "Please enter valid numbers for all answers."

        if result is None:  # Only set default messages if no error occurred above
            if all_correct:
                # Only need to set reward info, not result message
                show_reward = True
                reward_gif_url = random.choice(
                    settings.reward_gifs
                )()  # Select random GIF on success

        # Generate new questions for the next round regardless of correctness
        questions = generate_questions()
        session["questions"] = questions
        return render_template(
            "index.html",
            questions=questions,
            result=result,
            show_reward=show_reward,
            reward_gif_url=reward_gif_url,
        )

    else:
        # Initial GET request
        questions = generate_questions()
        session["questions"] = questions  # Store questions and answers in session
        # No reward on initial load
        return render_template(
            "index.html",
            questions=questions,
            result=None,
            show_reward=False,
            reward_gif_url=None,
        )


if __name__ == "__main__":
    # Use settings for Flask configuration
    app.run(port=settings.port, debug=settings.debug, host=settings.host)
