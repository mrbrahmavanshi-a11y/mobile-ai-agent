import os
import sys
import time
from google import genai

# 1. Free Gemini API Key Setup
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY set nahi hai. Pehle export GEMINI_API_KEY='your_key' chalayein.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# Agent Name
AGENT_NAME = "Jarvis"

def ask_gemini_for_adb(user_prompt):
    """
    User ki command ko direct Android ADB command me badalta hai (Free Tier)
    """
    system_instruction = """
    You are an Android OS automation AI Agent. Translate the user request into a valid Android ADB shell command.
    Return ONLY the raw ADB shell command (e.g., 'input keyevent 26', 'am start -a android.intent.action.VIEW', 'input tap 500 500').
    Do NOT include markdown backticks, 'adb shell' prefix, or any conversational text.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_instruction}\nUser Request: {user_prompt}"
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def main():
    print("=========================================")
    print(f"   🤖 {AGENT_NAME} FREE AI AGENT ONLINE")
    print("=========================================")
    print("Example commands: 'open whatsapp', 'volume up', 'lock screen', 'exit'")
    
    while True:
        try:
            user_input = input(f"\n{AGENT_NAME} ko command do > ")
            if user_input.lower() in ['exit', 'quit', 'stop']:
                print(f"{AGENT_NAME}: Goodbye!")
                break
            
            if not user_input.strip():
                continue

            print("Processing command with Gemini Free API...")
            raw_adb = ask_gemini_for_adb(user_input)

            if raw_adb:
                print(f"[Generated ADB Action]: adb shell {raw_adb}")
                # Phone par action execute karein
                os.system(f"adb shell {raw_adb}")
            else:
                print("Could not generate ADB command.")

        except KeyboardInterrupt:
            print(f"\n{AGENT_NAME}: Shutting down...")
            break

if __name__ == "__main__":
    main()
