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
        return False
    interfaceData = json.loads(json.dumps(interfaceData[0]))
    if interfaceData["enabled"]:
        return True
    return False


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

def setInterfaceStatus(deviceIp, interfaceName, ipAddr, mask, enabled):
    """Set interface status of interfaceName of deviceIp"""
    setInterfaceURL = f"https://{deviceIp}/restconf/data/ietf-interfaces:interfaces/interface={interfaceName}"
    headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
    basicauth = ("admin", "cisco")

    yangSetLoopback = {
    "ietf-interfaces:interface": {
        "name": interfaceName,
        "type": "iana-if-type:softwareLoopback",
        "enabled": enabled
    }
   }
    setResp = requests.put(setInterfaceURL, data=json.dumps(yangSetLoopback), auth=basicauth, headers=headers, verify=False)
    if(setResp.status_code >= 200 and setResp.status_code <= 299):
       return True
    return False

while True:
    latestMessage = getLatestMessage()
    print(f"Recieved Message: {latestMessage}")
    if latestMessage == "62070088":
        interfaceUp = getInterfaceStatus("10.0.15.103", "Loopback62070088")
        if interfaceUp:
            postMessage("Loopback62070088 - Operational status is up")
            continue
        if not interfaceUp:
            postMessage("Loopback62070088 - Operational status is down")
            setInterfaceStatus("10.0.15.103", "Loopback62070088", "192.168.1.1", "255.255.255.0", True)
        interfaceUp = getInterfaceStatus("10.0.15.103", "Loopback62070088")
        if not interfaceUp:
            postMessage("Enable Loopback62070088 - Now the Operational status is still down")
        else:
            postMessage("Enable Loopback62070088 - Now the Operational status is up again")
    time.sleep(1)