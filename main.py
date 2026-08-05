import tkinter as tk
from tkinter import scrolledtext
import random
import pyttsx3

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Speed of speech

def speak(text):
    """Helper function to make PyPro read answers and questions out loud"""
    clean_text = (
        text.replace("💡", "")
            .replace("Example:", "For example:")
            .replace("🎮", "")
            .replace("✅", "")
            .replace("❌", "")
            .replace("print(", "print ")
            .replace("'", "")
            .replace('"', "")
            .replace("=", " equals ")
    )
    engine.say(clean_text)
    engine.runAndWait()

# 1. Enhanced Knowledge Base with Definitions & Code Examples
responses = {
    "python": "Python is a high-level, interpreted programming language known for its simple syntax and readability.\n💡 Example:\nprint('Hello, DecodeLabs!')",
    
    "list": "Lists are ordered and mutable sequences.\n💡 Example:\nmy_list = ['apple', 'banana', 'cherry']\nmy_list.append('date')",
    
    "dictionary": "A dictionary stores data as key-value pairs and provides fast O(1) average lookup time.\n💡 Example:\nstudent = {'name': 'Alice', 'score': 95}\nprint(student['name'])",
    
    "function": "A function is a reusable block of code that performs a specific task.\n💡 Example:\ndef greet(name):\n    return f'Hello, {name}!'",
    
    "recursion": "Recursion is when a function calls itself. Always include a base case to prevent infinite loops!\n💡 Example:\ndef countdown(n):\n    if n <= 0:  # Base case\n        print('Done!')\n    else:\n        print(n)\n        countdown(n - 1)",
    
    "big-o": "Big-O notation describes time/space complexity as input size grows. Dictionaries give O(1) constant time lookups.",
    
    "class": "A class is a blueprint for creating objects.\n💡 Example:\nclass Car:\n    def __init__(self, brand):\n        self.brand = brand\nmy_car = Car('Tesla')",
    
    "inheritance": "Inheritance allows one class to acquire properties of another class.\n💡 Example:\nclass Animal:\n    pass\nclass Dog(Animal):\n    pass",
    
    "exception": "Exceptions handle runtime errors gracefully.\n💡 Example:\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero!')",
    
    "file": "Python uses open() to read and write files safely with 'with'.\n💡 Example:\nwith open('data.txt', 'w') as f:\n    f.write('Hello World')",
    
    "api": "An API allows different software applications to communicate using methods like GET and POST.",
    
    "sql": "SQL is used to manage relational databases.\n💡 Example:\nSELECT * FROM users WHERE age > 18;",
    
    "git": "Git tracks changes in software projects.\n💡 Example:\ngit add .\ngit commit -m 'Initial commit'",
    
    "project": "Be prepared to explain your projects, your role, technologies used, and challenges solved.",
    
    "help": "Try asking about: python, list, dictionary, function, recursion, big-o, class, inheritance, exception, file, api, sql, git, or project. \n🎮 Type '/quiz' to start a mock interview test!"
}

fallback = "I couldn't find that topic. Type 'help' to see available topics or '/quiz' to test your skills."

# Quiz State Variables
quiz_active = False
quiz_score = 0
quiz_total = 0
current_quiz_question = ""
quiz_questions = [
    ("python", "What is Python known for?"),
    ("list", "Are lists mutable or immutable?"),
    ("dictionary", "What time complexity do dictionaries give for average lookups?"),
    ("recursion", "What must every recursive function have to avoid infinite loops?"),
    ("class", "What is a blueprint for creating objects called?")
]

def send_message(event=None):
    global quiz_active, quiz_score, quiz_total, current_quiz_question
    
    user_text = user_entry.get().strip()
    if not user_text:
        return
    
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_text}\n", "user_tag")
    
    clean_input = user_text.lower()
    reply = ""
    
    if quiz_active and clean_input == "exit quiz":
        quiz_active = False
        reply = f"Quiz ended! Your final score: {quiz_score}/{quiz_total}. Type 'help' for normal mode."
    
    elif quiz_active:
        quiz_total += 1
        if current_quiz_question in clean_input:
            quiz_score += 1
            reply = f"✅ Correct! (Score: {quiz_score}/{quiz_total})\n\n"
        else:
            reply = f"❌ Not quite. The key concept was related to '{current_quiz_question}'. (Score: {quiz_score}/{quiz_total})\n\n"
        
        next_q = random.choice(quiz_questions)
        current_quiz_question = next_q[0]
        reply += f"Next Question: {next_q[1]}\n(Type 'exit quiz' to quit)"
        
    elif clean_input == "/quiz" or clean_input == "quiz":
        quiz_active = True
        quiz_score = 0
        quiz_total = 0
        first_q = random.choice(quiz_questions)
        current_quiz_question = first_q[0]
        reply = f"🎮 Quiz Mode Activated!\nQuestion: {first_q[1]}\n(Type your answer or type 'exit quiz' to quit)"
        
    else:
        reply = fallback
        for keyword in responses:
            if keyword in clean_input:
                reply = responses[keyword]
                break
            
    chat_history.insert(tk.END, f"PyPro:\n{reply}\n\n", "bot_tag")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)
    
    user_entry.delete(0, tk.END)
    speak(reply)

def clear_chat():
    global quiz_active
    quiz_active = False
    chat_history.config(state=tk.NORMAL)
    chat_history.delete(1.0, tk.END)
    greeting = "PyPro: Welcome to PyPro! " + responses["help"] + "\n\n"
    chat_history.insert(tk.END, greeting, "bot_tag")
    chat_history.config(state=tk.DISABLED)
    speak("Welcome to PyPro! " + responses["help"])

# Create Main Window GUI
window = tk.Tk()
window.title("PyPro - Technical Interviewer")
window.geometry("560x650")
window.config(bg="#181825")

header_frame = tk.Frame(window, bg="#1e1e2e", relief=tk.FLAT)
header_frame.pack(fill=tk.X, padx=12, pady=12)

title_label = tk.Label(header_frame, text="🤖 PyPro: Technical Interviewer", bg="#1e1e2e", fg="#cba6f7", font=("Segoe UI", 13, "bold"))
title_label.pack(pady=(10, 2))

subtitle_label = tk.Label(header_frame, text="Voice-Enabled Mock Interviewer with Interactive Quiz Mode", bg="#1e1e2e", fg="#9399b2", font=("Segoe UI", 9))
subtitle_label.pack(pady=(0, 10))

chat_history = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10), relief=tk.FLAT, bd=0)
chat_history.pack(padx=12, pady=(0, 10), fill=tk.BOTH, expand=True)

chat_history.tag_config("user_tag", foreground="#89b4fa", font=("Segoe UI", 10, "bold"))
chat_history.tag_config("bot_tag", foreground="#a6e3a1", font=("Segoe UI", 10))

bottom_frame = tk.Frame(window, bg="#181825")
bottom_frame.pack(padx=12, pady=(0, 15), fill=tk.X)

user_entry = tk.Entry(bottom_frame, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4", font=("Segoe UI", 11), relief=tk.FLAT)
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, ipadx=8, padx=(0, 8))
user_entry.bind("<Return>", send_message)

clear_button = tk.Button(bottom_frame, text="Clear", command=clear_chat, bg="#45475a", fg="#cdd6f4", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10, pady=6)
clear_button.pack(side=tk.RIGHT, padx=(0, 6))

send_button = tk.Button(bottom_frame, text="Send", command=send_message, bg="#89b4fa", fg="#11111b", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, activebackground="#b4befe", padx=14, pady=6)
send_button.pack(side=tk.RIGHT)

if __name__ == "__main__":
    chat_history.config(state=tk.NORMAL)
    startup_message = "PyPro: Welcome to PyPro! " + responses["help"] + "\n\n"
    chat_history.insert(tk.END, startup_message, "bot_tag")
    chat_history.config(state=tk.DISABLED)
    
    # Automatically speak the startup greeting and topics out loud upon launching
    window.after(500, lambda: speak("Welcome to PyPro! " + responses["help"]))
    
    window.mainloop()