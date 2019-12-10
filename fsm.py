from transitions.extensions import GraphMachine

from utils import send_text_message

from Message import *


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_Menu(self, event):
        text = event.message.text
        return text.lower() == "hungry" 


    def on_enter_Menu(self, event):
        print("Menu state")

        reply_token = event.reply_token
        send_text_message(reply_token, Message['Main'])

#**************************Japanese Food***************************************************
    def is_going_to_Japanese_Restaurant(self, event):
        text = event.message.text
        return text.lower() == "1" 

    def on_enter_Japanese_Restaurant(self, event):
        print("Japanese Restaurant state")
        reply_token = event.reply_token
        send_text_message(reply_token,Japanese_Restaurant['Restaurant'])
