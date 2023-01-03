import queue
import time
from string import Template
import random
import codecs

base_page: str
write_file: codecs.StreamReaderWriter
template: Template

file = codecs.open("BaseWebpage.html", 'r', "utf-8")
base_page = file.read()
file.close()

past_info = []

template = Template(base_page)


def open_webpage():
    global write_file
    write_file = codecs.open("WeatherStationPage.html", 'w+', "utf-8")


def close_webpage():
    write_file.close()


def get_pressure():
    return random.randrange(90, 110)


def get_temperature():
    return random.randrange(0, 30)


def get_humidity():
    return random.randrange(0, 100)


def get_closest_lightning():
    return random.randrange(-1, 3)

def format_past_info():
    ret_str = ""
    for entry in past_info:
        ret_str = entry+ret_str
    return ret_str

def update_webpage():
    global template, write_file
    # Substitute variables into the template
    open_webpage()
    write_file.write("\b"*len(write_file.read()))
    str_date = time.ctime()
    temp = get_temperature()
    humidity = get_humidity()
    pressure = get_pressure()
    lightning = get_closest_lightning()

    result = template.substitute(temp=temp, humidity=humidity,
                                 pressure=pressure, lightning=lightning,
                                 time=str_date, previous_data=format_past_info())
    past_info.append(f"Time: {str_date}, Temperature: {temp}, Pressure: {pressure}, Lightning: {lightning}<p></p>")
    if len(past_info) > 60:
        past_info.pop(0)
    write_file.write(result)
    close_webpage()


while True:
    update_webpage()
    time.sleep(1)
