from typing import List
import serial
import serial.tools.list_ports as prtlst
from serial.tools import list_ports_common
import time

SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 12

def list_serial_ports() -> list_ports_common.ListPortInfo:
    ports = prtlst.comports()
    if len(ports) == 0:
        print("No serial port available")
        exit(1)
    print("####### Available serial ports #######")
    for port in ports:
        print(port)
    print("####### End of available serial ports #######")
    return ports[0]

def get_AT_serial(port: str) -> serial.Serial:
    return serial.Serial(port, baudrate=SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT)

def ATSend(io: serial.Serial, cmd: str) -> bool:
    if not io.isOpen():
        return False
    print(f"<== Sending:\n{cmd}")
    io.write(cmd.encode())
    time.sleep(1.5)
    ret = io.read_all()
    print(f"==> Received:\n{ret.decode('utf-8')}")

    if b"OK\r\n" in ret:
        return True
    if b"ERROR\r\n" in ret:
        return False
    if ret == b"\r\n":
        return False
    if ret == cmd.encode():
        return True
    if ret == b'':
        return False
    return True

def tryATCmds(io: serial.Serial, cmds: List[str]):
    for i, cmd in enumerate(cmds):
        try:
            res = ATSend(io, cmd)
            if not res:
                print("=== OK")
        except:
            print(f"Error while sending command {cmd}")    
    try:
        io.close()
    except:
        print("Unable to properly close serial connection")

def enableADB():
    default_port = list_serial_ports()
    port = input(f"Choose a serial port (default={default_port.device}) :") or str(default_port.device)
    io = get_AT_serial(port)

    # seems to check if we are in *#0*# mode but apparently not working on the samsung I have
    print("Initial...");
    ATSend(io, "AT+KSTRINGB=0,3\r\n")
    print("Go to emergency dialer and enter *#0*#, press enter when done")
    input()

    print("Gathering information...")
    cmds = []
    cmds.append("AT+VERSNAME=3,2,3\r\n")
    cmds.append("AT+DEVCONINFO\r\n")
    cmds.append("AT+SVCIFPGM=1,1\r\n")
    cmds.append("AT+REACTIVE=1,0,0\r\n") # returns TRIGGERED in case of FRP lock
    tryATCmds(io, cmds)

    print("Enabling USB Debugging (old method)...")
    cmds = []
    cmds.append("AT+DUMPCTRL=1,0\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+SWATD=0\r\n")
    cmds.append("AT+ACTIVATE=0,0,0\r\n")
    cmds.append("AT+SWATD=1\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")

    tryATCmds(io, cmds)

    # new method discovered from Android Tool
    print("Enabling USB Debugging (new method)...")
    cmds = []
    cmds.append("AT+SWATD=0\r\n")
    cmds.append("AT+ACTIVATE=0,0,0\r\n")
    cmds.append("AT+DUMPCTRL=1,0\r\n")
    cmds.append("AT+SWATD=1\r\n")

    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+DEBUGLVC=0,5;\r\n") # new
    cmds.append("AT+KSTRINGB=0,3\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+DEBUGLVC=0,5;\r\n")

    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+DEBUGLVC=0,5;\r\n")
    cmds.append("AT+KSTRINGB=0,3\r\n")
    cmds.append("AT+DUMPCTRL=1,0\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+DEBUGLVC=0,5;\r\n")
    cmds.append("AT+KSTRINGB=0,3\r\n")
    cmds.append("AT+DUMPCTRL=1,0\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+DEBUGLVC=0,5;\r\n")

    tryATCmds(io, cmds)

    print("USB Debugging should be enabled")
    print("If USB Debugging prompt does not appear, try unplug/replug the USB cable")


if __name__ == "__main__":
    enableADB()
