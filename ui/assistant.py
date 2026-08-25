import streamlit as st
from typing import Dict, Any
from ai.ollama_client import ollama_client
from ai.prompts import CHAT_ASSISTANT_PROMPT_TEMPLATE
from rag.vector_store import get_vector_store

def render_ai_assistant(readiness_data: Dict[str, Any], student_dict: Dict[str, Any]):
    st.markdown("## 💬 AI Student Assistant (Context-Aware)")
    st.markdown(f"Conversational AI assistant tailored specifically to **{readiness_data.get('student_name')}** targeting **{readiness_data.get('target_role')}**.")

    if not ollama_client.is_available():
        st.warning("⚡ Local Ollama service is offline. AI Chat Assistant is operating in rule-based fallback mode. Start Ollama locally for rich conversational intelligence.")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Quick Suggestion Buttons
    st.markdown("**Quick Questions:**")
    q_cols = st.columns(3)
    preset_q = None
    with q_cols[0]:
        if st.button("Why is my readiness score low?"):
            preset_q = "Why is my career readiness score low and how can I fix it?"
    with q_cols[1]:
        if st.button("What project should I build next?"):
            preset_q = "What project should I build next to improve my portfolio?"
    with q_cols[2]:
        if st.button("What skills am I missing?"):
            preset_q = f"What key skills am I missing for a {readiness_data.get('target_role')} role?"

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input chat box
    user_input = st.chat_input("Ask Student360 AI anything about your portfolio or career...") or preset_q

    if user_input:
        # Display user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate Context-Aware Response
        high_gaps = [g['skill'] for g in readiness_data.get('skill_analysis', {}).get('high_priority_gaps', [])]
        acad = readiness_data.get('academic_analysis', {})
        proj = readiness_data.get('project_analysis', {})

        # Vector RAG search
        vector_store = get_vector_store()
        rag_results = vector_store.search(user_input, top_k=2)
        rag_context = "\n---\n".join([r['content'] for r in rag_results])

        prompt = CHAT_ASSISTANT_PROMPT_TEMPLATE.format(
            name=readiness_data.get('student_name'),
            department=student_dict.get('department', 'Computer Engineering'),
            semester=student_dict.get('semester', 7),
            target_role=readiness_data.get('target_role'),
            cgpa=acad.get('cgpa'),
            attendance=acad.get('avg_attendance'),
            career_score=readiness_data.get('career_readiness_score'),
            strengths=", ".join(readiness_data.get('strengths', [])),
            weaknesses=", ".join(readiness_data.get('weaknesses', [])),
            skill_gaps=", ".join(high_gaps) if high_gaps else "None",
            project_score=proj.get('overall_project_score'),
            deployed_count=proj.get('deployed_count'),
            intern_count=len(readiness_data.get('strengths', [])),
            cert_count=len(readiness_data.get('strengths', [])),
            rag_context=rag_context,
            user_question=user_input
        )

        with st.chat_message("assistant"):
            if ollama_client.is_available():
                with st.spinner("Student360 AI is thinking..."):
                    response = ollama_client.generate(prompt)
                    if not response:
                        response = generate_fallback_chat_answer(user_input, readiness_data)
            else:
                response = generate_fallback_chat_answer(user_input, readiness_data)

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

def generate_fallback_chat_answer(query: str, readiness_data: Dict[str, Any]) -> str:
    query_lower = query.lower()
    name = readiness_data.get('student_name')
    target_role = readiness_data.get('target_role')
    score = readiness_data.get('career_readiness_score')
    high_gaps = [g['skill'] for g in readiness_data.get('skill_analysis', {}).get('high_priority_gaps', [])]
    weaknesses = readiness_data.get('weaknesses', [])

    if "low" in query_lower or "score" in query_lower:
        return f"Hi {name}, your Career Readiness Score is currently **{score}/100** for the **{target_role}** role.\n\n" \
               f"**Primary factors holding your score back:**\n" + \
               "\n".join([f"- {w}" for w in weaknesses[:3]]) + \
               f"\n\nTo raise your score to 85+, focus on resolving your missing skills ({', '.join(high_gaps[:2])}) and deploying at least 1 project live!"

    elif "project" in query_lower or "build" in query_lower:
        return f"For a **{target_role}** role, I recommend building a **Containerized ML / REST Microservice Platform**.\n\n" \
               f"It will bridge your missing skills in **{', '.join(high_gaps[:3])}** and provide live deployment proof for recruiters."

    elif "skill" in query_lower or "missing" in query_lower:
        return f"Based on your target role as **{target_role}**, your top missing skills are:\n\n" + \
               "\n".join([f"1. **{g}** (High Priority Gap)" for g in high_gaps]) + \
               "\n\nI recommend starting with 1-2 hours of focused practice daily on these skills."

    return f"Hello {name}! As your Student360 AI Assistant, I analyzed your profile for **{target_role}**.\n\n" \
           f"Your current readiness score is **{score}/100**. Your main areas of improvement are: **{', '.join(high_gaps)}**. How else can I guide you today?"
