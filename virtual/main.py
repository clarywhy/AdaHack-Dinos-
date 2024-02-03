from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

chatbot = ChatBot("Le Hopper")

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.french")

conversation = [
    "Bonjour",
    "salut",
    "bonsoir",
    "ça va?",
    "comment allez-vous?"
]

while True:
    print("Le Hopper: Bonjour!")
    user_prompt = input("You: ")
    response = chatbot.get_response(user_prompt)
    print("Le Hopper: ", response)

    if "au revoir" in user_prompt.lower():
        print("Le Hopper: Au revoir!")
        break
