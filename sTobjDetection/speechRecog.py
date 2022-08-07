import speech_recognition as sr
import pyttsx3
import time

def recog():
    recognizer = sr.Recognizer()

    """ for index, mic_name in enumerate (sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, mic_name))
        if "sysdefault" in mic_name:
            laptop_mic = sr.Microphone(device_index = index, chunk_size=1024, sample_rate=48000)
            break """

    laptop_mic = sr.Microphone(device_index = 1, chunk_size=1024, sample_rate=48000)

    while (True):
        try:
            with laptop_mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Say something!")
                audio = recognizer.listen(source, timeout=5)

                object_name = recognizer.recognize_google(audio)
                object_name = object_name.lower()

                print(f"You said: {object_name}")
                #return set(object_name.split(" "))

        except sr.WaitTimeoutError:
            print("Timeout")
            return None
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")

# recog()