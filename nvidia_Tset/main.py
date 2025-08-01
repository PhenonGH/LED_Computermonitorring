import psutil
import time
import pynvml
import serial
import time
import serial.tools.list_ports
from pynvml import nvmlDeviceGetMemoryInfo
from dataclasses import dataclass
from enum import Enum
class modes(Enum):
    LOADOUT = 1
    FAN_1 = 2
    FAN_2 = 3
    FAN_3 = 7

class Fan:
    vertical: bytes
    horizontal: bytes
    pwm: bytes
    value_output: int

def find_rp2040_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Wir suchen nach dem RP2040, indem wir auf den Namen oder die Beschreibung achten
        #if 'RP2040' in port.description or 'Pico' in port.description or 'Raspberry Pi' in port.description:
        if 'CH9102' in port.description or 'USB Serial Device' in port.description:
            return port.device
    return None
def init():
    serial_port = find_rp2040_port()
    if serial_port is None:
        print("RP2040 nicht gefunden! Bitte sicherstellen, dass das Gerät angeschlossen ist.")

    arduino = serial.Serial(serial_port, baudrate=9600, timeout=10)
    if(arduino.isOpen()):
       h=0;
    else:
       arduino.open()
    return arduino



def get_vram_usage():
    # Speicherinformationen abrufen
    memory_info = psutil.virtual_memory()

    # VRAM-Verbrauch in Bytes abrufen
    vram_usage = memory_info.used / memory_info.total
    if(vram_usage>100):
        return 100

    # VRAM-Verbrauch in Megabytes konvertieren
    #vram_usage_mb = vram_usage / (1024 * 1024)

    return vram_usage
def get_gpu_usage():
    # NVIDIA Management Library initialisieren
    pynvml.nvmlInit()

    # ID der ersten GPU abrufen
    device_id = 0

    # GPU-Handle öffnen
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)

    # GPU-Auslastung abrufen
    gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle).gpu

    # NVIDIA Management Library beenden
    pynvml.nvmlShutdown()

    return gpu_utilization



def get_gpu_vram_usage():
    # NVIDIA Management Library initialisieren
    pynvml.nvmlInit()

    # ID der ersten GPU abrufen
    device_id = 0

    # GPU-Handle öffnen
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)

    # GPU-Auslastung abrufen
    gpu_vram = (nvmlDeviceGetMemoryInfo(gpu_handle).used / nvmlDeviceGetMemoryInfo(gpu_handle).total)*100
    print(f"info {gpu_vram}")
    # NVIDIA Management Library beenden
    pynvml.nvmlShutdown()

    return gpu_vram

def main(arduino):
    while True:
        Fan_1 = Fan()
        Fan_2 = Fan()
        Fan_3 = Fan()
        vram_usage_mb = get_vram_usage()
        #print(f"VRAM-Verbrauch: {vram_usage_mb:.2f} MB")

        vram_gpu= int(get_gpu_vram_usage())
        gpu_useage= int(get_gpu_usage())
        ram_cpu= int(psutil.virtual_memory().percent)
        cpu_useage= int(psutil.cpu_percent())


        modi = modes.LOADOUT.value

        #Fan_1.value_output=output(modes.FAN_1.value, 0, Fan_1.pwm, Fan_1.vertical, Fan_1.horizontal)
        #Fan_2.value_output=output(modes.FAN_2.value, 0, Fan_2.pwm, Fan_2.vertical, Fan_2.horizontal)
        #Fan_3.value_output=output(modes.FAN_3.value, 0, Fan_3.pwm, Fan_3.vertical, Fan_3.horizontal)
        wert= output(modes.LOADOUT.value, vram_gpu, gpu_useage, ram_cpu, cpu_useage)

        #all_values = [wert, Fan_1.value_output, Fan_2.value_output, Fan_3.value_output]
        all_values = [wert]

        wert_debug = (ram_cpu<<8);
        vram_gpu = int(get_gpu_vram_usage())
        #wert =(modi<<28) +(vram_gpu<<21) + (gpu_useage <<14) + (ram_cpu<<7) + cpu_useage


        for i in range(len(all_values)):
            #arduino.write(str(all_values[i]).encode())
            time.sleep(0.1)
            print(f"wertzusammen: {all_values[i]}")
            print(f"wertzusammen_hex: {hex(all_values[i])}")
            print(f"wertzusammen: {i}")#
        time.sleep(1)
        #arduino.write(str(wert).encode())
        arduino.write(f"{wert}\n".encode())


        gpu_utilization = get_gpu_usage()

def output(modi,value4,value3,value2,value1):
    wert = (modi << 28) + (value4 << 21) + (value3 << 14) + (value2 << 7) + value1
    #wert = 0x19643219;
    wert = (value4 << 24) + (value3 << 16) + (value2 << 8) + value1
    print(f"CPU: {value1}, CPU_RAM: {value2}, GPU: {value3}, GPU_RAM: {value4}, Zusammen: {wert}")  #
    ##wert =0x174E6E5004
    return wert



















if __name__ == "__main__":
    #while(1):
    #    try:
    arduino = init()
    main(arduino)
     #   except:
      #      print("fhler")

