import streamlit as st
import json



# Prompt Library
PROMPTS = {
    "Select a Prompt...": "",
    "Post-Conflict Recovery": "Act as an expert in post-conflict constitutional design. Review our current struggling metrics and propose 3 critical emergency stability measures.",
    "Eco-Democracy": "We are pivoting to a deeply ecological democracy. Suggest changes to the constitution that prioritize 'Environment Health' without tanking 'GDP'.",
    "AI Governance Model": "Evaluate our current regime type and metrics. How would transitioning to a fully Algorithmic Decision-Making (AI) Governance structure impact our 'Social Trust' and 'Democracy Score'?",
    "Techno-Libertarian": "Draft an actionable policy platform for a Techno-Libertarian state. Focus on maximizing 'Tech Innovation' and 'GDP' assuming minimal government.",
    "Nordic Social Democracy": "How can we safely transition our current setup toward a Nordic Social Democracy? Focus on stabilizing 'Income Inequality' and boosting 'Happiness Index'.",
    "Anarcho-Communalism": "Design a radical localized resource-sharing model where the central state is abolished. What immediate systemic risks do our current metrics predict?",
    "Authoritarian Crackdown": "Calculate the projected impact on 'Crime Rate' vs 'Press Freedom' if we declare martial law right now.",
    "Cultural Renaissance": "Determine an optimal strategy to massively inflate 'Culture' and 'Happiness Index' using our current 'GDP' buffer."
}

def call_mock_ai(prompt):
    return f"*[MOCKED CLAUDE AI RESPONSE]*\\n\\nBased on your prompt:\\n'{prompt}'\\n\\nI have analyzed the current society simulation metrics. Your Democracy Score is stable, but there are underlying issues in Social Trust. If you execute the requested transition, you may risk instability in GDP, but a long-term improvement in the Happiness Index. I recommend cautious incremental reforms rather than sweeping changes."

def call_ai(prompt):
    return call_mock_ai(prompt)

def render():
    st.header("🤖 AI Governance Analysis")
    st.write("Generate high-level strategy reports or chat interactively with an AI Constitutional Advisor.")

    if "history" not in st.session_state or not st.session_state.history:
        st.warning("Simulation state not initialized.")
        return

    hist = st.session_state.history
    current_state = hist[-1]
    state_str = json.dumps(current_state, indent=2)



    sys_prompt = f"You are a Constitutional Economics & Governance AI Advisor. Analyze the following current state of the nation:\\n{state_str}"

    tab1, tab2 = st.tabs(["Preset Analysis Reports", "Live Governance Chat"])

    with tab1:
        st.subheader("Generate Governance Reports")
        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)
        
        btn_1 = c1.button("+ Governance Report", use_container_width=True)
        btn_2 = c2.button("+ Crisis Risk", use_container_width=True)
        btn_3 = c3.button("+ Economic Analysis", use_container_width=True)
        btn_4 = c4.button("+ Democracy Health Check", use_container_width=True)
        btn_5 = c5.button("+ Demographic Stability", use_container_width=True)
        btn_6 = c6.button("+ Foreign Policy Draft", use_container_width=True)
        
        preset_prompt = ""
        if btn_1: preset_prompt = "Generate a comprehensive Governance Report prioritizing system stability."
        elif btn_2: preset_prompt = "Identify the top 3 critical failure risks based on our current metrics."
        elif btn_3: preset_prompt = "Generate a deep-dive Economic Analysis focusing on GDP vs Inequality."
        elif btn_4: preset_prompt = "Run a Democracy Health check. Are we backsliding?"
        elif btn_5: preset_prompt = "Assess demographic stability based on Crime, Education, and Healthcare."
        elif btn_6: preset_prompt = "Draft a foreign policy strategy given our Military Power and GDP."

        if preset_prompt:
            with st.spinner("Analyzing..."):
                response = call_ai(preset_prompt)
                st.markdown("### AI Report")
                st.write(response)
                st.download_button("Download Report as text", data=response, file_name="ai_analysis_report.txt", mime="text/plain")

    with tab2:
        st.subheader("Interactive Strategy Chat")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Prompt Library Injection
        st.write("📖 **Prompt Library:**")
        selected_prompt = st.selectbox("Inject a template into the chat:", list(PROMPTS.keys()))
        
        # Display chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat Input
        if user_msg := st.chat_input("Ask advice or simulate a policy..."):
            # Append user message
            st.session_state.messages.append({"role": "user", "content": user_msg})
            with st.chat_message("user"):
                st.markdown(user_msg)

            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Consulting..."):
                    result = call_ai(user_msg)
                    st.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})

        if selected_prompt and selected_prompt != "Select a Prompt...":
            st.info(f"💡 Suggestion: Copy/paste this: \\n*{PROMPTS[selected_prompt]}*")
