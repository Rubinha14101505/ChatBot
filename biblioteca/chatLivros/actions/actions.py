import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionBuscarPorTitulo(Action):
    def name(self) -> Text:
        return "action_buscar_por_titulo"  
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        titulo = next(tracker.get_latest_entity_values("titulo"), None)
        
        if not titulo:
            dispatcher.utter_message(text="Qual é o título do livro que você procura?")
            return []

        url = f"https://openlibrary.org/search.json?title={titulo}"
        response = requests.get(url) 
        data = response.json()  
        
        if data["numFound"] > 0:
            livros = data["docs"][:3]
            mensagens = [f"{livro.get('title')} por {', '.join(livro.get('author_name', []))}" 
                        for livro in livros]
            dispatcher.utter_message(text="Aqui estão alguns resultados:\n" + "\n".join(mensagens))
        else:
            dispatcher.utter_message(response="utter_erro_base")
        
        return []  