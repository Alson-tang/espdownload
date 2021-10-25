#!/usr/bin/env python

import os
import sys
import subprocess
import glob
from typing import Tuple

ESP8266 = 'ESP8266'
ESP32 = 'ESP32'
ESP32C3 = 'ESP32-C3'

VERSION_1_5_1 = 'v1.5.1.0'
VERSION_1_6_0 = 'v1.6.0.0'
VERSION_1_6_1 = 'v1.6.1.0'
VERSION_1_6_2 = 'v1.6.2.0'
VERSION_1_7_0 = 'v1.7.0.0'
VERSION_1_7_1 = 'v1.7.1.0'
VERSION_1_7_2 = 'v1.7.2.0'
VERSION_1_7_3 = 'v1.7.3.0'
VERSION_1_7_4 = 'v1.7.4.0'
VERSION_2_0_0 = 'v2.0.0.0'
VERSION_2_1_0 = 'v2.1.0.0'
VERSION_2_2_0 = 'v2.2.0.0'
VERSION_2_2_1 = 'v2.2.1.0'

WROOM_32 = 'WROOM-32'
MINI_1 = 'MINI-1'
WROVER_32 = 'WROVER-32'
PICO = 'PICO'
SOLO = 'SOLO'

g_platforms_list = { 0 : ESP8266, 
                    1 : ESP32, 
                    2 : ESP32C3 }
g_esp8266_versions_list = { 0 : VERSION_1_5_1, 
                            1 : VERSION_1_6_0, 
                            2 : VERSION_1_6_1, 
                            3 : VERSION_1_6_2, 
                            4 : VERSION_1_7_0, 
                            5 : VERSION_1_7_1,
                            6 : VERSION_1_7_2,
                            7 : VERSION_1_7_3,
                            8 : VERSION_1_7_4,
                            9 : VERSION_2_0_0, 
                            10 : VERSION_2_1_0,
                            11 : VERSION_2_2_0, 
                            12 : VERSION_2_2_1 }
g_esp8266_modules_list = { 0 : WROOM_32 }
g_esp32_versions_list = { 0 : VERSION_2_0_0, 
                        1 : VERSION_2_1_0, 
                        2 : VERSION_2_2_0 }
g_esp32_modules_list = { 0: WROOM_32, 
                        1 : MINI_1, 
                        2 : WROVER_32, 
                        3 : PICO, 
                        4 : SOLO }
g_esp32c3_versions_list = { 0 : VERSION_2_2_0 }
g_esp32c3_modules_list = { 0 : MINI_1 }

g_serial_ports_list = {}
g_serial_port_src = ''

g_plarform_index = 0
g_platform_name = ''
g_module_index = 0
g_module_name = ''
g_module_version = ''

g_esptool_path = '/home/esp/esp/esptool/esptool.py'

g_serial_port = ''

def list_platforms():
    for index in g_platforms_list:
        print(index, g_platforms_list[index])

def list_modules():
    print('\r\n', end='')

    if g_platform_name == ESP8266:
        for index in g_esp8266_modules_list:
            print(index, g_esp8266_modules_list[index])
        return

    if g_platform_name == ESP32:
        for index in g_esp32_modules_list:
            print(index, g_esp32_modules_list[index])
        return

    if g_platform_name == ESP32C3:
        for index in g_esp32c3_modules_list:
            print(index, g_esp32c3_modules_list[index])
        return

def list_versions():
    print('\r\n', end='')

    if g_platform_name == ESP8266:
        for index in g_esp8266_versions_list:
            print(index, g_esp8266_versions_list[index])
        return
    if g_platform_name == ESP32:
        for index in g_esp32_versions_list:
            print(index, g_esp32_versions_list[index])
        return
    if g_platform_name == ESP32C3:
        for index in g_esp32c3_versions_list:
            print(index, g_esp32c3_versions_list[index])
        return

def get_platform_index():
    recv_platform_index = input()
    platform_name = g_platforms_list.get(int(recv_platform_index), 'invalid platform parameter')
    if platform_name == 'invalid platform parameter':
        print('invalid platform parameter')
        return False
    else:
        global g_plarform_index
        g_plarform_index = int(recv_platform_index)

        global g_platform_name
        g_platform_name = g_platforms_list[g_plarform_index]

        return True

def get_module_index():
    module_name = ''
    recv_module_index = input()

    if g_platform_name == ESP8266:
        module_name = g_esp8266_modules_list.get(int(recv_module_index), 'invalid esp8266 module parameter')
        if module_name == 'invalid esp8266 module parameter':
            print('invalid esp8266 module parameter')
            return False

    if g_platform_name == ESP32:
        module_name = g_esp32_modules_list.get(int(recv_module_index), 'invalid esp32 module parameter')
        if module_name == 'invalid esp32 module parameter':
            print('invalid esp32 module parameter')
            return False

    if g_platform_name == ESP32C3:
        module_name = g_esp32c3_modules_list.get(int(recv_module_index), 'invalid esp32c3 module parameter')
        if module_name == 'invalid esp32c3 module parameter':
            print('invalid esp32c3 module parameter')
            return False

    global g_module_index
    g_module_index = int(recv_module_index)

    global g_module_name
    g_module_name = module_name

    return True

def get_version_index():
    recv_versions_index = input()

    global g_module_version

    if g_platform_name == ESP8266:
        version = g_esp8266_versions_list.get(int(recv_versions_index), 'invalid esp8266 version parameter')
        if version == 'invalid esp8266 version parameter':
            print('invalid esp8266 version parameter')
            return False
        else:
            g_module_version = version
            return True            
    if g_platform_name == ESP32:
        version = g_esp32_versions_list.get(int(recv_versions_index), 'invalid esp32 version parameter')
        if version == 'invalid esp32 version parameter':
            print('invalid esp32 version parameter')
            return False
        else:
            g_module_version = version
            return True
    if g_platform_name == ESP32C3:
        version = g_esp32c3_versions_list.get(int(recv_versions_index), 'invalid esp32c3 version parameter')
        if version == 'invalid esp32c3 version parameter':
            print('invalid esp32c3 version parameter')
            return False
        else:
            g_module_version = version
            return True

def get_serial_ports_list():
    serial_ports_info = subprocess.Popen('ls /dev/ttyUSB* | tr \' \' \'\n\'', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    serial_ports_info_lines = serial_ports_info.stdout.readlines()
    serial_ports_info_nums = len(serial_ports_info_lines)

    if serial_ports_info_nums == 0:
        return
    else:
        global g_serial_ports_list
        g_serial_ports_list.clear()

        for lines_index in range(serial_ports_info_nums):
            g_serial_ports_list[lines_index] = serial_ports_info_lines[lines_index].decode('utf-8').strip('\r\n')

        return

def list_serial_ports():
    print('\r\n', end='')

    if len(g_serial_ports_list) == 0:
        print('cannot access \'/dev/ttyUSB*\': No such file or directory')
        return False
    else:
        for index in g_serial_ports_list:
            print(index, g_serial_ports_list[index])
        return True

def get_serial_port():
    recv_serial_port_index = input()
    serial_port_src = g_serial_ports_list.get(int(recv_serial_port_index), 'invalid serial ports index parameter')
    if serial_port_src == 'invalid serial ports index parameter':
        print('invalid serial ports index parameter')
        return False
    else:
        global g_serial_port_src
        g_serial_port_src = g_serial_ports_list[int(recv_serial_port_index)]
        return True

def download_firmware():
    firmware_version_path = ''
    firmware_version_boot_path = ''
    firmware_version_user_path = ''
    firmware_version_data_default_path = ''
    firmware_version_blank_path = ''
    firmware_dir = os.path.dirname(os.path.realpath(__file__))

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_5_1:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'esp8266_at_bin_v1.5.1_0', 'ESP8266_AT_Bin_V1.5.1', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_6_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'esp8266_at_bin_v1.6_0', 'ESP8266_AT_Bin_V1.6', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_6_1:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'esp8266_at_bin_v1.6.1', 'ESP8266_AT_Bin_V1.6.1', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_6_2:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266_AT_Bin_V1.6.2', 'ESP8266_AT_Bin_V1.6.2', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_7_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266_AT_Bin_V1.7', 'ESP8266_AT_Bin_V1.7', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_7_1:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266_NonOS_AT_Bin_V1.7.1', 'ESP8266_NonOS_AT_Bin_V1.7.1', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_7_2:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266_NonOS_AT_Bin_V1.7.2_0', 'ESP8266_NonOS_AT_Bin_V1.7.2', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_7_3:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266_NonOS_AT_Bin_V1.7.3_1', 'ESP8266_NonOS_AT_Bin_V1.7.3', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_1_7_4:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266_NonOS_AT_Bin_V1.7.4', 'ESP8266_NonOS_AT_Bin_V1.7.4', 'bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_2_0_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266-IDF-AT_V2.0_0', 'ESP8266-IDF-AT_V2.0', 'ESP8266-IDF-AT_V2.0', 'factory', 'factory_WROOM-02.bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_2_1_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266-IDF-AT_V2.1.0.0', 'ESP8266-IDF-AT_V2.1.0.0', 'ESP8266-IDF-AT_V2.1', 'factory', 'factory_WROOM-02.bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_2_2_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266-IDF-AT_V2.2.0.0', 'ESP8266-AT-V2.2.0.0', 'factory', 'factory_WROOM-02.bin')

    if g_platform_name == ESP8266 and g_module_name == WROOM_32 and g_module_version == VERSION_2_2_1:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP8266-IDF-AT_V2.2.1.0', 'ESP8266-AT-V2.2.1.0', 'factory', 'factory_WROOM-02.bin')

    if g_platform_name == ESP32 and g_module_name == WROOM_32 and g_module_version == VERSION_2_0_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-WROOM-32_AT_Bin_V2.0', 'ESP32-WROOM-32_AT_Bin_V2.0', 'ESP32-WROOM-32_AT_Bin_V2.0', 'factory', 'factory_WROOM-32.bin')

    if g_platform_name == ESP32 and g_module_name == WROOM_32 and g_module_version == VERSION_2_1_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-WROOM-32_AT_Bin_V2.1.0.0', 'ESP32-WROOM-32_AT_Bin_V2.1.0.0', 'ESP32-WROOM-32_AT_Bin_V2.1', 'factory', 'factory_WROOM-32.bin')

    if g_platform_name == ESP32 and g_module_name == WROOM_32 and g_module_version == VERSION_2_2_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-WROOM-32_AT_Bin_V2.2.0.0', 'ESP32-WROOM-32-V2.2.0.0', 'factory', 'factory_WROOM-32.bin')


    if g_platform_name == ESP32 and g_module_name == MINI_1 and g_module_version == VERSION_2_2_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-MINI-1_AT_Bin_V2.2.0.0', 'ESP32-MINI-1_AT_Bin_V2.2.0.0', 'factory', 'factory_MINI-1.bin')


    if g_platform_name == ESP32 and g_module_name == WROVER_32 and g_module_version == VERSION_2_0_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-WROVER_AT_Bin_V2.0', 'ESP32-WROVER_AT_Bin_V2.0', 'ESP32-WROVER_AT_Bin_V2.0', 'factory', 'factory_WROVER-32.bin')

    if g_platform_name == ESP32 and g_module_name == WROVER_32 and g_module_version == VERSION_2_1_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-WROVER_AT_Bin_V2.1.0.0', 'ESP32-WROVER_AT_Bin_V2.1.0.0', 'ESP32-WROVER_AT_Bin_V2.1', 'factory', 'factory_WROVER-32.bin')

    if g_platform_name == ESP32 and g_module_name == WROVER_32 and g_module_version == VERSION_2_2_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-WROVER_AT_Bin_V2.2.0.0', 'ESP32-WROVER_AT_Bin_V2.2.0.0', 'ESP32-WROVER_AT_Bin_V2.2', 'factory', 'factory_WROVER-32.bin')


    if g_platform_name == ESP32 and g_module_name == PICO and g_module_version == VERSION_2_0_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-PICO-D4_AT_Bin_V2.0', 'ESP32-PICO-D4_AT_Bin_V2.0', 'ESP32-PICO-D4_AT_Bin_V2.0', 'factory', 'factory_PICO-D4.bin')

    if g_platform_name == ESP32 and g_module_name == PICO and g_module_version == VERSION_2_1_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-PICO-D4_AT_Bin_V2.1.0.0', 'ESP32-PICO-D4_AT_Bin_V2.1.0.0', 'ESP32-PICO-D4_AT_Bin_V2.1.0.0', 'factory', 'factory_PICO-D4.bin')

    if g_platform_name == ESP32 and g_module_name == PICO and g_module_version == VERSION_2_2_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-PICO-D4_AT_Bin_V2.2.0.0', 'ESP32-PICO-D4_AT_Bin_V2.2.0.0', 'ESP32-PICO-D4_AT_Bin_V2.2.0.0', 'factory', 'factory_PICO-D4.bin')


    if g_platform_name == ESP32 and g_module_name == SOLO and g_module_version == VERSION_2_0_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-SOLO_AT_Bin_V2.0', 'ESP32-SOLO_AT_Bin_V2.0', 'ESP32-SOLO_AT_Bin_V2.0', 'factory', 'factory_SOLO-1.bin')

    if g_platform_name == ESP32 and g_module_name == SOLO and g_module_version == VERSION_2_1_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-SOLO_AT_Bin_V2.1.0.0', 'ESP32-SOLO_AT_Bin_V2.1.0.0', 'ESP32-SOLO_AT_Bin_V2.1', 'factory', 'factory_SOLO-1.bin')

    if g_platform_name == ESP32 and g_module_name == SOLO and g_module_version == VERSION_2_2_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-SOLO_AT_Bin_V2.2.0.0', 'ESP32-SOLO_AT_Bin_V2.2.0.0', 'ESP32-SOLO_AT_Bin_V2.2', 'factory', 'factory_SOLO-1.bin')


    if g_platform_name == ESP32C3 and g_module_name == MINI_1 and g_module_version == VERSION_2_2_0:
        firmware_version_path = os.path.join(firmware_dir, 'firmware', 'ESP32-C3-MINI-1_AT_Bin_V2.2.0.0', 'ESP32-C3-MINI-1-V2.2.0.0', 'factory', 'factory_MINI-1.bin')

    if g_module_version == VERSION_1_5_1 or g_module_version == VERSION_1_6_0 or g_module_version == VERSION_1_6_1 or g_module_version == VERSION_1_6_2 or g_module_version == VERSION_1_7_0 or g_module_version == VERSION_1_7_1 or g_module_version == VERSION_1_7_2 or g_module_version == VERSION_1_7_3 or g_module_version == VERSION_1_7_4:
        firmware_version_boot_path = os.path.join(firmware_version_path, 'boot_v1.7.bin')
        firmware_version_user_path = os.path.join(firmware_version_path, 'at', '1024+1024', 'user1.2048.new.5.bin')

        if os.path.exists(os.path.join(firmware_version_path, 'esp_init_data_default.bin')):
            firmware_version_data_default_path = os.path.join(firmware_version_path, 'esp_init_data_default.bin')
        else:
            firmware_version_data_default_path = os.path.join(firmware_version_path, 'esp_init_data_default_v08.bin')

        firmware_version_blank_path = os.path.join(firmware_version_path, 'blank.bin')

        cmd = '{} {} --chip {} --port {} --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size 2MB-c1 0x0 {} 0x01000 {} 0x1fc000 {} 0xfe000 {} 0x1fe000 {}'.format(sys.executable, g_esptool_path, g_platform_name, g_serial_port_src, firmware_version_boot_path, firmware_version_user_path, firmware_version_data_default_path, firmware_version_blank_path, firmware_version_blank_path)
    else:
        cmd = '{} {} --chip {} --port {} --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size 4MB 0x0 {}'.format(sys.executable, g_esptool_path, g_platform_name, g_serial_port_src, firmware_version_path)

    print('platform is ', g_platform_name)
    print('module is ', g_module_name)
    print('version is ', g_module_version)
    print(cmd)
    subprocess.call(cmd, shell = True)
    return

def main():

    list_platforms()
    ret = get_platform_index()
    if ret == False:
        exit(-1)

    list_modules()
    ret = get_module_index()
    if ret == False:
        exit(-1)

    list_versions()
    ret = get_version_index()
    if ret == False:
        exit(-1)

    get_serial_ports_list()
    ret = list_serial_ports()
    if ret == False:
        exit(-1)
    ret = get_serial_port()
    if ret == False:
        exit(-1)

    download_firmware()

    exit(0)

if __name__ == '__main__':
    main()