import speech_recognition as sr
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time

class VoiceToTextApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Membantu Listening")
        
        self.text_output = ScrolledText(self.master, wrap=tk.WORD, width=80, height=30)
        self.text_output.pack(pady=10)
        
        self.btn_start = tk.Button(self.master, text="Mulai Mendengarkan", command=self.start_listening)
        self.btn_start.pack(pady=10)
        
        self.btn_stop = tk.Button(self.master, text="Berhenti Mendengarkan", command=self.stop_listening, state=tk.DISABLED)
        self.btn_stop.pack(pady=10)
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False

        # Change the source to "Stereo Mix" or similar
        self.microphone.dynamic_energy_threshold = False
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.last_sound_time = time.time()  # Waktu terakhir suara terdeteksi

    def start_listening(self):
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.is_listening = True

        with self.microphone as source:
            self.audio = self.recognizer.listen(source, timeout=None)

        try:
            text = self.recognizer.recognize_google(self.audio)
            self.text_output.insert(tk.END, f"{text}\n")
            self.last_sound_time = time.time()  # Perbarui waktu terakhir suara terdeteksi
        except sr.UnknownValueError:
            self.text_output.insert(tk.END, "Suara tidak dapat dimengerti\n")
        except sr.RequestError as e:
            self.text_output.insert(tk.END, f"Error with the speech recognition service; {e}\n")

        if self.is_listening:
            self.master.after(100, self.check_for_silence)

    def check_for_silence(self):
        if not self.is_listening:
            return  # Hentikan pemeriksaan jika tidak mendengarkan

        current_time = time.time()
        elapsed_time = current_time - self.last_sound_time

        if elapsed_time > 3.0:  # Jeda setelah 3 detik tanpa suara
            self.stop_listening()
            return

        try:
            text = self.recognizer.recognize_google(self.audio, show_all=True)
            if not text:
                self.stop_listening()
                return
        except sr.UnknownValueError:
            pass  # Biarkan lanjut jika suara tidak dapat dipahami

        self.master.after(100, self.check_for_silence)

    def stop_listening(self):
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.is_listening = False

        # Set timeout to 0 to stop listening
        self.recognizer.listen(self.microphone, timeout=0)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceToTextApp(root)
    root.mainloop()
