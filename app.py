import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["Menu", "Japanese_Restaurant", "JR_Jia","JR_Pork",
    "Western_Restaurant","WR_AJ","WR_GC",
    "Hot_Pot_Restaurant","HP_Mother","HP_Breath",
    "Random"],
    transitions=[
        {
            "trigger": "advance",
            "source": "Menu",
            "dest": "Japanese_Restaurant",
            "conditions": "is_going_to_Japanese_Restaurant",
        },

        {
            "trigger": "advance",
            "source": ["Random","Japanese_Restaurant"],
            "dest": "JR_Jia",
            "conditions": "is_going_to_JR_Jia",
        },

        {
            "trigger": "advance",
            "source": ["Random","Japanese_Restaurant"],
            "dest": "JR_Pork",
            "conditions": "is_going_to_JR_Pork",
        },

        {
            "trigger": "advance",
            "source": "JR_Jia",
            "dest": "JR_Pork",
            "conditions": "is_going_to_JR_Pork",
        },

        {
            "trigger": "advance",
            "source": "JR_Pork",
            "dest": "JR_Jia",
            "conditions": "is_going_to_JR_Jia",
        },

        {
            "trigger": "advance",
            "source": "Menu",
            "dest": "Western_Restaurant",
            "conditions": "is_going_to_Western_Restaurant",
        },

        {
            "trigger": "advance",
            "source": ["Random","Western_Restaurant"],
            "dest": "WR_AJ",
            "conditions": "is_going_to_WR_AJ",
        },

        {
            "trigger": "advance",
            "source": ["Random","Western_Restaurant"],
            "dest": "WR_GC",
            "conditions": "is_going_to_WR_GC",
        },

        {
            "trigger": "advance",
            "source": "WR_AJ",
            "dest": "WR_GC",
            "conditions": "is_going_to_WR_AJ",
        },

        {
            "trigger": "advance",
            "source": "WR_GC",
            "dest": "WR_AJ",
            "conditions": "is_going_to_WR_GC",
        },

        {
            "trigger": "advance",
            "source": "Menu",
            "dest": "Hot_Pot_Restaurant",
            "conditions": "is_going_to_Hot_Pot_Restaurant",
        },

        {
            "trigger": "advance",
            "source": ["Random","Hot_Pot_Restaurant"],
            "dest": "HP_Mother",
            "conditions": "is_going_to_HP_Mother",
        },

        {
            "trigger": "advance",
            "source": ["Random","Hot_Pot_Restaurant"],
            "dest": "HP_Breath",
            "conditions": "is_going_to_HP_Breath",
        },

        {
            "trigger": "advance",
            "source": "HP_Breath",
            "dest": "HP_Mother",
            "conditions": "is_going_to_HP_Mother",
        },

        {
            "trigger": "advance",
            "source": "HP_Mother",
            "dest": "HP_Breath",
            "conditions": "is_going_to_HP_Breath",
        },


        {
            "trigger": "advance",
            "source": ["Menu","JR_Jia","JR_Pork","WR_AJ","WR_GC","HP_Mother","HP_Breath"],
            "dest": "Random",
            "conditions": "is_going_to_Random",
        },


        {
            "trigger": "advance",
            "source": ["Menu","Japanese_Restaurant", "JR_Jia","JR_Pork","Western_Restaurant","WR_AJ","WR_GC","Hot_Pot_Restaurant","HP_Mother","HP_Breath"],
            "dest": "Menu",
            "conditions": "is_going_to_Menu",
        },
    ],
    initial="Menu",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
