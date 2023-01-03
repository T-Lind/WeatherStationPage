import time
import datetime
from string import Template
import random
import codecs

MAX_RECORDED_DATA = 24
TIME_STEP_SECONDS = 1

base_page: str
write_file: codecs.StreamReaderWriter
template: Template

file = codecs.open("BaseWebpage.html", 'r', "utf-8")
base_page = file.read()
file.close()

# Data structure for past information acting as a queue
past_info_day = []
past_info_week = []

template = Template(base_page)


def mean(it):
    sum = 0
    for item in it:
        sum += item
    return sum / len(it)


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


def format_past_week_info():
    ret_str = ""
    for entry in past_info_day:
        ret_str = f"Time: {entry[0]}, Temperature: {entry[1]}, " \
                  f"Pressure: {entry[2]}, Humidity: {entry[3]}, Lightning: {entry[4]}<p></p>" + ret_str
    return ret_str


def update_webpage():
    global template, write_file
    # Substitute variables into the template
    open_webpage()
    date = datetime.datetime.now()
    temp = get_temperature()
    humidity = get_humidity()
    pressure = get_pressure()
    lightning = get_closest_lightning()

    result = template.substitute(temp=temp, humidity=humidity,
                                 pressure=pressure, lightning=lightning,
                                 time=date, previous_data=format_past_week_info(), previous_week_data=past_info_week)
    # Old logging system
    # past_info_day.append(f"Time: {date}, Temperature: {temp}, Pressure: {pressure}, Lightning: {lightning}<p></p>")

    # If it just turned past the hour, record the previous day's average
    if date.hour == 0:
        temps = [past_info_day[x][1] for x in range(len(past_info_day))]
        pressures = [past_info_day[x][2] for x in range(len(past_info_day))]
        humidities = [past_info_day[x][3] >= 0 for x in range(len(past_info_day))]
        lightning_strikes = [past_info_day[x][4] >= 0 for x in range(len(past_info_day))]

        past_info_week.append(f"Day: {date.month} {date.day - 1}"
                              f"Daily low temperature: {min(temps)}, Daily high temperature: {max(temps)}, Daily average temperature: {mean(temps)}<p></p>"
                              f"Daily low pressure: {min(pressures)}, Daily high pressure: {max(pressures)}, Daily average pressure: {mean(pressures)}<p></p>"
                              f"Daily low humidity: {min(humidities)}, Daily high humidity: {max(humidities)}, Daily average humidity: {mean(humidities)}<p></p>"
                              f"Total number of lightning strikes: {sum(lightning_strikes)}<p></p>")

        if len(past_info_week) > 7:
            past_info_week.pop(0)

    if len(past_info_day) > MAX_RECORDED_DATA:
        past_info_day.pop(0)

    past_info_day.append([date, temp, pressure, humidity, lightning])

    write_file.write(result)
    close_webpage()


while True:
    update_webpage()
    time.sleep(TIME_STEP_SECONDS)
