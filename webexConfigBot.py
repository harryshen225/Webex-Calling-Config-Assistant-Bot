import os
import requests
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
import sys
import json
from dotenv import load_dotenv
from cardTemplates.scheduleConfigCard import getScheduleConfigCard
from Utilities.AutoAttendantAPIs import updateAutoAttendant
import time



load_dotenv()
# Retrieve required details from environment variables
bot_email = os.getenv("TEAMS_BOT_EMAIL")
teams_token = os.getenv("TEAMS_BOT_TOKEN")
bot_url = os.getenv("TEAMS_BOT_URL")
bot_app_name = os.getenv("TEAMS_BOT_APP_NAME")
temp_api_token = os.getenv('TEMP_API_TOKEN')

bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    # approved_users=approved_users,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},
    ],
)

if not bot_email or not teams_token or not bot_url or not bot_app_name:
    print(
        "sample.py - Missing Environment Variable. Please see the 'Usage'"
        " section in the README."
    )
    if not bot_email:
        print("TEAMS_BOT_EMAIL")
    if not teams_token:
        print("TEAMS_BOT_TOKEN")
    if not bot_url:
        print("TEAMS_BOT_URL")
    if not bot_app_name:
        print("TEAMS_BOT_APP_NAME")
    sys.exit()


def create_message_with_attachment(rid, msgtxt, attachment):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/messages"
    data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    #print(response)
    return response.json()

def show_card(incoming_msg):
    backupmessage = "This is an example using Adaptive Cards."
    print(json.loads(getScheduleConfigCard(temp_api_token)))
    c = create_message_with_attachment(
        incoming_msg.roomId, msgtxt=backupmessage, attachment=json.loads(getScheduleConfigCard(temp_api_token))
    )
    print(c)
    return ""

# Create a custom bot greeting function returned when no command is given.
# The default behavior of the bot is to return the '/help' command response
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I'm a chat bot. ".format(sender.firstName)
    response.markdown += "type /setaa to get the card"
    return response

# Temporary function to get card attachment actions
def get_attachment_actions(attachmentid):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/attachment/actions/" + attachmentid
    response = requests.get(url, headers=headers)
    return response.json()

# An example of how to process card actions
def handle_cards(api, incoming_msg):
    """
    Sample function to handle card actions.
    :param api: webexteamssdk object
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    m = get_attachment_actions(incoming_msg["data"]["id"])
    if m['inputs']['action'] == 'cancel':
        return "Okay, I will leave it as it is."
    elif m['inputs']['action'] == 'apply':
        res = {}
        if m['inputs']['actionSetting'] == 'holiday':
            res = updateAutoAttendant(businessSchedule='Override Business Hours',teams_token=temp_api_token)
            print('hit holidy')
        elif m['inputs']['actionSetting'] == 'original':
            res = updateAutoAttendant(businessSchedule='Business Hours',teams_token=temp_api_token)
        if res['status']=='success':
            return 'Update Successful!'
        else:
            return 'Update Unsuccessful! Please contact Cloud Earth to assistance!!'

    #return "card action was :-)- {}".format(m["inputs"])

# Set the bot greeting.
bot.set_greeting(greeting)

# Add new commands to the bot.
bot.add_command("/setaa", "show an adaptive card", show_card)
bot.add_command("attachmentActions", "*", handle_cards)


if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=80,debug=True)