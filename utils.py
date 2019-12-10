import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage,PostbackAction,ButtonsTemplate,ImageSendMessage,TemplateSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_multiple_message(reply_token,userId,imageURL,text):
    line_bot_api = LineBotApi(channel_access_token)
    image_message=ImageSendMessage(
            original_content_url=imageURL,
            preview_image_url=imageURL
    )
    text_message=TextSendMessage(text)
    button=ButtonsTemplate(
        text='  What to do next',
        actions=[
            PostbackAction(label='Next',data='Whatever',text='next'),
            PostbackAction(label='Back to menu',data='Whatever',text='back')
        ]
    )
    template_message=TemplateSendMessage(alt_text='button template',template=button)
    line_bot_api.push_message(userId, image_message)
    line_bot_api.push_message(userId, text_message)
    line_bot_api.push_message(userId, template_message)



    return "OK"
