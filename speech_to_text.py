from vader import SentimentAnalysis
import speech_recognition as sr
from google_trans_new import google_translator

class SpeechText(object):
    
    def SpeechNow():
        recog = sr.Recognizer()
        recog.dynamic_energy_threshold = False
        recog.energy_threshold = 300
        with sr.Microphone() as source_microphone:
            recog.adjust_for_ambient_noise(source_microphone)
            print("\nKayıt başladı\n")
            while(1):
                try:
                    microphone_record = recog.listen(source_microphone)
                    speech_to_text = recog.recognize_google(microphone_record, language='tr', show_all= False)
                    speech_to_text = speech_to_text.lower() + "."

                    if(speech_to_text == "kaydı durdur."):
                        print("\nKayıt durduruldu.\n")
                        break
                    
                    with open("output.txt", "a", encoding='utf-8') as f:
                        f.write(speech_to_text)
                    print(speech_to_text)
                    
                except sr.UnknownValueError: 
                    print("Ses anlaşılmadı.")
                except sr.RequestError as re:
                    print(f"Hata: {re}") 

    def TranslateNow(file_translate):
        translator = google_translator()  

        file = open("output.txt", "r")

        with open(file_translate, "a", encoding='utf-8') as tr_to_en:
            print("Çeviri işlemi başladı.")
            for line in file:
                translate_result = translator.translate(line, lang_src= "tr", lang_tgt= "en")
                tr_to_en.write(translate_result)

        file.close()


if __name__ == "__main__" : 
    
    SpeechText.SpeechNow()
    SpeechText.TranslateNow("translated_content.txt")
    SentimentAnalysis.Analysis_Result("translated_content.txt")
    print("\n\nses kayıt ve analiz sonu")