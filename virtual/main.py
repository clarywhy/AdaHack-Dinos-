from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

class Character:
    def __init__(self, name, conversation, targetWords):
        self.name = name
        self.conversation = conversation
        self.targetWords = targetWords
        
        self.chatbot = ChatBot(name)
        

chatbot = ChatBot("Le Hopper")

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.french")

userScore = 0
targetWords = ["bonjour"]

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
