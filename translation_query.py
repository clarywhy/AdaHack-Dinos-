# External imports
from googletrans import Translator

def translate_unknown_phrases():
    """ Prompts user to input any phrases they didn't understand. """
    
    initial_input = input("Were there any phrases Hopper used that you didn't understand? Y or N ")
    
    if "y" in initial_input.lower:
        
        # Flag for if the user has phrases they didn't understand
        more_words = True
        
        # Create a translator object
        translator = Translator()
        
        
        # Whilst a user has more things they want to translate
        while more_words:
            
            # Prompt user for input
            user_word = input("Type them in here and we'll give you the English translation: ")
            
            # Print translated response
            print(translator.translate(user_word, src="fr", dest="en").text)
            
            # Ask user if they have more to say
            more_words_response = input("Do you have anything else you want to translate into English? Y or N ")
            
            if "n" in more_words_response.lower:
                more_words = False