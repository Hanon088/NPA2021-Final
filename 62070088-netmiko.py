from netmiko import ConnectHandler

def getDataFromDevice(params, command):
    """Send command to device and return the result"""
    with ConnectHandler(**params) as ssh:
        result = ssh.send_command(command)
        return result

def checkForInterface(params, interfaceName):
    """Check if interface exists"""
    return getDataFromDevice(params, f"sh ip int br | include {interfaceName}") != ""

def createLoopback(params, loopbackNumber):
    """Create loopback interface with loopbackNumber"""

def deleteLoopback(params, loopbackNumber):
    """Delete loopback interface with loopbackNumber"""