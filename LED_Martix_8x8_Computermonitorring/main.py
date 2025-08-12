
#This program, written by TS on 12.08.2025 (version 1.0), monitors system RAM, CPU,
#and GPU utilisation, packs the four percentages into a single 32‑bit integer, and transmits the
#result over a serial link to an RP2040 microcontroller.


import psutil
import pynvml
import serial
import time
import serial.tools.list_ports
from pynvml import nvmlDeviceGetMemoryInfo
#Search all connected serial ports and return the device path of the RP2040.
def find_rp2040_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'CH9102' in port.description or 'USB Serial Device' in port.description:
            return port.device
    return None
# Open a serial connection to the RP2040.
def init():
    serial_port = find_rp2040_port()
    if serial_port is None:
        print("RP2040 Not found!")
    arduino = serial.Serial(serial_port, baudrate=9600, timeout=10)
    if(arduino.isOpen()):
        print("Port is already open")
    else:
       arduino.open()
    return arduino
# Calculate the percentage of total system RAM currently in use.
def get_vram_usage():

    memory_info = psutil.virtual_memory()
    vram_usage = memory_info.used / memory_info.total
    #over 100% not possible
    if(vram_usage>100):
        return 100

    return vram_usage
# Return the percentage of VRAM currently used on the  GPU.
def get_gpu_usage():
    pynvml.nvmlInit()
    device_id = 0
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)
    gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle).gpu
    pynvml.nvmlShutdown()
    return gpu_utilization

# Return the percentage of VRAM currently used on the first GPU.
def get_gpu_vram_usage():
    pynvml.nvmlInit()
    device_id = 0
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)
    gpu_vram = (nvmlDeviceGetMemoryInfo(gpu_handle).used / nvmlDeviceGetMemoryInfo(gpu_handle).total)*100
    pynvml.nvmlShutdown()
    return gpu_vram

# Pack four 8‑bit values into a single 32‑bit integer.
#
#    The order corresponds to:
#    - value4:  bits 24‑31  (e.g. GPU‑VRAM %)
#    - value3:  bits 16‑23  (GPU %)
#    - value2:  bits 8‑15   (RAM %)
#    - value1:  bits 0‑7    (CPU %)

def output(value4,value3,value2,value1): #send to rp2040
    wert = (value4 << 24) + (value3 << 16) + (value2 << 8) + value1
    print(f"CPU: {value1}, CPU_RAM: {value2}, GPU: {value3}, GPU_RAM: {value4}, all_value: {wert}")  #
    return wert


#   Main loop: read system stats, pack them, and send to the RP2040.
def main(arduino):
    while True:

        vram_gpu= int(get_gpu_vram_usage())
        gpu_useage= int(get_gpu_usage())
        ram_cpu= int(psutil.virtual_memory().percent)
        cpu_useage= int(psutil.cpu_percent())

        wert= output(vram_gpu, gpu_useage, ram_cpu, cpu_useage)
        all_values = [wert]
        for i in range(len(all_values)):
            time.sleep(0.1)
        time.sleep(1)
        arduino.write(f"{wert}\n".encode()) #send all data


if __name__ == "__main__":
    arduino = init()
    main(arduino)


