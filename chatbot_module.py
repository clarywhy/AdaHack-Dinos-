""" First script training the chatbots"""

# External imports
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from googletrans import Translator

# Internal imports
from translation_query import translate_unknown_phrases

user_score = 0
class ChatbotLevel:
    # Train the chatbot
    def __init__(self, name, conversation, targetWords, corpusModules):
        self.name = name
        self.conversation = conversation
        self.targetWords = targetWords
        
        self.chatbot = ChatBot(name)
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        for module in corpusModules: #TODO: this
            trainer.train(module)
        # trainer.train("chatterbot.corpus.french.greetings")
        listTrainer = ListTrainer(self.chatbot)
        listTrainer.train(conversation)

# Say hello
first_level = ChatbotLevel(
    "Hopper", 
    [
        "Bonjour",
        "Salut",      
    ], 
    {2: ["bonjour", "salut", "bonsoir", "coucou"], 
     1: ["bon jour", "bon soir"]}, 
    ["chatterbot.corpus.french.greetings"])

# Say hello and ask how someone is and respond
second_level = ChatbotLevel(
    "Hopper", 
    [
        "Bonjour",
        "Salut",      
        "Ca va?",
        "Bien, et toi?",
        "Bien, merci",
        "Super!"
    ], 
    {2: ["bonjour", "salut", "bonsoir", "coucou", "ça va", "comment allez vous", "comment allez-vous", "bien", "mal"], 
     1: ["bon jour", "bon soir", "ca va", "bon"]}, 
    ["chatterbot.corpus.french.greetings"])

# Say hello and ask for directions
third_level = ChatbotLevel(
    "Hopper", 
    [
        "Bonjour",
        "Salut",        
        "Ca va?",
        "Super, et toi?",
        "Bien, merci",
        "Où est la tour Eiffel?",
        "à gauche",
        "Merci beaucoup",
        "Au revoir",
        "Au revoir",
    ], 
    {2: ["où est"], 1: ["ou est"]}, 
    ["chatterbot.corpus.french.greetings", "chatterbot.corpus.french.conversations"])


def conversation_loop(level):
    global user_score
    while True:
        # Ask the user to input
        user_prompt = input("You: ")
        # print(user_score) # for debugging , remove
        
        # Add to the user's score if they use key phrases from the lessom
        for score, words in level.targetWords.items():
            for word in words:
                if word in user_prompt.lower():
                    user_score += score
                
        # Stop the conversation 
        if "au revoir" in user_prompt.lower():
            print(level.name + ": Au revoir!")
            print("Score:", user_score)
            break

        # Get a response from the chatbot
        response = level.chatbot.get_response(user_prompt)

        # Shot the chatbot response
        print(level.name + ": ", response)

    # Translate unknown phrases
    # translate_unknown_phrases()

# Start the first level
# Prompt for the user to start the conversation
print("Say hello to Hopper!")
print("When you are finished with the conversation, say \"Au Revoir\", which means goodbye!") 
# TODO: Run the example conversation
# TODO: Add user guidance - hint button?
# Initialise the chatbot   
conversation_loop(first_level)

print("Say hello to Hopper and ask how they're doing!")
print("When you are finished with the conversation, say \"Au Revoir\", which means goodbye!") 
conversation_loop(second_level)

print("Say hello to Hopper and ask for directions to the Eiffel Tower!")
print("In French, the Eiffel Tower is 'La tour Eiffel'!")
print("When you are finished with the conversation, say \"Au Revoir\", which means goodbye!") 
conversation_loop(third_level)
print(user_score)

