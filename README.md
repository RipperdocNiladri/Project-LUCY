# 🤖 LUCY A.I. — Voice Command Assistant

**LUCY A.I.** is a modular, Python-based voice command assistant inspired by futuristic AI assistants such as **JARVIS**.

The project combines **speech recognition, neural text-to-speech, system monitoring, application control, web navigation, media playback, and voice notes** into a single desktop assistant.

LUCY is designed with a modular architecture so that new capabilities can be added as the project evolves.

---

## ✨ Features

### 🗣️ Natural Voice Interaction

* Converts speech into commands using **Google Speech Recognition**.
* Uses automatic microphone noise calibration for improved recognition.
* Responds using Microsoft's **Edge Neural TTS** through `edge-tts`.
* Uses the `en-US-AriaNeural` voice for natural-sounding responses.

### 🔊 Offline Voice Fallback

* Automatically falls back to **Windows SAPI5 / `pyttsx3`** when an internet connection is unavailable.
* Allows LUCY to remain functional even when neural TTS cannot be accessed.

### 🖥️ System Diagnostics

LUCY can monitor basic system information using `psutil`, including:

* CPU usage
* RAM usage
* Battery percentage
* Battery status

### 🌐 Web & Media Control

LUCY can interact with commonly used online services:

* Google Search
* YouTube
* Reddit
* GitHub
* ChatGPT
* Gmail

It can also open and launch media searches through voice commands.

### 🪟 Windows Application Control

Launch common Windows applications using voice commands:

* Notepad
* Calculator
* Visual Studio Code
* File Explorer
* Command Prompt

### 📝 Voice Notes

* Record quick notes using voice commands.
* Store notes for later use.
* Read saved notes back through LUCY.

### 😴 Standby Mode

* LUCY can enter a standby/sleep state.
* Wake-up detection allows the assistant to become active again.
* Provides a more natural always-ready assistant experience.

### 🎲 Fun Commands

LUCY also includes simple entertainment commands such as:

* Tell a joke
* Flip a coin
* Roll a die

---

## 🛠️ Technologies Used

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| **Python**            | Core programming language    |
| **SpeechRecognition** | Speech-to-text               |
| **PyAudio**           | Microphone input             |
| **Edge-TTS**          | Neural text-to-speech        |
| **pyttsx3**           | Offline Windows TTS fallback |
| **pygame**            | Audio playback               |
| **psutil**            | System monitoring            |
| **Wikipedia**         | Knowledge queries            |
| **Requests**          | HTTP/network requests        |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RipperdocNiladri/Project-LUCY.git
cd Project-LUCY
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install SpeechRecognition PyAudio edge-tts pygame pyttsx3 wikipedia psutil requests
```

### ⚠️ Windows PyAudio Note

If installing `PyAudio` fails with build errors on your Python version, you may need an alternative installation method or a compatible PyAudio wheel.

One possible approach is:

```bash
pip install pipwin
pipwin install pyaudio
```

> **Note:** `pipwin` compatibility can vary with newer Python versions. If it doesn't work, use a PyAudio package/wheel compatible with your Python version.

---

## 🚀 Running LUCY

After installing the dependencies, run:

```bash
python lucy.py
```

LUCY will initialize the microphone and begin listening for voice commands.

---

## 🗣️ Voice Commands

Here are some example commands that LUCY can understand:

| Category                 | Example Commands                                                                   |
| ------------------------ | ---------------------------------------------------------------------------------- |
| 🤖 **Identity & Status** | `"Who are you?"` · `"How are you?"` · `"What can you do?"`                         |
| 🕐 **Time & Date**       | `"What time is it?"` · `"What is today's date?"`                                   |
| 💻 **System Health**     | `"System status"` · `"Battery percentage"` · `"CPU usage"`                         |
| 🌐 **Web Navigation**    | `"Search Google for quantum computing"` · `"Open GitHub"` · `"Open ChatGPT"`       |
| ▶️ **YouTube & Media**   | `"Play Interstellar soundtrack on YouTube"` · `"Play music"`                       |
| 📚 **Knowledge**         | `"Who is Albert Einstein?"` · `"Wikipedia Python programming"`                     |
| 🪟 **Applications**      | `"Open Notepad"` · `"Open Calculator"` · `"Open VS Code"` · `"Open File Explorer"` |
| 📝 **Notes**             | `"Take a note"` · `"Read my notes"`                                                |
| 🎲 **Fun**               | `"Tell me a joke"` · `"Flip a coin"` · `"Roll a die"`                              |
| 😴 **Standby & Exit**    | `"Lucy, go to sleep"` · `"Goodbye"` · `"Exit"`                                     |

> **Note:** Available commands may change as new features are added to the project.

---

## 🧩 Project Structure

A typical project structure may look like:

```text
Project-LUCY/
│
├── lucy.py
├── requirements.txt
├── README.md
│
├── notes/
│   └── ...
│
└── assets/
    └── ...
```

The project is intended to evolve into a more modular architecture as additional assistant capabilities are implemented.

---

## 🔮 Future Development

LUCY is an ongoing project. Planned improvements may include:

* 🧠 More advanced conversational intelligence
* 🎙️ Improved speech recognition
* ⚡ Faster voice response generation
* 🖥️ Dedicated graphical desktop interface
* 🧩 Plugin-based command system
* 🏠 Smart-device and IoT integration
* 🔐 Local/user-specific commands
* 📊 Advanced system monitoring
* 🤖 More natural assistant interactions
* 🚀 Full-featured desktop AI assistant

---

## 🎯 Project Vision

The goal of **LUCY A.I.** is to evolve from a simple voice-command program into a **full desktop AI assistant** capable of interacting naturally with the computer and helping with everyday tasks.

The project is being developed incrementally, with each version introducing new capabilities and improving the overall assistant experience.

---

## 👨‍💻 Author

**Niladri**

Built with Python, curiosity, and a little bit of futuristic ambition. ⚡🤖

---

## 📌 Project Status

**🚧 Active Development**

LUCY A.I. is an evolving personal project. Features, architecture, and capabilities are continuously being improved.

```

This version is ready to use as your repository's **`README.md`** and avoids overclaiming features that aren't implemented yet.
```
