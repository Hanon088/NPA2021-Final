import json
import requests
requests.packages.urllib3.disable_warnings()

headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
basicauth = ("admin", "cisco")

def getInterfaceStatus(deviceIp, interfaceName):
    """Get status of interface"""
    getInterfaceURL = f"https://{deviceIp}/restconf/data/ietf-interfaces:interfaces"
    getResp = requests.get(getInterfaceURL, auth=basicauth, headers=headers, verify=False)
    interfaceJSON = getResp.json()
    interfaceData = list(filter(lambda x: interfaceName in x["name"] ,interfaceJSON["ietf-interfaces:interfaces"]["interface"]))
    if interfaceData == []:
        return(f"{interfaceName} - Operational status is down")
    interfaceData = json.loads(json.dumps(interfaceData[0]))
    if interfaceData["enabled"]:
        return(f"{interfaceName} - Operational status is up")
    return(f"{interfaceName} - Operational status is down")

print(getInterfaceStatus("10.0.15.103", "Loopback62070088"))
    