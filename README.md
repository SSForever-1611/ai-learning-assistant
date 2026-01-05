# ai-learning-assistant

An AI-powered teaching assistant built for December AI Challenge. This tool uses Google Gemini API Key to help students learn from their own notes using the Socratic method.

##  Features
- **Socratic Method:** Doesn't give answers directly; asks guiding questions.
- **RAG (Document Analysis):** Upload PDF/DOCX lecture notes to get personalized help, or summarize.
- **Multimodal:** Upload images of handwritten math or science problems.


## Tech Stack
- Streamlit used for interface
- Gemini API key for AI model
- The model uses a specific prompt for students

## Future Improvements
- I would add a Voice feature
- Performance improvements such as speed, a better prompt.
- UI enhancements
- add specific AI models for specific topics for students


##  Installation
1. Clone the repo:
   `git clone https://github.com/SSForever-1611/ai-learning-assistant.git`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the app:
   `streamlit run app.py`
