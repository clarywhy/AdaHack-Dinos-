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
        for module in corpusModules:
            trainer.train(module)
        listTrainer = ListTrainer(self.chatbot)
        listTrainer.train(conversation)

# Say hello
first_level = ChatbotLevel(
    "Hopper", 
    [
        "Bonjour",
        "Salut",      
        "Ca va?",
        "Bien, et toi?",
        "Bien, merci",
        "Super!"
    ], 
    {2: ["bonjour", "salut", "bonsoir", "coucou"], 
     1: ["bon jour", "bon soir"]}, 
    ["chatterbot.corpus.french.greetings"])

# Say hello and ask how someone is and respond
# second_level = ChatbotLevel(
#     "Hopper", 
#     [
#         "Bonjour",
#         "Salut",      
#         "Ca va?",
#         "Bien, et toi?",
#         "Bien, merci",
#         "Super!"
#     ], 
#     {2: ["bonjour", "salut", "bonsoir", "coucou", "ça va", "comment allez vous", "comment allez-vous", "bien", "mal"], 
#      1: ["bon jour", "bon soir", "ca va", "bon"]}, 
#     ["chatterbot.corpus.french.greetings"])

# Say hello in the evening
# second_level = ChatbotLevel(
#     "Hopper", 
#     [
#         "Bonsoir",
#         "Bonsoir",      
#         "Ca va?",
#         "Bien, et toi?",
#         "Bien, merci",
#         "Super!"
#     ], 
#     {2: ["bonsoir", "ça va", "comment allez vous", "comment allez-vous", "bien", "mal"], 
#      1: ["bon soir", "ca va", "bon"]}, 
#     ["chatterbot.corpus.french.greetings"])

# Say hello and ask for directions
# fourth_level = ChatbotLevel(
#     "Hopper", 
#     [
#         "Bonjour",
#         "Salut",        
#         "Ca va?",
#         "Super, et toi?",
#         "Bien, merci",
#         "Où est la tour Eiffel?",
#         "à gauche",
#         "Là-bas?",
#         "Oui",
#         "Merci becaucoup",
#         "Au revoir",
#         "Au revoir",
#     ], 
#     {2: ["où est"], 1: ["ou est"]}, 
#     ["chatterbot.corpus.french.greetings", "chatterbot.corpus.french.conversations"])


def conversation_loop(level):
    global user_score
    while True:
        # Ask the user to input
        user_prompt = input("You: ")
        print(user_score) # for debugging , remove
        
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
    translate_unknown_phrases()
    # while True:
    #     translator = Translator()
    #     # TODO: turn this into a button
    #     print("Were there any phrases Hopper used that you didn't understand? Press 'n' to exit")
    #     user_word = input("Type them in here and we'll give you the English translation: ")

    #     if user_word.lower() == 'n':
    #         break
    #     try:
    #         translation = translator.translate(user_word, dest='en', src='fr').text
    #         print("Translation:", translation)
    #     except Exception as e:
    #         print("Translation error:", str(e))

# Start the first level
# Prompt for the user to start the conversation
# print("Say hello to Hopper!")
# print("When you are finished with the conversation, say \"Au Revior\", which means goodbye!") 
# TODO: Run the example conversation
# TODO: Add user guidance - hint button?
# Initialise the chatbot   
# conversation_loop(first_level)

