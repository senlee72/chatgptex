from datetime import datetime

import pandas as pd
import streamlit as st

user_avatar = "😄"
assistant_avatar = "😙"

def display_conversation(conversation_history):
    for message in conversation_history:
        avatar = user_avatar if message["role"] == "user" else assistant_avatar

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

            if "api_cal_cost" in message:
                st.caption(f"Cost: US${message['api_call_cost']:.5f}")




def clear_conversation():
    """Clear the conversation history."""
    if (
        st.button("🧹 Clear conversation", use_container_width=True)
        or "conversation_history" not in st.session_state
    ):
        st.session_state.conversation_history = []
        st.session_state.total_cost = 0

def download_conversation():
    """Download the conversation history as a CSV file."""
    conversation_df = pd.DataFrame(
        st.session_state.conversation_history, columns=["role", "content"]
    )
    csv = conversation_df.to_csv(index=False)

    st.download_button(
        label="💾 Download conversation",
        data=csv,
        file_name=f"conversation_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

def calc_cost(token_usage):
    # https://openai.com/pricing

    return (token_usage["prompt_tokens"] * 0.0015 / 1000) + (
        token_usage["completion_tokens"] * 0.002 / 1000
    )    