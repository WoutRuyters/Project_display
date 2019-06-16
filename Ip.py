from RPi import GPIO
from subprocess import check_output
import time

# display definiëren
data_bits = [24, 25, 21, 20, 16, 26, 19, 13]
# data_bits = [13, 19, 26, 16, 20, 21, 25, 24]
rs = 5
e = 6

setup_display = [0x38, 0xc, 0x1]
clear_scherm = 0x1
cursor_display = 0xa
newline = 0xc0
cursor_begin = 0x2
ip_getoond = 0


def setup():
    GPIO.setmode(GPIO.BCM)
    for bit in data_bits:
        GPIO.setup(bit, GPIO.OUT)
    GPIO.setup(e, GPIO.OUT)
    GPIO.setup(rs, GPIO.OUT)
    GPIO.output(rs, 1)
    GPIO.output(e, 1)
    print("setup voltooid")


def ip_finder():
    # ip achterhalen
    ips = check_output(['hostname', '--all-ip-addresses'])
    ips = str(ips)
    ip_tussenstap = ips.strip("b'")
    ip = ip_tussenstap.split(" ")
    return ip[0]


def start_display():
    GPIO.output(rs, 0)
    for instruction in setup_display:
        set_data_bits(instruction)
        clock()


def clock():
    GPIO.output(e, 0)
    time.sleep(0.01)
    GPIO.output(e, 1)


def set_data_bits(value):
    mask = 0x80
    for i in range(0, 8):
        if (value & mask) == 0:
            GPIO.output(data_bits[i], 0)
        else:
            GPIO.output(data_bits[i], 1)
        time.sleep(0)

        mask = mask >> 1


def schrijf_letter(woord):
    GPIO.output(rs, 0)
    clock()
    GPIO.output(rs, 1)
    teller = 0
    for letter in woord:
        asc_letter = ord(letter)
        set_data_bits(asc_letter)
        clock()


time.sleep(15)
try:
    setup()
    start_display()
    while True:
        if ip_getoond == 0:
            set_data_bits(clear_scherm)
            ip_adres = ip_finder()
            string_ip = str(ip_adres)
            ip_tekst = "IP-adres:"
            schrijf_letter(ip_tekst)
            set_data_bits(newline)
            schrijf_letter(string_ip)
            ip_getoond += 1


except KeyboardInterrupt as e:
    print(e)

finally:
    GPIO.cleanup()

