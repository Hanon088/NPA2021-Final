from cgitb import reset
import re
from unittest import result
from netmiko import ConnectHandler

def getDataFromDevice(params, command):
    """Send command to device and return the result"""
    with ConnectHandler(**params) as ssh:
        result = ssh.send_command(command)
        return result

def checkForInterface(params, interfaceName):
    """Check if interface exists, return True if it does"""
    return getDataFromDevice(params, f"sh ip int br | include {interfaceName}") != ""

def getInterfaceIP(params, interfaceName):
    """Get ip address of interface"""
    command = f"sh ip int {interfaceName} | include Internet address"
    result = getDataFromDevice(params, command)
    ipAddr = re.search("\d+\.\d+\.\d+\.\d+", result).group()
    subnetMask = re.search("/\d+$", result)
    return (ipAddr, subnetMask)

def createLoopback(params, loopbackNumber, ipAddr, subnetMask):
    """Create loopback interface with loopbackNumber"""
    interfaceExists = checkForInterface(params, f"Loopback{loopbackNumber}")
    if interfaceExists:
        interfaceAddr = getInterfaceIP(params, f"Loopback{loopbackNumber}")
        integerForm = "/" + sum([bin(int(i)).count("1") for i in subnetMask.split(".")])
        #if interfaceAddr[0] != ipAddr or interfaceAddr[1] != integerForm:
           # deleteLoopback(params, loopbackNumber)
    if not interfaceExists:
        with ConnectHandler(**params) as ssh:
            ssh.send_config_set([f"int loop {loopbackNumber}", f"ip addr {ipAddr} {subnetMask}"])
        return f"Loopback{loopbackNumber} created"
    return f"Loopback{loopbackNumber} already exists"


def deleteLoopback(params, loopbackNumber):
    """Delete loopback interface with loopbackNumber"""
    interfaceExists = checkForInterface(params, f"Loopback{loopbackNumber}")
    if interfaceExists:
        with ConnectHandler(**params) as ssh:
            ssh.send_config_set([f"no int loop {loopbackNumber}"])
        return f"Loopback{loopbackNumber} deleted"
    return f"Loopback{loopbackNumber} does not exist"

    
if __name__ == '__main__':
    device_ip = "10.0.15.103"
    username = "admin"
    password = "cisco"

    device_params = {"device_type": "cisco_ios",
                    "ip": device_ip,
                    "username": username,
                    "password": password
                    }

    #result = createLoopback(device_params, 62070088, "192.168.1.1", "255.255.255.0")
    result = deleteLoopback(device_params, 62070088)
    print(result)
