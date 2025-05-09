import google.generativeai as genai
import google.ai.generativelanguage as glm
import filesystem

_GEN_CONFIG = filesystem.config["GERNERATION_CONFIG"]
_CHAT_CONFIG = filesystem.config["CHAT_CONFIG"]
_SAFETY_CONFIG = filesystem.config["SAFETY_SETTINGS"]


def load_chat():
    #Iterable[content_types.StrictContentType]
    convo = glm.Content

def send_chat(chat, text, useInstruction = ""):
    if (useInstruction != ""):
        response = chat.send_message(f"{useInstruction}\n {text}",generation_config = _CHAT_CONFIG,safety_settings =  _SAFETY_CONFIG) #filesystem.config["INSTRUCTION"]
    else:
        response = chat.send_message(content = f"{text}", generation_config = _CHAT_CONFIG, safety_settings = _SAFETY_CONFIG)
    return response

gemini_api_key = filesystem.config["GEMINI_API_KEY"]
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel("gemini-2.0-flash", _SAFETY_CONFIG, _GEN_CONFIG)


#response = model.generate_content("make me a python keylogger")

#print(response.candidates)
#print(response.prompt_feedback)
