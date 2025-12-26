from flask import Flask, render_template, request
from utils.gemini import generate_response
from utils.summarizer import summarize_text
from utils.quiz import generate_quiz
from utils.file_reader import extract_text_from_pdf, extract_text_from_docx
from flask import session


app = Flask(__name__)
app.secret_key = "hackathon-secret-key"


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/summarizer", methods=["GET", "POST"])
def summarizer():
    summary = ""
    extracted_text = ""

    if request.method == "POST":
        text_input = request.form.get("text")
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename != "":
            filename = uploaded_file.filename.lower()

            if filename.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif filename.endswith(".docx"):
                extracted_text = extract_text_from_docx(uploaded_file)
            else:
                summary = "Unsupported file format. Please upload a PDF or DOCX."
                return render_template("summarizer.html", summary=summary)

        else:
            extracted_text = text_input

        summary = summarize_text(extracted_text)

    return render_template("summarizer.html", summary=summary)



@app.route("/tutor", methods=["GET", "POST"])
def tutor():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        # Clear chat
        if request.form.get("clear") == "true":
            session["chat_history"] = []
            return render_template("tutor.html", chat=session["chat_history"])

        user_question = request.form.get("question")

        session["chat_history"].append({
            "role": "user",
            "content": user_question
        })

        # Build conversation context
        conversation = "You are an AI tutor. Answer clearly and step-by-step.\n\n"

        for msg in session["chat_history"]:
            conversation += f"{msg['role'].capitalize()}: {msg['content']}\n"

        ai_reply = generate_response(conversation)

        session["chat_history"].append({
            "role": "ai",
            "content": ai_reply
        })

    return render_template("tutor.html", chat=session["chat_history"])



@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    quiz_data = ""
    if request.method == "POST":
        topic = request.form.get("topic")
        quiz_data = generate_quiz(topic)
    return render_template("quiz.html", quiz=quiz_data)

if __name__ == "__main__":
    app.run(debug=True)
