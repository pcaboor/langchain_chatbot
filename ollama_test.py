from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from tqdm import tqdm
import time
import threading

# Créer le modèle de template
template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1", callback_manager=CallbackManager([StreamingStdOutCallbackHandler]))

# Chainer le prompt avec le modèle
chain = prompt | model

def loading_indicator():
    for _ in tqdm(iter(int, 1), desc="Génération en cours..."):
        if response_ready:
            break
        time.sleep(0.1)


while True:
    question = input("Veuillez entrer votre question (ou tapez 'exit' pour quitter) : ")

    # Vérifier si l'utilisateur souhaite quitter
    if question.lower() == "exit":
        print("Fin de la conversation. Au revoir !")
        break

    response_ready = False

    loading_thread = threading.Thread(target=loading_indicator)
    loading_thread.start()

    response = chain.invoke({"question": question})
    response_ready = True  

    loading_thread.join()

    print("\nRéponse :", response)
