import ollama

modelos = {
    "gemma3:1b" : "gemma3:1b",
    "gemma3:latest" :  "gemma3",
    "gemma3:12b" : "gemma3:12b",
    "gemma3:27b" : "gemma3:27b",
    "llama3.2-vision:latest" : "llama3.2-vision",
    "minicpm-o:latest" : "minicpm-o",
    "minicpm-v:latest" : "minicpm-v",
    "llava-phi3:latest" : "llava-phi3",
    "llava-llama3:latest" : "llava-llama3",
    "moondream:latest" : "moondream"
}

def avaliable_models():
    return [
        modelos[model]
        for model in ([model.model for model in ollama.list().models])
        if model in modelos.keys()
    ]            

def new_message(model, message, messages):
    new_messages = {
        'role' : 'user',
        'content' : message,
    }
    messages.append(new_messages)
    chat = ollama.chat(
        model=model,
        messages=messages,
        stream=True
    )
    return chat, messages
