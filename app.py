import streamlit as st
import google.generativeai as genai
from PIL import Image
from pypdf import PdfReader
import docx
import io

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="AI learning assistant", page_icon="🎓", layout="wide")

# 2. SIDEBAR SETUP (API Key and File Uploads)
with st.sidebar:
    st.title("⚙️ Setup")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get an API key from [Google AI Studio](https://aistudio.google.com/)")
    
    st.markdown("---")
    st.header("📚 Study Materials")
    uploaded_file = st.file_uploader("Upload Notes (PDF/DOCX) or Problem (Image)", 
                                     type=["pdf", "docx", "jpg", "png", "jpeg"])
    
    document_context = ""
    image_data = None
    
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Handle Documents
        if file_extension == 'pdf':
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                document_context += page.extract_text() + "\n"
            st.success("PDF Content Loaded!")
            
        elif file_extension == 'docx':
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                document_context += para.text + "\n"
            st.success("Word Doc Content Loaded!")
            
        # Handle Images
        elif file_extension in ['jpg', 'jpeg', 'png']:
            image_data = Image.open(uploaded_file)
            st.image(image_data, caption="Uploaded Homework Image", use_column_width=True)

# 3. INITIALIZE CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hi! I'm your AI Tutor. Upload your notes or a photo of a problem, and let's solve it together!"
    })

# 4. MAIN INTERFACE
st.title("🎓 AI Tutor")
st.write("Use your own lecture notes to learn faster.")

# Display Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. CHAT INPUT AND PROCESSING
if user_input := st.chat_input("Ask a question about your study material..."):
    # Add user message to UI
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    if not api_key:
        st.error("Please provide an API key in the sidebar!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # THE PROMPT: This defines the AI's behavior
            system_instruction = f"""
            You are a world-class Socratic Tutor. 
            
            STUDY MATERIAL CONTEXT:
            {document_context if document_context else "No document uploaded yet."}
            
            INSTRUCTIONS:
            1. Use the provided context to guide your answers.
            2. NEVER give the full answer immediately. 
            3. Break down complex problems into steps.
            4. Ask the student a question to help them reach the next step.
            5. If they are totally stuck, give a solution, but also teach them how to approach similar problems.
            6. Be encouraging and patient.
            7. If the user provides a file or text and says summarize, summarize the key points directly without asking further questions.
            8. If the user uploads an image of a problem, analyze it and help them.
            9. only give the answer immediately if they are asking to summarize the document or if they explicitly ask for the solution.
            Remember, your goal is to help the student learn through guided questioning!
            10. Answer some questions direcltly, only if the question is it is fact-based like who is the president of a country or what is the capital of a state. or tell me the defintion of a word., or tell me about a historical event, a country, a person, etc."
            """

            # Initialize the model with instructions
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_instruction
            )

            # FORMAT HISTORY FOR GEMINI API (Strictly alternating User/Model)
            # We exclude the very last user message because we send it in chat.send_message()
            formatted_history = []
            for msg in st.session_state.messages[:-1]:
                # The first welcome message is assistant; Gemini calls this 'model'
                role = "user" if msg["role"] == "user" else "model"
                formatted_history.append({"role": role, "parts": [msg["content"]]})

            # START CHAT
            chat_session = model.start_chat(history=formatted_history)
            
            # PREPARE CONTENT (Include image if available)
            content_list = [user_input]
            if image_data:
                content_list.append(image_data)

            # GET RESPONSE
            with st.spinner("Analyzing..."):
                response = chat_session.send_message(content_list)
                ai_text = response.text

            # Update UI and History
            with st.chat_message("assistant"):
                st.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})

        except Exception as e:
            st.error(f"Error: {e}")
