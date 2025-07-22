import streamlit as st
from rag_pipeline.rag import rag, vector_search, build_prompt, llm  # Import your RAG functions

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ratings" not in st.session_state:
    st.session_state.ratings = {}

st.title("🔍 Ask My Resume")

# Sidebar controls
st.sidebar.header("Retriever Settings")
section_options = ["Work Experience", "Projects", "Skills", "Education"]
selected_sections = st.sidebar.multiselect("Filter by Section", section_options, default=section_options)
top_k = st.sidebar.slider("Number of Chunks to Retrieve", min_value=1, max_value=5, value=5)
model_options = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"]
selected_model = st.sidebar.selectbox("Select Model", model_options)

# Chat Interface
user_input = st.chat_input("Ask a question about the resume")
if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get search results & response
    with st.spinner("Thinking..."):
        results = vector_search(user_input, sections=selected_sections, limit=top_k)
        answer = rag(user_input, sections=selected_sections, llm_model=selected_model, limit=top_k)

    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": results})

import uuid

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("Sources Used"):
                for j, doc in enumerate(msg["sources"], 1):
                    section = doc.get("section", "Unknown")
                    text = doc.get("text", "")
                    st.markdown(f"**{j}. [{section}]** {text}")
            
            # Rating option
            #unique_key = str(uuid.uuid4())  # generates a truly unique ID
            message_id = f"msg_{i}"
            #current_rating = st.session_state.ratings.get(message_id, None)

            rating = st.radio(
                "Rate this answer:",
                ["👍+1", "👎-1"],
                index=["👍+1", "👎-1"].index(st.session_state.ratings.get(message_id, "👍+1")),
                key=f"rating_{message_id}"
            )

            # Save rating to session_state
            st.session_state.ratings[message_id] = rating

            #st.markdown(f"You selected: **{rating}**")
        # TODO: Save feedback to file or database
        # save_feedback(question=user_input, answer=answer, rating=rating)

st.markdown("---")
#st.markdown("Made with using Qdrant, Groq, and Streamlit")
