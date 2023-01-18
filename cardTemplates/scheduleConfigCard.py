from Utilities.Misoutilites import current_time
from Utilities.AutoAttendantAPIs import getAutoAttendantList
from Utilities.Misoutilites import extractAAIdName
import json

    


def getScheduleConfigCard(token):
    return """
        {{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content":{{
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.2",
                "body": [
                    {{
                        "type": "TextBlock",
                        "text": "Auto Attendent Schedule Settings",
                        "size": "Large",
                        "weight": "Bolder"
                    }},
                    {{
                        "type": "FactSet",
                        "separator": true,
                        "facts": [
                            {{
                                "title": "Current Time",
                                "value": "{}"
                            }},
                            {{
                                "title": "Business Hour",
                                "value": "8:00 AM - 5:00 PM"
                            }}
                        ]
                    }},
                    {{
                        "type": "TextBlock",
                        "text": "Today is not a holiday",
                        "isSubtle": true,
                        "size": "Medium",
                        "weight": "Bolder",
                        "horizontalAlignment": "Left"
                    }},
                    {{
                        "type": "TextBlock",
                        "text": "Please select one of the Auto Attendants",
                        "fontType": "Default",
                        "size": "Medium",
                        "weight": "Default",
                        "color": "Default"
                    }},
                    {{
                        "type": "Input.ChoiceSet",
                        "id": "aaList",
                        "value": "original",
                        "choices": {}
                    }},
                    {{
                        "type": "TextBlock",
                        "text": "What would you like to do with the schedule?",
                        "fontType": "Default",
                        "size": "Medium",
                        "weight": "Default",
                        "color": "Default"
                    }},
                    {{
                        "type": "Input.ChoiceSet",
                        "id": "actionSetting",
                        "value": "original",
                        "choices": [
                            {{
                                "title": "Set to today to Holiday/After hour",
                                "value": "holiday"
                            }},
                            {{
                                "title": "Restore to Original schedule",
                                "value": "original"
                            }}
                        ]
                    }}
                ],
                "actions": [
                    {{
                        "type": "Action.Submit",
                        "data": {{
                            "action": "apply"
                        }},
                        "style": "positive",
                        "title": "Proceed Action"
                    }},
                    {{
                        "type": "Action.Submit",
                        "data": {{
                            "action": "cancel"
                        }},
                        "style": "destructive",
                        "title": "Never Mind"
                    }}
                ]
            }}
        }}""".format(current_time(),extractAAIdName(getAutoAttendantList(teams_token=token)) )
