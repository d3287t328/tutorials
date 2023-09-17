import json


def get_alarm_attributes(sns_message):
    return {
        'name': sns_message['AlarmName'],
        'description': sns_message['AlarmDescription'],
        'reason': sns_message['NewStateReason'],
        'region': sns_message['Region'],
        'instance_id': sns_message['Trigger']['Dimensions'][0]['value'],
        'state': sns_message['NewStateValue'],
        'previous_state': sns_message['OldStateValue'],
    }


def register_alarm(alarm):
    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":warning: " + alarm['name'] + " alarm was registered"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "_" + alarm['description'] + "_"
                },
                "block_id": "text1"
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Region: *" + alarm['region'] + "*"
                    }
                ]
            }
        ]
    }


def activate_alarm(alarm):
    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":red_circle: Alarm: " + alarm['name'],
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "_" + alarm['reason'] + "_"
                },
                "block_id": "text1"
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Region: *" + alarm['region'] + "*"
                    }
                ]
            }
        ]
    }


def resolve_alarm(alarm):
    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":large_green_circle: Alarm: " + alarm['name'] + " was resolved",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "_" + alarm['reason'] + "_"
                },
                "block_id": "text1"
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Region: *" + alarm['region'] + "*"
                    }
                ]
            }
        ]
    }


with open('sns-alarm-event.json') as f:
    sns_message = json.load(f)
    alarm = get_alarm_attributes(sns_message)
    msg = str()

    if alarm['previous_state'] == "INSUFFICIENT_DATA" and alarm['state'] == 'OK':
        msg = register_alarm(alarm)
    elif alarm['previous_state'] == 'OK' and alarm['state'] == 'ALARM':
        msg = activate_alarm(alarm)
    elif alarm['previous_state'] == 'ALARM' and alarm['state'] == 'OK':
        msg = resolve_alarm(alarm)

    print(msg)
