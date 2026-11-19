# Build Your First AI Chatbot (Groq)

SDIT × IEEE peer learning session, 19 Nov 2026

## 1. Get an API key
1. Go to https://console.groq.com/keys and sign in (it's free).
2. Click **Create API Key**.
3. Copy the key. It starts with `gsk_`.

## 2. Install
```
pip install -r requirements.txt
```

## 3. Fill in the .env file
Open the **.env** file and change:
- `GROQ_API_KEY` to your key
- `SYSTEM_PROMPT` to your bot's personality (keep the double quotes)

If you got this project from GitHub, there is no `.env` yet. Copy `.env.example`, rename the copy to `.env`, then fill it in.

`.gitignore` keeps `.env` off GitHub, so your key stays private.
The chatbot reads the key directly from `.env`; you do not need to add it to Windows environment variables.

## 4. Run
| Version | Command | Where to chat |
|---|---|---|
| Terminal | `python chatbot.py` | The terminal window |
| Web | `python chatbot_web.py` | Open http://127.0.0.1:7860 in your browser |

## System prompt ideas
- "You are a strict but kind maths tutor. Never give the answer directly; give hints."
- "You are a Mangaluru food guide. Recommend local dishes like neer dosa and ghee roast."
- "You are a career coach for engineering students. Ask one question at a time."
- "You talk like a pirate, but your answers are still correct."

## Common errors
| Error | Fix |
|---|---|
| `401` / `Incorrect API key` | Re-copy the key and check for extra spaces |
| "Please put your API key in the .env file" | Make sure the file is named exactly `.env` (not `.env.txt`) and is in the same folder |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `429` / rate limit | Wait a few seconds or free-tier limits are per minute; check console.groq.com |
| `model not found` | Check the model names at https://console.groq.com/docs/models |

**Never upload your API key to GitHub or share it in a group chat.**
