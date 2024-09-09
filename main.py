import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import pyautogui
import time

def start_program():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    # Initialize OpenCV
    cap = cv2.VideoCapture(0)

    # Define gesture recognition functions
    def recognize_gesture(landmarks):
        thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP].y
        index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        middle_finger_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        ring_finger_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y
        pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP].y
        wrist = landmarks[mp_hands.HandLandmark.WRIST].y

        # Open hand (all fingers up)
        if all(landmark < wrist for landmark in [thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip]):
            return "Play/Pause"
        # Thumbs up
        elif thumb_tip < index_finger_tip and thumb_tip < middle_finger_tip and thumb_tip < ring_finger_tip and thumb_tip < pinky_tip:
            return "Volume Up"
        # Thumbs down
        elif thumb_tip > index_finger_tip and thumb_tip > middle_finger_tip and thumb_tip > ring_finger_tip and thumb_tip > pinky_tip:
            return "Volume Down"
        # Index finger up
        elif index_finger_tip < thumb_tip and index_finger_tip < middle_finger_tip and index_finger_tip < ring_finger_tip and index_finger_tip < pinky_tip:
            return "Next Video"
        # Index finger down
        elif index_finger_tip > thumb_tip and index_finger_tip > middle_finger_tip and index_finger_tip > ring_finger_tip and index_finger_tip > pinky_tip:
            return "Previous Video"
        # Pinky up
        elif pinky_tip < thumb_tip and pinky_tip < index_finger_tip and pinky_tip < middle_finger_tip and pinky_tip < ring_finger_tip:
            return "Toggle Subtitles"
        return "Unknown"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Recognize gesture
                gesture = recognize_gesture(hand_landmarks.landmark)
                cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Perform actions based on gesture
                if gesture == "Play/Pause":
                    pyautogui.press('space')
                elif gesture == "Volume Up":
                    pyautogui.press('volumeup')
                elif gesture == "Volume Down":
                    pyautogui.press('volumedown')
                elif gesture == "Next Video":
                    pyautogui.hotkey('shift', 'n')
                elif gesture == "Previous Video":
                    pyautogui.hotkey('shift', 'p')
                elif gesture == "Toggle Subtitles":
                    pyautogui.hotkey('c')

                time.sleep(2)

        # Display the frame
        cv2.imshow('Hand Gesture Control', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def show_how_to_use():
    messagebox.showinfo("How to use", """
    Thumbs up/down -> Volume up/down
    Index up/down -> Next/previous video
    Flat hand -> Pause/play
    Pinky up -> Subtitles on/off

    Click the key 'q' to quit
    """)

def show_credits():
    messagebox.showinfo("About", "Created by Ezequiel, Felipe, Inácio & Victor")


def toggle_theme():
    if root.cget("bg") == "#2c3e50":
        set_light_theme()
    else:
        set_dark_theme()

def set_light_theme():
    root.configure(bg="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", foreground="#2c3e50")
    style.configure("Light.TButton", background="#d3d3d3", foreground="black", borderwidth=0, relief="flat")
    style.map("Light.TButton", background=[("pressed", "#c0c0c0"), ("active", "#d3d3d3")])
    logo_label.configure(bg="#f0f0f0")
    switch_button_styles("Light.TButton")

def set_dark_theme():
    root.configure(bg="#2c3e50")
    style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1")
    style.configure("Dark.TButton", background="#2980b9", foreground="#ecf0f1", borderwidth=0, relief="flat")
    style.map("Dark.TButton", background=[("pressed", "#1c1c1c"), ("active", "#2980b9")])
    logo_label.configure(bg="#2c3e50")
    switch_button_styles("Dark.TButton")

def switch_button_styles(style_name):
    start_button.configure(style=style_name, cursor="hand2")
    how_to_use_button.configure(style=style_name, cursor="hand2")
    credits_button.configure(style=style_name, cursor="hand2")
    toggle_button.configure(style=style_name, cursor="hand2")

root = tk.Tk()
root.title("GestPlay")
root.geometry("600x400")

# Create a style
style = ttk.Style()
style.theme_use("clam")

# Define custom styles with no hover effect
style.configure("Light.TButton", font=("Helvetica", 12), padding=10, borderwidth=0, relief="flat")
style.configure("Dark.TButton", font=("Helvetica", 12), padding=10, borderwidth=0, relief="flat")

style.configure("TLabel", font=("Helvetica", 14))

# Define button states (you can set these to be the same as the background color to minimize hover effect)
style.map("Light.TButton", background=[("pressed", "#c0c0c0"), ("active", "#d3d3d3")])
style.map("Dark.TButton", background=[("pressed", "#1c1c1c"), ("active", "#2980b9")])

# Load and place the logo
youtube_logo = Image.open("youtube_logo.png")
youtube_logo = youtube_logo.resize((100, 50), Image.Resampling.LANCZOS)
youtube_logo = ImageTk.PhotoImage(youtube_logo)

logo_label = tk.Label(root, image=youtube_logo)
logo_label.pack(pady=10)

# Create and place the title label
title_label = ttk.Label(root, text="GestPlay", style="TLabel")
title_label.pack(pady=10)

# Create and place the buttons
start_button = ttk.Button(root, text="Start", command=start_program, style="Light.TButton")
start_button.pack(pady=10)

how_to_use_button = ttk.Button(root, text="How to use", command=show_how_to_use, style="Light.TButton")
how_to_use_button.pack(pady=10)

credits_button = ttk.Button(root, text="About", command=show_credits, style="Light.TButton")
credits_button.pack(pady=10)

# Create and place the theme toggle button
toggle_button = ttk.Button(root, text="Toggle Theme", command=toggle_theme, style="Light.TButton")
toggle_button.pack(pady=10)

# Set the initial theme
set_dark_theme()

# Run the application
root.mainloop()

