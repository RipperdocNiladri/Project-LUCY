import os
import sys
import time
import datetime
import random
import webbrowser
import subprocess
import tempfile
import asyncio
from typing import Optional


try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pygame
    pygame.mixer.init()
except Exception:
    pygame = None

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import wikipedia
except ImportError:
    wikipedia = None

try:
    import psutil
except ImportError:
    psutil = None


class LucyAssistant:
    def __init__(self, name: str = "Lucy", voice_name: str = "en-US-AriaNeural"):
        self.name = name
        self.voice_name = voice_name
        self.temp_audio_file = os.path.join(tempfile.gettempdir(), "lucy_voice_temp.mp3")
        self.notes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lucy_notes.txt")
        self.is_running = True

        if sr:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
        else:
            self.recognizer = None

        self._init_offline_tts()

    def _init_offline_tts(self):
        self.offline_engine = None
        if pyttsx3:
            try:
                self.offline_engine = pyttsx3.init()
                voices = self.offline_engine.getProperty("voices")
                for voice in voices:
                    if "zira" in voice.name.lower() or "female" in voice.name.lower():
                        self.offline_engine.setProperty("voice", voice.id)
                        break
                self.offline_engine.setProperty("rate", 175)
            except Exception as e:
                print(f"[Warning] Offline TTS initialization issue: {e}")

    def speak(self, text: str):
        print(f"\n[{self.name.upper()}]: {text}")

        if edge_tts and pygame:
            try:
                async def _generate():
                    communicate = edge_tts.Communicate(text, self.voice_name)
                    await communicate.save(self.temp_audio_file)

                asyncio.run(_generate())

                pygame.mixer.music.load(self.temp_audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()

                if os.path.exists(self.temp_audio_file):
                    try:
                        os.remove(self.temp_audio_file)
                    except OSError:
                        pass
                return
            except Exception:            
                pass

        if self.offline_engine:
            try:
                self.offline_engine.say(text)
                self.offline_engine.runAndWait()
            except Exception as e:
                print(f"[Audio Output Error]: {e}")

    def listen(self) -> str:
        if not self.recognizer:
            print("\n[Notice] Microphone module is not loaded. Type your command below.")
            return input(f"[{os.getlogin()}]: ").strip().lower()

        try:
            with sr.Microphone() as source:
                print("\n[LISTENING] Listening for your command...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=10)
                print("[PROCESSING] Analyzing speech...")
                query = self.recognizer.recognize_google(audio, language="en-US")
                print(f"[YOU]: {query}")
                return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"[Network Notice] Speech API unreachable ({e})")
            self.speak("I am having trouble reaching the speech recognition servers.")
            return ""
        except Exception as e:
            print(f"[Microphone Notice]: {e}")
            return ""

    def greet(self):
        """Greets the user based on the time of the day."""
        current_hour = datetime.datetime.now().hour
        if 0 <= current_hour < 12:
            greeting_period = "Good morning"
        elif 12 <= current_hour < 18:
            greeting_period = "Good afternoon"
        else:
            greeting_period = "Good evening"

        self.speak(
            f"{greeting_period}! I am {self.name}, your personal AI voice assistant. "
            f"All systems are online and fully operational. How may I assist you today?"
        )

    def greet_user(self):
        """Responds warmly and dynamically to greetings like 'hello', 'hi', 'hey'."""
        responses = [
            "Hello there! How can I help you today?",
            "Hi! Lucy here, all systems online. What's on your mind?",
            "Hey! Great to hear from you. What can I do for you?",
            "Hello! I am listening and ready for your command.",
            "Hi! Always a pleasure to assist you. How can I help?",
        ]
        self.speak(random.choice(responses))

    def tell_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}.")

    def tell_date(self):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {today}.")

    def report_system_status(self):
        """Reports hardware performance, battery, and memory usage."""
        if not psutil:
            self.speak("System diagnostics module is not available. Please install psutil.")
            return

        cpu_usage = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        battery = psutil.sensors_battery()

        report = f"Current CPU utilization is at {cpu_usage} percent. System memory is at {ram.percent} percent used."
        if battery:
            power_status = "plugged in" if battery.power_plugged else "discharging on battery"
            report += f" Battery level is at {battery.percent} percent, currently {power_status}."
        else:
            report += " No battery hardware detected on this device."

        self.speak(report)

    def search_wikipedia(self, query: str):
        if not wikipedia:
            self.speak("Wikipedia module is not installed.")
            return

        clean_query = (
            query.replace("wikipedia", "")
            .replace("who is", "")
            .replace("what is", "")
            .replace("search for", "")
            .replace("tell me about", "")
            .strip()
        )
        if not clean_query:
            self.speak("What subject would you like me to look up on Wikipedia?")
            return

        self.speak(f"Querying Wikipedia for {clean_query}...")
        try:
            summary = wikipedia.summary(clean_query, sentences=2)
            self.speak(summary)
        except wikipedia.DisambiguationError as e:
            suggested = ", ".join(e.options[:3])
            self.speak(f"There are multiple entries for {clean_query}, including {suggested}. Please be more specific.")
        except wikipedia.PageError:
            self.speak(f"I was unable to find an article matching {clean_query}.")
        except Exception:
            self.speak("I encountered an issue fetching information from Wikipedia.")

    def search_google(self, query: str):
        search_terms = (
            query.replace("search google for", "")
            .replace("google search", "")
            .replace("search for", "")
            .replace("search", "")
            .replace("google", "")
            .strip()
        )
        if not search_terms:
            self.speak("What should I search for on Google?")
            return
        self.speak(f"Searching Google for {search_terms}.")
        webbrowser.open(f"https://www.google.com/search?q={search_terms}")

    def play_youtube(self, query: str):
        song_name = (
            query.replace("play on youtube", "")
            .replace("play", "")
            .replace("on youtube", "")
            .replace("youtube", "")
            .strip()
        )
        if not song_name:
            self.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
            return
        self.speak(f"Playing {song_name} on YouTube.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song_name}")

    def take_note(self):
        self.speak("What would you like me to write down?")
        note_text = self.listen()
        if note_text:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.notes_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {note_text}\n")
            self.speak("Your note has been saved.")
        else:
            self.speak("I did not catch that. Note creation has been cancelled.")

    def read_notes(self):
        """Reads recent notes aloud."""
        if not os.path.exists(self.notes_file):
            self.speak("You don't have any saved notes yet.")
            return

        with open(self.notes_file, "r", encoding="utf-8") as f:
            notes = [line.strip() for line in f.readlines() if line.strip()]

        if not notes:
            self.speak("Your notes file is currently empty.")
            return

        self.speak(f"You have {len(notes)} notes recorded. Reading your most recent entries:")
        for note in notes[-3:]:
            self.speak(note)

    def launch_application(self, target: str):
        """Launches standard desktop tools and programs."""
        target = target.lower().strip()
        try:
            if "notepad" in target:
                self.speak("Launching Notepad.")
                subprocess.Popen("notepad.exe")
            elif "calculator" in target or "calc" in target:
                self.speak("Launching Calculator.")
                subprocess.Popen("calc.exe")
            elif "command prompt" in target or "cmd" in target or "terminal" in target:
                self.speak("Opening Command Prompt.")
                subprocess.Popen("cmd.exe")
            elif "explorer" in target or "file manager" in target or "my computer" in target:
                self.speak("Opening File Explorer.")
                subprocess.Popen("explorer.exe")
            elif "code" in target or "vs code" in target:
                self.speak("Opening Visual Studio Code.")
                os.system("code .")
            elif "chrome" in target:
                self.speak("Opening Google Chrome.")
                webbrowser.open("https://www.google.com")
            elif "edge" in target:
                self.speak("Opening Microsoft Edge.")
                subprocess.Popen("msedge.exe")
            elif "instagram" in target:
                self.speak("Opening Instagram.")
                webbrowser.open("https://www.instagram.com")
            else:
                self.speak(f"I don't have a direct application shortcut for {target}. Searching the web instead.")
                webbrowser.open(f"https://www.google.com/search?q={target}")
        except Exception as e:
            self.speak(f"Unable to launch application: {e}")

    def tell_joke(self):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why did the developer go broke? Because he used up all his cache.",
            "An SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
            "Why do Python programmers have low self-esteem? Because they're constantly comparing their self to others.",
            "A programmer's spouse asks: 'Could you go to the store and get a loaf of bread? If they have eggs, get a dozen.' The programmer returns with 12 loaves of bread."
        ]
        self.speak(random.choice(jokes))

    def process_command(self, query: str) -> bool:
        """
        Parses the user query and routes it to the corresponding skill.
        Returns False if the session should terminate, True to continue.
        """
        if not query:
            return True

        # Session Termination
        if any(w in query for w in ["exit", "quit", "goodbye", "bye", "shutdown", "terminate", "power off"]):
            self.speak("Shutting down. Have an excellent day!")
            return False

        # Greetings (Hello / Hi / Hey)
        elif any(w in query.split() for w in ["hello", "hi", "hey", "greetings", "hola"]):
            self.greet_user()

        # Identity & Small Talk
        elif any(w in query for w in ["who are you", "what is your name", "what's your name"]):
            self.speak(
                f"I am {self.name}, your Jarvis-inspired voice assistant written in modern Python. "
                "I am here to handle your system operations, searches, and daily workflows."
            )

        elif any(w in query for w in ["how are you", "how are you doing", "how's it going"]):
            self.speak("All background services are optimal and operating smoothly! How can I help you right now?")

        elif "what can you do" in query or "help" in query or "features" in query:
            self.speak(
                "You can ask me to check system health, tell the time and date, search Google, "
                "play videos on YouTube, search Wikipedia, open apps like Notepad or Calculator, "
                "take notes, or tell a joke."
            )

        # Date & Time
        elif "time" in query:
            self.tell_time()

        elif "date" in query or "day is it" in query:
            self.tell_date()

        # Hardware & System Diagnostics
        elif any(w in query for w in ["system status", "system information", "system report", "battery", "cpu", "ram", "memory", "diagnostics", "performance"]):
            self.report_system_status()

        # Wikipedia Queries
        elif "wikipedia" in query or query.startswith("who is") or query.startswith("what is"):
            self.search_wikipedia(query)

        # Media & YouTube
        elif "youtube" in query or query.startswith("play"):
            self.play_youtube(query)

        # Web Navigation Shortcuts
        elif "open google" in query:
            self.speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "open github" in query:
            self.speak("Opening GitHub.")
            webbrowser.open("https://www.github.com")

        elif "open reddit" in query:
            self.speak("Opening Reddit.")
            webbrowser.open("https://www.reddit.com")

        elif "open chatgpt" in query:
            self.speak("Opening ChatGPT.")
            webbrowser.open("https://chatgpt.com")

        elif "open gmail" in query or "open email" in query:
            self.speak("Opening Gmail.")
            webbrowser.open("https://mail.google.com")

        elif "open instagram" in query:
            self.speak("Opening Instagram.")
            webbrowser.open("https://www.instagram.com")

        elif "search" in query or "google" in query:
            self.search_google(query)

        # Application Launching
        elif query.startswith("open") or query.startswith("launch"):
            app_target = query.replace("open", "").replace("launch", "").strip()
            self.launch_application(app_target)

        # Note Taking
        elif any(p in query for p in ["take a note", "write this down", "new note", "record note"]):
            self.take_note()

        elif any(p in query for p in ["read notes", "show notes", "my notes", "read my note"]):
            self.read_notes()

        # Entertainment & Fun
        elif "joke" in query or "make me laugh" in query:
            self.tell_joke()

        elif "flip a coin" in query or "toss a coin" in query:
            self.speak(f"The coin shows {random.choice(['Heads', 'Tails'])}!")

        elif "roll a die" in query or "roll a dice" in query:
            self.speak(f"The die rolled a {random.randint(1, 6)}!")

        # Standby / Sleep Mode
        elif "sleep" in query or "standby" in query:
            self.speak("Entering standby mode. Call my name or say 'wake up' when you are ready.")
            self.standby_mode()

        # Fallback / Unrecognized Command
        else:
            self.speak(f"I didn't recognize a built-in command for '{query}'. Would you like me to Google it?")
            confirmation = self.listen()
            if any(w in confirmation for w in ["yes", "sure", "ok", "yeah", "please", "go ahead"]):
                self.search_google(query)
            else:
                self.speak("Standing by for your next command.")

        return True

    def standby_mode(self):
        """Low-power standby loop that waits for wake command."""
        while True:
            if not self.recognizer:
                input("Press [Enter] to wake LUCY up...")
                self.speak("I am back online and listening.")
                break
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=4)
                    transcript = self.recognizer.recognize_google(audio, language="en-US").lower()
                    if self.name.lower() in transcript or "wake up" in transcript:
                        self.speak("I am awake! How may I assist you?")
                        break
            except Exception:
                continue

    def run(self):
        """Main execution lifecycle."""
        print("=" * 65)
        print(f"             L U C Y   A . I .   O N L I N E")
        print("=" * 65)
        self.greet()

        while self.is_running:
            command = self.listen()
            if command:
                self.is_running = self.process_command(command)
            time.sleep(0.3)


if __name__ == "__main__":
    lucy = LucyAssistant(name="Lucy", voice_name="en-US-AriaNeural")
    lucy.run()
