""" First script training the chatbots"""

# External imports
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from googletrans import Translator

user_score = 0
class ChatbotLevel:
    # Train the chatbot
    def __init__(self, name, conversation, targetWords, corpusModules):
        self.name = name
        self.conversation = conversation
        self.targetWords = targetWords
        
        self.chatbot = ChatBot(name)
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        for module in corpusModules:
            trainer.train(module)
        listTrainer = ListTrainer(self.chatbot)
        listTrainer.train(conversation)



first_level = ChatbotLevel(
    "Hopper", 
    [
        "Bonjour",
        "Salut",
        "Bonsoir",        
        "Ca va?",
        "Comment allez-vous?",
        "Bien, merci",
        "Super!"
    ], 
    ["bonjour", "salut", "bonsoir", "coucou"], 
    ["chatterbot.corpus.french.greetings"])


# second_level = ChatbotLevel(
#     "Hopper", 
#     [
#         "Bonjour",
#         "Salut",
#         "Bonsoir",        
#         "Ca va?",
#         "Comment allez-vous?",
#         "Bien, merci",
#         "Super!"
#         "Où est la tour Eiffel?",
#         "à gauche",
#         "à droit",
#         "Ici",
#         "Là-bas",
#         "Je ne sais pas",
#         "Merci",
#     ], 
#     ["bonjour", "ça va"], 
#     ["chatterbot.corpus.french.greetings", "chatterbot.corpus.french.conversations"])

# third_level = ChatbotLevel(
#     "Hopper", 
#     [
#         "Bonjour",
#         "Salut",
#         "Bonsoir",        
#         "Ca va?",
#         "Comment allez-vous?",
#         "Bien, merci",
#         "Super!"
#         "Où est la tour Eiffel?",
#         "à gauche",
#         "à droit",
#         "Ici",
#         "Là-bas",
#         "Je ne sais pas",
#         "Merci",
#     ], 
#     ["bonjour"], 
#     ["chatterbot.corpus.french.greetings", "chatterbot.corpus.french.conversations", "chatterbot.corpus.french.food"])


def conversation_loop(level):
    
    # Record the score for this level
    # this_level_user_score = 0
    global user_score
    while True:
        # Ask the user to input
        user_prompt = input("You: ")
        print(user_score)
        # print(this_level_user_score)
        
        # Add to the user's score if they use key phrases from the lessom
        for word in level.targetWords:
            if word in user_prompt.lower():
                user_score += 1
                
        # Stop the conversation 
        if "au revoir" in user_prompt.lower():
            print(level.name + ": Au revoir!")
            print("Score:", user_score)
            break

        # Get a response from the chatbot
        response = level.chatbot.get_response(user_prompt)

        # Shot the chatbot response
        print(level.name + ": ", response)

    # return user_score

# Start the first level
# Prompt for the user to start the conversation
print("Say hello to Hopper!")
print("When you are finished with the conversation, say \"Au Revior\", which means goodbye!") 
# TODO: Run the example conversation
# TODO: Fix the score update
# Initialise the chatbot   
conversation_loop(first_level)
conversation_loop(first_level)

translator = Translator()

print("Were there any phrases Hopper used that you didn't understand?")
print("Type them in here and we'll give you the english translationm")