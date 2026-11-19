# =====================================================================
#   BUILD YOUR FIRST AI CHATBOT  -  Terminal version
#   Peer Learning Session | SDIT x IEEE | 19 Nov 2026
# ---------------------------------------------------------------------
#   This program lets you chat with an AI model hosted on Groq
#   (a super-fast AI service) right inside your terminal.
#
#   YOU ONLY NEED TO FILL IN 2 THINGS, inside the  .env  file:
#     1. GROQ_API_KEY   -> the "password" that lets you use Groq
#     2. SYSTEM_PROMPT  -> the "personality / job" of your bot
#
#   HOW TO RUN:
#     pip install -r requirements.txt
#     python chatbot.py
#
#   Type your message and press Enter. Type  bye  to quit.
# =====================================================================


# ---------------------------------------------------------------------
# We borrow a ready-made helper library called "openai".
# Groq's API speaks the same "language" as OpenAI's, so this
# library works with Groq too - we just point it at Groq's address.
# ---------------------------------------------------------------------
from openai import OpenAI


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

# Which AI "brain" to use. gpt-oss-120b is a free, open model from
# OpenAI that Groq runs super fast. For even faster (smaller) answers,
# try "openai/gpt-oss-20b".
MODEL_NAME = "openai/gpt-oss-120b"

# Creativity dial: 0 = serious & predictable, 1 = more creative & random.
TEMPERATURE = 0.7

# The name shown before the bot's replies.
BOT_NAME = "AI Bot"


# =====================================================================
#   STEP 2:  THE ACTUAL CHATBOT  (no need to touch anything below)
# =====================================================================

# Create a "client" = a connection to Groq's servers.
# base_url is simply the internet address where Groq lives.
client = OpenAI(
    api_key=API_KEY or "missing-key",  # placeholder so the friendly check below can run
    base_url="https://api.groq.com/openai/v1",
)

# The bot has no memory of its own. So we keep the whole conversation
# in a list and send it EVERY time - that's how it "remembers"
# what you said earlier.
# We start the list with the system prompt (the bot's instructions).
conversation = [
    {"role": "system", "content": SYSTEM_PROMPT.strip()}
]


def ask_ai(user_message):
    """Send the user's message to Groq and return Groq's reply."""

    # 1. Add what the user just typed to the conversation history.
    conversation.append({"role": "user", "content": user_message})

    # 2. Send the full conversation to Groq and wait for its answer.
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=conversation,
        temperature=TEMPERATURE,
    )

    # 3. Pull out just the text of the reply from the response.
    reply = response.choices[0].message.content

    # 4. Save the bot's reply in the history too, so it remembers it.
    conversation.append({"role": "assistant", "content": reply})

    return reply


def main():
    """Runs the chat loop: read message -> ask Groq -> print reply."""

    # Friendly check: stop early if the API key was never filled in.
    if not API_KEY or API_KEY.startswith("paste-"):
        print("Oops! Please put your API key in the .env file (GROQ_API_KEY=...).")
        return

    print("=" * 55)
    print(f"  {BOT_NAME} is ready! Type 'bye' to exit.")
    print("=" * 55)

    # "while True" means: keep repeating forever, until we say stop.
    while True:
        user_message = input("\nYou: ").strip()

        # Skip empty messages (user just pressed Enter).
        if not user_message:
            continue

        # Exit words - end the chat politely.
        if user_message.lower() in ("bye", "exit", "quit"):
            print(f"\n{BOT_NAME}: Goodbye! 👋")
            break

        # "try / except" = try to do this, and if something goes
        # wrong (no internet, wrong key...), show a message instead
        # of crashing the whole program.
        try:
            reply = ask_ai(user_message)
            print(f"\n{BOT_NAME}: {reply}")
        except Exception as error:
            # Remove the message that failed, so history stays clean.
            conversation.pop()
            print(f"\n⚠️  Something went wrong: {error}")
            print("   Check your API key and internet connection.")


# This line means: "start the chatbot when this file is run".
if __name__ == "__main__":
    main()
