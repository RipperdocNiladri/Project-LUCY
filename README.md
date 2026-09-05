# LUCY A.I. - Voice Command Assistant

LUCY is a modern, modular voice assistant built in Python inspired by JARVIS.

## Features
- **Natural Human-like Voice**: Powered by Microsoft Edge's Neural TTS (`edge-tts` with `en-US-AriaNeural`).
- **Offline Fallback**: Automatically switches to Windows SAPI5 / `pyttsx3` if no internet connection is available.
- **Smart Speech Recognition**: Google Speech Recognition API with automatic noise calibration.
- **System Diagnostics**: Reports CPU load, RAM usage, and battery statistics using `psutil`.
- **Web & Media**: Search Google, play videos on YouTube, open Reddit, GitHub, ChatGPT, Gmail.
- **Windows Apps**: Launch Notepad, Calculator, VS Code, File Explorer, Command Prompt.
- **Productivity**: Record quick voice notes and read them back anytime.
- **Standby & Exit**: Standby/sleep mode with wake-up detection.

---

## 📦 Required Packages

Install all dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install SpeechRecognition PyAudio edge-tts pygame pyttsx3 wikipedia psutil requests
```

> **Windows Note on PyAudio**:
> If `pip install pyaudio` fails with build errors on your Python version, install it using:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

---

## 🚀 How to Run

Navigate to this directory and run:

```bash
python lucy.py
```

---

## 🗣️ Voice Commands You Can Say to LUCY

| Category | Example Commands |
|---|---|
| **Identity & Status** | *"Who are you?"*, *"How are you?"*, *"What can you do?"* |
| **Time & Date** | *"What time is it?"*, *"What is today's date?"* |
| **System Health** | *"System status"*, *"Battery percentage"*, *"CPU usage"* |
| **Web Navigation** | *"Search Google for quantum computing"*, *"Open GitHub"*, *"Open ChatGPT"* |
| **YouTube & Music** | *"Play Interstellar soundtrack on YouTube"*, *"Play music"* |
| **Knowledge** | *"Who is Albert Einstein?"*, *"Wikipedia Python programming"* |
| **Applications** | *"Open Notepad"*, *"Open Calculator"*, *"Open VS Code"*, *"Open File Explorer"* |
| **Notes** | *"Take a note"*, *"Read my notes"* |
| **Fun** | *"Tell me a joke"*, *"Flip a coin"*, *"Roll a die"* |
| **Standby & Exit** | *"Lucy, go to sleep"*, *"Goodbye"*, *"Exit"* |
