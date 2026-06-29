import streamlit as st

from main import agent_loop



# -----------------------------
# Page Setup
# -----------------------------


st.set_page_config(

    page_title="Weather AI",

    page_icon="🌦️",

    layout="centered"

)



# -----------------------------
# Style
# -----------------------------


st.markdown(

"""

<style>


body{

background:#0e1117;

}


.user{

background:#262730;

padding:15px;

border-radius:10px;

margin:10px;

}


.bot{

background:#075985;

padding:15px;

border-radius:10px;

margin:10px;

}


</style>


""",

unsafe_allow_html=True

)



# -----------------------------
# Title
# -----------------------------


st.title(
"🌦️ Weather AI Assistant"
)


st.caption(
"OpenRouter + OpenWeather + Streamlit"
)




# -----------------------------
# Memory
# -----------------------------


if "messages" not in st.session_state:

    st.session_state.messages=[]




# -----------------------------
# Display Chat
# -----------------------------


for msg in st.session_state.messages:


    if msg["role"]=="user":


        st.markdown(

        f"""

        <div class='user'>

        👤 <b>You</b><br>

        {msg['content']}

        </div>

        """,

        unsafe_allow_html=True

        )


    else:


        st.markdown(

        f"""

        <div class='bot'>

        🤖 <b>AI</b><br>

        {msg['content']}

        </div>

        """,

        unsafe_allow_html=True

        )





# -----------------------------
# Input
# -----------------------------


question = st.chat_input(
"Ask weather..."
)



if question:


    st.session_state.messages.append(

    {
    "role":"user",
    "content":question
    }

    )


    with st.spinner(
        "Checking weather..."
    ):


        try:

            answer = agent_loop(question)


        except Exception as e:

            answer = (
                "Error: "
                + str(e)
            )



    st.session_state.messages.append(

    {
    "role":"assistant",
    "content":answer
    }

    )


    st.rerun()




# -----------------------------
# Sidebar
# -----------------------------


with st.sidebar:


    st.header(
        "🌦️ Weather AI"
    )


    st.write(
        "Features:"
    )


    st.success(
        "OpenRouter"
    )


    st.success(
        "OpenWeather"
    )


    st.success(
        "Tool Calling"
    )


    if st.button(
        "Clear Chat"
    ):


        st.session_state.messages=[]

        st.rerun()