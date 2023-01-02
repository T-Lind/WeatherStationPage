# import module
import codecs
import random
import webbrowser

INSERTED_DATA_LEN = 58
START_IDX = 307


def get_temp():
    # TODO: Implement this functionality
    return random.randint(-1, 25)


def get_humidity():
    # TODO: Implement this functionality
    return random.randint(0, 100)


def get_pressure():
    # TODO: Implement this functionality
    return random.randint(90, 110)


def get_lightning_strike():
    # -1 will be convention for no more detections
    # Otherwise will be distance in km.
    return random.randint(-1, 4)


if __name__ == "__main__":
    inserted_string = f"Temp: {get_temp():2}, Humidity: {get_humidity():2}, Pressure:{get_pressure():3}, Recent Lightning: {get_lightning_strike():2}"

    assert len(inserted_string) == INSERTED_DATA_LEN

    file_read = codecs.open("WeatherStationPage.html", 'r', "utf-8")
    data = list(file_read.read())
    file_read.close()

    data[START_IDX:START_IDX + INSERTED_DATA_LEN + 2] = f"\n\t{inserted_string}"

    file_write = codecs.open("WeatherStationPage.html", 'w', "utf-8")
    html_string = ""
    for char in data:
        html_string += char
    file_write.write(html_string)

    file_write.close()

    webbrowser.open("WeatherStationPage.html")
