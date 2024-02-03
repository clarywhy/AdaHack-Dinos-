import tkinter as tk 

from chatbot_module import ChatbotLevel, first_level
  
# Top level window 
frame = tk.Tk() 
frame.title("TextBox Input") 
frame.geometry('400x200') 
# Function for getting Input 
# from textbox and printing it  
# at label widget 
  
def printInput(): 
    
    input_1 = inputtxt.get(1.0, "end-1c") 
    lbl_user.config(text = "You: "+input) 
    
    # chatbot = ChatbotLevel(first_level)
    
    # # Add to the user's score if they use key phrases from the lessom
    # for score, words in chatbot.targetWords.items():
    #     for word in words:
    #         if word in input_1.lower():
    #             user_score += score
            
    # # Stop the conversation 
    # if "au revoir" in input_1.lower():
    #     print(chatbot.name + ": Au revoir!")
    #     print("Score:", user_score)
    #     return

    # # Get a response from the chatbot
    # response_1 = chatbot.chatbot.get_response(input_1)

    # # Shot the chatbot response
    # print(chatbot.name + ": ", response_1)
    # lbl_user.config(text = "+chatbot.name: "+response_1) 
    
    
    
    
  
  
lbl = tk.Label(frame, text = "Say Hello to the Hopper!") 
lbl.pack() 

lbl = tk.Label(frame, text = "When you've finished your conversation, say \"Au revoir\"") 
lbl.pack() 
  
# TextBox Creation 
inputtxt = tk.Text(frame, 
                   height = 5, 
                   width = 20) 
  
inputtxt.pack() 
  
# Button Creation 
printButton = tk.Button(frame, 
                        text = "Print",  
                        command = printInput) 
printButton.pack() 
  
# Label Creation 
lbl_user = tk.Label(frame, text = "") 
lbl_user.pack() 

lbl_reply = tk.Label(frame, text = "") 
lbl_reply.pack() 
frame.mainloop() 