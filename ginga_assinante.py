# Importação de bibliotecas
import enum
from typing import Any, Dict, Optional
import click
from miio import DeviceStatus, MiotDevice
from miio.click_common import EnumType, command, format_output
import paho.mqtt.client as mqtt
import re

class OperationMode(enum.Enum):
    Normal = "normal"
    Nature = "nature"

class MoveDirection(enum.Enum):
    Left = "left"
    Right = "right"

MODEL_FAN_P9 = "dmaker.fan.p9"
MODEL_FAN_P10 = "dmaker.fan.p10"
MODEL_FAN_1C = "dmaker.fan.1c"

MIOT_MAPPING = {
    MODEL_FAN_P9: {
        # Definição das propriedades MIOT para o modelo P9
        # ...
    },
    MODEL_FAN_P10: {
        # Definição das propriedades MIOT para o modelo P10
        # ...
    },
    MODEL_FAN_1C: {
        "power": {"siid": 2, "piid": 1},
        "fan_speed": {"siid": 2, "piid": 2},
        # Adicione outras propriedades conforme a documentação MIOT
    },
}

class FanMiot(MiotDevice):
    _mappings = MIOT_MAPPING

    @command(
        click.argument("speed", type=int),
        default_output=format_output("Setting speed to {speed}")
    )
    def set_speed(self, speed: int):
        if speed not in (1, 2, 3):
            raise ValueError("Invalid speed: %s" % speed)

        return self.set_property("fan_speed", speed)

    @command(
        click.argument("power", type=int),
        default_output=format_output("Fan power is {power}")
    )
    def set_power(self, power: int):
        if power not in (0, 1):
            raise ValueError("Invalid power value: %s" % power)

        return self.set_property("power", power)

def normalize_message(message):
    # Remove espaços e caracteres especiais da mensagem e converte para minúsculas
    message = re.sub(r'[^a-zA-Z0-9]', '', message.lower())
    return message

def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código de resultado {rc}")
    client.subscribe("wind_effect")

def on_message(client, userdata, msg):
    raw_message = msg.payload.decode()
    normalized_message = normalize_message(raw_message)
    print(f"Comando recebido: {raw_message}")
    
    if normalized_message == "on":
        ventilador.set_power(1)
        print("Ventilador ligado.")
    elif normalized_message == "off" or normalized_message == "10":
        ventilador.set_power(0)
        print("Ventilador desligado.")
    else:
        print("Comando inválido.")

def control_fan(ventilador):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()

    while True:
        pass

if __name__ == "__main__":
    ventilador = FanMiot("192.168.0.101", "0f3a2387f3ada8f8f512d970045d87fc")
    
    try:
        control_fan(ventilador)
    except KeyboardInterrupt:
        print("Script encerrado pelo usuário.")
