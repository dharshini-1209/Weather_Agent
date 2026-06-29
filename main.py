import os
import json
import requests

from dotenv import load_dotenv

from tools import get_weather
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT


# -----------------------------
# Load Environment
# -----------------------------

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


if not OPENROUTER_API_KEY:
    raise Exception(
        "OPENROUTER_API_KEY missing. Check .env file"
    )


MODEL = "openai/gpt-4o-mini"

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)



# -----------------------------
# Tool Definition
# -----------------------------

TOOLS = [

{
"type":"function",

"function":{

"name":"get_weather",

"description":
"Get current weather information for a city",

"parameters":{

"type":"object",

"properties":{

"city":{
"type":"string",
"description":"City name"
}

},

"required":[
"city"
]

}

}

}

]



# -----------------------------
# Tool Mapping
# -----------------------------


TOOL_FUNCTIONS = {

"get_weather": get_weather

}




# -----------------------------
# Call LLM
# -----------------------------


def call_llm(messages):


    headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8501",
    "X-Title": "Weather AI Agent"
}



    payload = {

        "model":MODEL,

        "messages":messages,

        "tools":TOOLS

    }



    response = requests.post(

        OPENROUTER_URL,

        headers=headers,

        json=payload

    )


    if response.status_code != 200:

        print(response.text)

        raise Exception(
            f"OpenRouter Error {response.status_code}"
        )


    return response.json()




# -----------------------------
# Execute Tool
# -----------------------------


def run_tool(tool_call):


    name = tool_call["function"]["name"]


    args = json.loads(

        tool_call["function"]["arguments"]

    )


    if name in TOOL_FUNCTIONS:


        result = TOOL_FUNCTIONS[name](**args)


        return str(result)


    return "Tool not found"





# -----------------------------
# Agent Loop
# -----------------------------


def agent_loop(user_input):


    memory = load_memory()


    messages = [

        {
        "role":"system",
        "content":SYSTEM_PROMPT
        }

    ]


    messages.extend(memory)


    messages.append(

        {
        "role":"user",
        "content":user_input
        }

    )



    for step in range(5):


        response = call_llm(messages)


        message = response["choices"][0]["message"]


        messages.append(message)



        if message.get("tool_calls"):


            for tool_call in message["tool_calls"]:


                result = run_tool(tool_call)



                messages.append(

                {

                "role":"tool",

                "tool_call_id":
                tool_call["id"],

                "name":
                tool_call["function"]["name"],

                "content":
                result

                }

                )


        else:


            answer = message.get(
                "content",
                "No response"
            )


            save_memory(messages[1:])


            return answer



    return "Maximum steps reached"





# -----------------------------
# Terminal Test
# -----------------------------


if __name__ == "__main__":


    print("🌦️ Weather AI Agent Started")

    print("Type exit to quit")


    while True:


        question = input("\nYou: ")


        if question.lower()=="exit":

            break


        try:

            print(

            "\nAI:",

            agent_loop(question)

            )


        except Exception as e:

            print(
            "Error:",
            e
            )