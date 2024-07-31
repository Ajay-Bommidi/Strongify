import tkinter as tk
from tkinter import ttk
import re
import random

# Function to check password strength and provide tips
def check_password_strength(password):
    min_length = 8
    max_length = 20
    special_characters = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
    
    score = 0
    tips = []

    if len(password) < min_length:
        return "Password is too short. Minimum length is 8 characters.", "red", ["Increase password length to at least 8 characters."]
    elif len(password) > max_length:
        return "Password is too long. Maximum length is 20 characters.", "red", ["Reduce password length to a maximum of 20 characters."]

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        tips.append("Include at least one uppercase letter.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        tips.append("Include at least one lowercase letter.")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        tips.append("Include at least one number.")

    if special_characters.search(password):
        score += 1
    else:
        tips.append("Include at least one special character (e.g., !, @, #, $, etc.).")

    if score == 4:
        return "Strong password.", "green", []
    elif score == 3:
        return "Moderate password.", "yellow", tips
    else:
        return "Weak password. Consider improving your password with the following suggestions:", "red", tips

# Function to handle password check and update GUI
def on_check_password():
    password = password_entry.get()
    
    if not password:
        result_label.config(text="Please enter a password.", foreground="red")
        suggestion_label.config(text="", foreground="black")
        progress_bar.config(value=0)
        return
    
    result, color, tips = check_password_strength(password)
    
    # Get theme-based appreciation messages
    appreciation_message = get_appreciation_message(result, color)
    
    result_label.config(text=f"{result}\n{appreciation_message}", foreground=color)
    
    # Update progress bar color and tips
    if color == "red":
        progress_bar.config(value=25)
        suggestion_label.config(text="\n".join(tips), foreground="red")
    elif color == "yellow":
        progress_bar.config(value=50)
        suggestion_label.config(text="\n".join(tips), foreground="yellow")
    else:
        progress_bar.config(value=100)
        suggestion_label.config(text="", foreground="black")

# Function to get random appreciation message based on theme
def get_appreciation_message(result, color):
    if is_dark_mode:
        # Dark theme appreciation messages
        dark_messages = [
            "Excellent! Your password is secure and hacker-approved!",
            "Great work! Your password is strong and ready for any challenge.",
            "Top-notch! Your password is hacker-worthy and well-protected.",
            "Fantastic! Your password is as secure as it gets."
        ]
        if color == "green":
            return random.choice(dark_messages)
        elif color == "yellow":
            return "Good job! Your password is decent but could be more robust for optimal security."
        else:
            return "Watch out! Your password needs improvement to be hacker-ready."
    else:
        # Light theme appreciation messages
        light_messages = [
            "Well done! Your password is strong and developer-approved!",
            "Nice work! Your password is secure and developer-worthy.",
            "Great job! Your password is robust and meets developer standards.",
            "Impressive! Your password is strong and ready for any coding challenge."
        ]
        if color == "green":
            return random.choice(light_messages)
        elif color == "yellow":
            return "Nice work! Your password is moderate. Consider enhancing it for better security."
        else:
            return "Alert! Your password is weak. Strengthen it for a more secure developer environment."

# Function to toggle password visibility
def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        eye_label.config(text='👁️')  # Eye icon when password is visible
    else:
        password_entry.config(show='*')
        eye_label.config(text='👁️')  # Eye icon when password is hidden

# Function to handle button hover effect
def on_enter(e):
    check_button.config(background="#0056b3", foreground="white", font=("Arial", 14, "bold"))

def on_leave(e):
    check_button.config(background="#007bff", foreground="white", font=("Arial", 14, "bold"))

# Function to toggle between dark and light themes
def toggle_theme():
    global is_dark_mode
    if is_dark_mode:
        # Switch to light mode
        root.configure(bg="white")
        title_label.config(bg="white", fg="black")
        password_label.config(bg="white", fg="black")
        frame.config(bg="white")
        password_entry.config(background="white", foreground="black", insertbackground="black")  # Cursor color for light mode
        eye_label.config(bg="white", fg="black")
        check_button.config(style="Light.TButton")
        progress_bar.config(style="Light.Horizontal.TProgressbar")
        result_label.config(bg="white", fg="black")
        suggestion_label.config(bg="white", fg="black")
        theme_button.config(text="Switch to Dark Mode")
    else:
        # Switch to dark mode
        root.configure(bg="black")
        title_label.config(bg="black", fg="white")
        password_label.config(bg="black", fg="white")
        frame.config(bg="black")
        password_entry.config(background="black", foreground="white", insertbackground="white")  # Cursor color for dark mode
        eye_label.config(bg="black", fg="white")
        check_button.config(style="Dark.TButton")
        progress_bar.config(style="Dark.Horizontal.TProgressbar")
        result_label.config(bg="black", fg="white")
        suggestion_label.config(bg="black", fg="white")
        theme_button.config(text="Switch to Light Mode")
    
    is_dark_mode = not is_dark_mode

# Create the main window
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("450x400")
is_dark_mode = True  # Start with dark mode

# Create and place widgets
title_label = tk.Label(root, text="Password Strength Checker", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

password_label = tk.Label(root, text="Enter your password:")
password_label.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

password_entry = tk.Entry(frame, show="*", width=40, font=("Arial", 12))
password_entry.pack(side=tk.LEFT, padx=5)

# Eye icon to toggle password visibility
eye_label = tk.Label(frame, text="👁️", font=("Arial", 16), cursor="hand2")
eye_label.pack(side=tk.LEFT, padx=5)
eye_label.bind("<Button-1>", lambda e: toggle_password())

# Use ttk.Button for check_button and theme_button
check_button = ttk.Button(root, text="Check Password", command=on_check_password)
check_button.pack(pady=10, padx=10)
check_button.bind("<Enter>", on_enter)
check_button.bind("<Leave>", on_leave)

# Progress bar for password strength
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

suggestion_label = tk.Label(root, text="", font=("Arial", 12))
suggestion_label.pack(pady=10)

# Toggle theme button
theme_button = ttk.Button(root, text="Switch to Light Mode", command=toggle_theme)
theme_button.pack(pady=10)

# Style customization for buttons and progress bars
style = ttk.Style()
style.configure("Dark.TButton", font=("Arial", 14, "bold"), background="#007bff", foreground="white", borderwidth=1, relief="flat")
style.configure("Light.TButton", font=("Arial", 14, "bold"), background="#007bff", foreground="white", borderwidth=1, relief="flat")
style.configure("Dark.Horizontal.TProgressbar", thickness=20, troughcolor='black', background='#007bff')
style.configure("Light.Horizontal.TProgressbar", thickness=20, troughcolor='white', background='#007bff')

# Apply initial theme
toggle_theme()

# Run the application
root.mainloop()
