import requests
import json



def updateAutoAttendant(businessSchedule, teams_token):
    try:
        url = "https://webexapis.com/v1/telephony/config/locations/Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzVhNTEyYTNjLTQ3OGItNDhiNi1iMDA4LWUwYmU3OTg0YWU1OA/autoAttendants/Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2JtVndNbWwwTldKck0wQXdNVFUzTlRNM05TNWhkVEV3TG1KamJHUXVkMlZpWlhndVkyOXQ"

        payload = json.dumps({
        "businessSchedule": businessSchedule
        })
        headers = {
        'Authorization': 'Bearer {}'.format(teams_token),
        'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        #print(response.text)
        return {'status':'success'}

    except requests.exceptions.RequestException as e:
        # handle exception
        print(f'Request Failed: {e}')
        print(response.text)
        return {'status':'error'}


def getAutoAttendantList(teams_token):
    try:
        url = "https://webexapis.com/v1/telephony/config/autoAttendants"

        payload={}
        headers = {
        'Authorization': 'Bearer {}'.format(teams_token),
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        #print(json.loads(response.text))
        return json.loads(response.text)['autoAttendants']
    except requests.exceptions.RequestException as e:
        # handle exception
        print(f'Request Failed: {e}')
        print(response.text)
        return {'status':'error'}

