import os  # Needed for secret key
import random

from flask import Flask, render_template, request, session

app = Flask(__name__)
# A secret key is needed to use sessions
# Use a strong, random key in production. For development, os.urandom(24) is fine.
app.secret_key = os.urandom(24)

# List of cute animal GIF URLs
REWARD_GIFS = ["https://cataas.com/cat/gif"]


def generate_questions(num_questions=3):
    """Generates a list of multiplication questions with answers."""
    questions = []
    for _ in range(num_questions):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
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
                    REWARD_GIFS
                )  # Select random GIF on success

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
    # Added host='0.0.0.0' to make it accessible on the network if needed
    # Added debug=True for development ease
    # Changed port back to default 5000 for simplicity, can be changed if needed
    app.run(port=5000, debug=True, host="0.0.0.0")
