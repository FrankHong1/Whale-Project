from openai import OpenAI
import os

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def reply(response):
  reply = response.choices[0].message.content
  return reply

def chatting():
  msg_history = []
  system_msg = input("What type of chatbot would you like to create?\nUser: ")
  msg_history.append({"role": "system", "content": system_msg})
  print("Bot: Your new assistant is ready, feel free to ask me anything!\nType 'exit' to end the chat\n")

  while True:
    user_msg = input("\nUser: ")
    if user_msg.lower() in ["bye", "exit", "quit", "done", "stop"]:
      break
    msg_history.append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(
      model = "gpt-4o",
      messages = msg_history
    )
    ext_reply = reply(response)
    msg_history.append({"role": "assistant", "content": ext_reply})
    print(f"\nBot: {ext_reply}")

  print("\nBot: Goodbye!")
  return None

if __name__ == "__main__":
  chatting()