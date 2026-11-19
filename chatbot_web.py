# =====================================================================
#   BUILD YOUR FIRST AI CHATBOT  -  Web (browser) version
#   Peer Learning Session | SDIT x IEEE | 19 Nov 2026
# ---------------------------------------------------------------------
#   Same chatbot as chatbot.py, but with a nice chat window that
#   opens in your web browser - like a mini ChatGPT / Groq app!
#
#   YOU ONLY NEED TO FILL IN 2 THINGS, inside the  .env  file:
#     1. GROQ_API_KEY   -> the "password" that lets you use Groq
#     2. SYSTEM_PROMPT  -> the "personality / job" of your bot
#
#   HOW TO RUN:
#     pip install -r requirements.txt
#     python chatbot_web.py
#   Then open the link it prints (usually http://127.0.0.1:7860)
# =====================================================================


# ---------------------------------------------------------------------
# Two ready-made helper libraries:
#   openai -> talks to Groq (Groq uses the same format as OpenAI)
#   gradio -> builds the chat web page for us automatically
# ---------------------------------------------------------------------
from openai import OpenAI
import gradio as gr


# ---------------------------------------------------------------------
# Read settings from .env without adding them to Windows environment variables.
# ---------------------------------------------------------------------
from pathlib import Path
from dotenv import dotenv_values


# =====================================================================
#   STEP 1:  YOUR SETTINGS LIVE IN THE  .env  FILE  (not here!)
# ---------------------------------------------------------------------
#   Open the file called  .env  (in the same folder) and fill in:
#     GROQ_API_KEY   -> your secret key from https://console.groq.com/keys
#     SYSTEM_PROMPT  -> the personality / job of your bot
#   Why? So you can share this code on GitHub without leaking your key.
# =====================================================================

settings = dotenv_values(Path(__file__).with_name(".env"))

# Grab the two values from .env ("" = use empty text if missing).
API_KEY = (settings.get("GROQ_API_KEY") or "").strip()
SYSTEM_PROMPT = settings.get("SYSTEM_PROMPT") or "You are a friendly and helpful assistant develop by shriketh . I'm here to help you answer questions,provide information ,solve problem ,explain concepts,and assist you with various tasks."

# =====================================================================
#   (Optional) Settings you CAN change, but don't have to
# =====================================================================

MODEL_NAME = "openai/gpt-oss-120b"  # or "openai/gpt-oss-20b" (faster)
TEMPERATURE = 0.7                # 0 = serious, 1 = more creative
BOT_NAME = "My First AI Chatbot" # Title shown at the top of the page
SHARE_LINK = False               # True = get a public link friends can open


# =====================================================================
#   STEP 2:  THE ACTUAL CHATBOT  (no need to touch anything below)
# =====================================================================

# Connect to Groq's servers (base_url = Groq's internet address).
client = OpenAI(
    api_key=API_KEY or "missing-key",  # placeholder so the friendly check below can run
    base_url="https://api.groq.com/openai/v1",
)


def respond(user_message, history):
    """
    Gradio calls this every time you hit Send.
      user_message -> what you just typed
      history      -> all earlier messages in this chat (Gradio keeps it)
    We send everything to Groq and show its reply word-by-word.
    """

    # 1. Start with the bot's instructions (system prompt)...
    messages = [{"role": "system", "content": SYSTEM_PROMPT.strip()}]

    # 2. ...then add the earlier chat so the bot "remembers" it...
    for old in history:
        # Older Gradio versions store each turn as a pair: [your msg, bot reply]
        if isinstance(old, (list, tuple)):
            user_text, bot_text = old
            if user_text:
                messages.append({"role": "user", "content": str(user_text)})
            if bot_text:
                messages.append({"role": "assistant", "content": str(bot_text)})
            continue

        # Newer Gradio stores each message as {"role": ..., "content": ...}
        text = old["content"]
        # Sometimes the text is split into pieces - join them into one string.
        if isinstance(text, list):
            text = " ".join(p.get("text", "") for p in text if isinstance(p, dict))
        messages.append({"role": old["role"], "content": str(text)})

    # 3. ...and finally the new message you just typed.
    messages.append({"role": "user", "content": user_message})

    try:
        # stream=True makes the reply appear word-by-word (typing effect)
        # instead of waiting for the whole answer at once.
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            stream=True,
        )

        reply = ""
        for chunk in stream:
            # Each "chunk" is a small piece of the answer. Glue them together.
            if chunk.choices and chunk.choices[0].delta.content:
                reply += chunk.choices[0].delta.content
                yield reply  # update the chat window with what we have so far

    except Exception as error:
        # If something fails (wrong key, no internet), show it in the chat.
        yield f"⚠️ Something went wrong: {error}\n\nCheck your API key and internet."


# Build the chat web page. Gradio gives us the text box, Send button,
# chat bubbles - everything - in just this one block.
app = gr.ChatInterface(
    fn=respond,
    title=BOT_NAME,
    description=f"Powered by {MODEL_NAME} on Groq • SDIT x IEEE Workshop",
    examples=["Hi! Who are you?", "Explain AI like I'm 10", "Give me a fun fact"],
)


# Start the web app when this file is run.
if __name__ == "__main__":
    if not API_KEY or API_KEY.startswith("paste-"):
        print("Oops! Please put your API key in the .env file (GROQ_API_KEY=...).")
    else:
        app.launch(share=SHARE_LINK)
