import json
import requests
import time
requests.packages.urllib3.disable_warnings()

from keyfile import bearerToken, roomId
#Keys and tokens are stored locally in a separate file

def getInterfaceStatus(deviceIp, interfaceName):
    """Get status of interface"""
    getInterfaceURL = f"https://{deviceIp}/restconf/data/ietf-interfaces:interfaces"
    headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
        }
    basicauth = ("admin", "cisco")
    getResp = requests.get(getInterfaceURL, auth=basicauth, headers=headers, verify=False)
    interfaceJSON = getResp.json()
    interfaceData = list(filter(lambda x: interfaceName in x["name"] ,interfaceJSON["ietf-interfaces:interfaces"]["interface"]))
    if interfaceData == []:
        return(f"{interfaceName} - Operational status is down")
    interfaceData = json.loads(json.dumps(interfaceData[0]))
    if interfaceData["enabled"]:
        return(f"{interfaceName} - Operational status is up")
    return(f"{interfaceName} - Operational status is down")


def getLatestMessage():
    """Get latest message from Webex Teams"""
    getMessageUrl = f"https://webexapis.com/v1/messages?roomId={roomId}&max=1"
    headers = { "Accept": "application/json", 
                "Content-type":"application/json",
                "Authorization": bearerToken
            }
    getResp = requests.get(getMessageUrl, headers=headers, verify=False)
    messageJson = getResp.json()
    return messageJson["items"][0]["text"]

def postMessage(messageContent):
    """Post message to Webex Teams"""
    postMessageUrl = "https://webexapis.com/v1/messages"
    headers = { "Accept": "application/json",
                "Content-type":"application/json",
                "Authorization": bearerToken
            }
    body = { "roomId": roomId,
              "text": messageContent
         }
    postResp = requests.post(postMessageUrl, headers=headers, json=body, verify=False)
    postResp = postResp.json()
    return postResp


while True:
    latestMessage = getLatestMessage()
    print(f"Recieved Message: {latestMessage}")
    if latestMessage == "62070088":
        postMessage(getInterfaceStatus("10.0.15.103", "Loopback62070088"))
    time.sleep(1)