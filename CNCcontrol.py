import serial
import time
def connect_cnc(SERIAL_PORT, BAUD_RATE = 115200):
    try:
        cnc_serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"{SERIAL_PORT} connected, baud rate: {BAUD_RATE}")
        time.sleep(2)
        return cnc_serial
    except Exception as e:
        print(f"Can not connect to device: {e}")
        exit()
        return None
def send_gcode(command, cnc_serial):
    cnc_serial.write((command + "\n").encode())
    time.sleep(0.05) 
    response = cnc_serial.readline().decode().strip()
    return response
def operate_gcode(commands, cnc_serial):
    for cmd in commands:
        send_gcode(cmd, cnc_serial)
    print(f"operating {commands}")
def get_position(cnc_serial):
    cnc_serial.write(b"?\n")  
    run = True
    isrunning = None
    while run:
        response = cnc_serial.readline().decode().strip()
        if response.startswith("<"):
            run = False
            if response[1] == 'R':
                isrunning = True
            else:
                isrunning = False
        elif response:
            run = True
    return isrunning

# wait until end
def wait_until_end(cnc_serial):
    while True:
        status = get_position(cnc_serial)
        if status == False:
            print('Running Complete')
            break
        time.sleep(0.01)
def operate_until_end(commands,cnc_serial):
    operate_gcode(commands,cnc_serial)
    wait_until_end(cnc_serial)