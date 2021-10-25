import csv
import paho.mqtt.client as mqtt
from datetime import datetime
import json

f_csv = open('data.csv', 'a',newline='')
write = csv.writer(f_csv,delimiter=';')
write.writerow(['sound',  'illumination',  'voltage', 'time'])
lastTime = datetime.now()
# Параметры подключения к MQTT-брокеру
HOST = "192.168.1.14" # IP чемодана
PORT = 1883 # Стандартный порт подключения для Mosquitto
KEEPALIVE = 60 # Время ожидания доставки сообщения, если при отправке оно будет привышено, брокер будет считаться недоступным

# Словарь с топиками и собираемыми из них параметрами
SUB_TOPICS = {
    '/devices/wb-msw-v3_21/controls/Sound Level': 'sound',
    '/devices/wb-ms_11/controls/Illuminance' : 'illumination',
    '/devices/wb-ms_11/controls/Input Voltage': 'voltage',
}

# Создание словаря для хранения данных JSON
JSON_DICT = {}
for value in SUB_TOPICS.values():
    JSON_DICT[value] = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Подключение ко всем заданным выше топикам
    for topic in SUB_TOPICS.keys():
        client.subscribe(topic)

def on_message(client, userdata, msg):
    global lastTime
    payload = msg.payload.decode() # Основное значение, приходящее в сообщение, например, показатель температуры
    topic = msg.topic # Топик, из которого пришло сообщение, поскольку функция обрабатывает сообщения из всех топиков
    if (datetime.now() - lastTime).total_seconds() >= 5:
        lastTime = datetime.now()
        param_name = SUB_TOPICS[topic]
        JSON_DICT[param_name] = payload
        JSON_DICT['time'] = datetime.strftime(datetime.now(), '%H:%M:%S')
        print(topic + " " + payload)
        print([str(JSON_DICT[i]) for i in JSON_DICT])
        write.writerow([str(JSON_DICT[i]) for i in JSON_DICT])

    # Запись данных в файл
    # with open('data.json', 'a') as file:
    #     json_string = json.dumps(JSON_DICT) # Формирование строки JSON из словаря
    #     file.write(json_string+',\n')


def main():
    # Создание и настройка экземпляра класса Client для подключения в Mosquitto
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, KEEPALIVE)

    client.loop_forever() # Бесконечный внутренний цикл клиента в ожидании сообщений


if __name__ == "__main__":
    main()
