from transitions.extensions import GraphMachine

from utils import *

from Message import *

import random


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
#**************************Return to Menu***************************************************

    def is_going_to_Menu(self, event):
        event.message.text='12354'
        text=event.message.text
        print(text)

        return True

    def on_enter_Menu(self, event):
        print("Menu state")
        reply_token = event.reply_token
        send_text_message(reply_token, Message['Main'])

#**************************Japanese Restaurant***************************************************
    def is_going_to_Japanese_Restaurant(self, event):
        text = event.message.text
        return text.lower() == "1" 

    def on_enter_Japanese_Restaurant(self, event):
        print("Japanese Restaurant state")
        reply_token = event.reply_token
        send_text_message(reply_token,Japanese_Restaurant['Restaurant'])

#**************************佳味庭***************************************************
    def is_going_to_JR_Jia(self, event):
        text = event.message.text
        return text.lower() == "1" or text.lower()=="next" or text.lower()=="10"

    def on_enter_JR_Jia(self, event):
        print("JR_Jia state")
        reply_token = event.reply_token
        id=event.source.user_id
        send_multiple_message(reply_token,id,Japanese_Restaurant['Jia']['image'],
        Japanese_Restaurant['Jia']['text'])


#**************************豚讚日式豬排***************************************************
    def is_going_to_JR_Pork(self, event):
        text = event.message.text
        return text.lower() == "2" or text.lower()== "next" or text.lower()=="11"

    def on_enter_JR_Pork(self, event):
        print("JR_Pork state")
        reply_token = event.reply_token
        id=event.source.user_id
        send_multiple_message(reply_token,id,Japanese_Restaurant['Pork']['image'],
        Japanese_Restaurant['Pork']['text'])

#**************************Western Restaurant***************************************************
    def is_going_to_Western_Restaurant(self, event):
        text = event.message.text
        return text.lower() == "2" 

    def on_enter_Western_Restaurant(self, event):
        print("Western Restaurant state")
        reply_token = event.reply_token
        send_text_message(reply_token,Western_Restaurant['Restaurant'])

 #**************************AJ Burger Restaurant***************************************************
    def is_going_to_WR_AJ(self, event):
        text = event.message.text
        return text.lower() == "1" or text.lower()== "next" or text.lower()=="12"

    def on_enter_WR_AJ(self, event):
        print("AJ_Burger state")
        reply_token = event.reply_token
        id=event.source.user_id
        send_multiple_message(reply_token,id,Western_Restaurant['AJ_Burger']['image'],
        Western_Restaurant['AJ_Burger']['text'])


 #**************************Good Cookery***************************************************
    def is_going_to_WR_GC(self, event):
        text = event.message.text
        return text.lower() == "2" or text.lower()== "next" or  text.lower()=="13"


    def on_enter_WR_GC(self, event):
        print("Good Cookery state")
        reply_token = event.reply_token
        id=event.source.user_id
        send_multiple_message(reply_token,id,Western_Restaurant['Good_Cookery']['image'],
        Western_Restaurant['Good_Cookery']['text'])

#**************************Hot Pot Restaurant***************************************************
    def is_going_to_Hot_Pot_Restaurant(self, event):
        text = event.message.text
        return text.lower() == "3" 

    def on_enter_Hot_Pot_Restaurant(self, event):
        print("Hot Pot Restaurant state")
        reply_token = event.reply_token
        send_text_message(reply_token,Hot_Pot_Restaurant['Restaurant'])

 #**************************三媽臭臭鍋 Restaurant***************************************************
    def is_going_to_HP_Mother(self, event):
        text = event.message.text
        return text.lower() == "1" or text.lower()== "next" or text.lower()=="14"

    def on_enter_HP_Mother(self, event):
        print("三媽臭臭鍋 state")
        reply_token = event.reply_token
        id=event.source.user_id
        send_multiple_message(reply_token,id,Hot_Pot_Restaurant['HP_Mother']['image'],
        Hot_Pot_Restaurant['HP_Mother']['text'])


 #**************************大呼過癮***************************************************
    def is_going_to_HP_Breath(self, event):
        text = event.message.text
        return text.lower() == "2" or text.lower()== "next" or text.lower()=="15"


    def on_enter_HP_Breath(self, event):
        print("大呼過癮 state")
        reply_token = event.reply_token
        id=event.source.user_id
        send_multiple_message(reply_token,id,Hot_Pot_Restaurant['HP_Breath']['image'],
        Hot_Pot_Restaurant['HP_Breath']['text'])

 #**************************Random State***************************************************

    def is_going_to_Random(self, event):
        text = event.message.text
        return text.lower() == "0"
    
    
    def on_enter_Random(self, event):
        print("Random State")
        x=random.randint(10,16)
        event.message.text=str(x)
        text=event.message.text
        print(text)

        self.advance(event)
