"""
Projeto: Automacao de Iluminacao com ESP32 + MQTT + Blynk
Disciplina: Internet das Coisas em um Mundo Conectado - Atividade Somativa 2

Cenario: iluminacao automatica de um ambiente (ex.: corredor, varanda).
Um LDR (sensor de luminosidade) mede o nivel de luz ambiente e publica
o valor via MQTT para o Blynk Cloud. Um LED (atuador) representa a
lampada, que acende automaticamente quando o ambiente esta escuro
(abaixo de um limiar configuravel pelo dashboard). Tambem e possivel
assumir controle manual do LED direto pelo dashboard.

Elementos do dashboard Blynk:
  V0 - Gauge  : nivel de luminosidade atual (0-100%)
  V1 - Switch : liga/desliga o MODO AUTOMATICO
  V2 - Slider : define o LIMIAR de luminosidade (0-100%) que aciona o LED
  V3 - Switch : controle MANUAL do LED (usado quando o modo automatico esta desligado)
"""

import network
import time
from machine import Pin, ADC
from umqttsimple import MQTTClient

# ---------------------------------------------------------------------------
# Configuracoes - AJUSTAR conforme seu ambiente Wokwi / device do Blynk
# ---------------------------------------------------------------------------
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

BLYNK_AUTH_TOKEN = "SEU_TOKEN_DO_DEVICE_AQUI"   # gerado ao criar o device no Blynk.Cloud (NAO COMITAR o token real)
MQTT_BROKER = "mqtt.blynk.cloud"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32-iluminacao"

LDR_PIN = 34     # entrada analogica (ADC) ligada ao divisor de tensao com o LDR
LED_PIN = 2      # saida digital ligada ao LED (lampada simulada)

PUBLISH_INTERVAL_MS = 2000  # intervalo entre leituras/publicacoes do sensor

# Alguns modulos de LDR entregam tensao MAIOR no escuro (comportamento invertido).
# Se o LED acender com luz em vez de no escuro, mude para True.
INVERT_LDR = False

# ---------------------------------------------------------------------------
# Estado global do sistema
# ---------------------------------------------------------------------------
auto_mode = True      # V1: True = automatico, False = manual
threshold = 30         # V2: limiar (%) abaixo do qual o LED acende no modo auto
manual_led_state = 0    # V3: estado do LED quando em modo manual

led = Pin(LED_PIN, Pin.OUT)
ldr = ADC(Pin(LDR_PIN))
ldr.atten(ADC.ATTN_11DB)  # permite ler toda a faixa 0-3.3V


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando ao WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("WiFi conectado:", wlan.ifconfig())


def ler_luminosidade_pct():
    """Le o ADC do LDR e converte para uma porcentagem de luminosidade (0-100).
    Ajustar a formula conforme a orientacao do divisor de tensao montado."""
    valor_bruto = ldr.read()          # 0 - 4095
    pct = (valor_bruto / 4095) * 100
    if INVERT_LDR:
        pct = 100 - pct
    return round(pct, 1)


def aplicar_estado_led():
    """Decide o estado do LED com base no modo (automatico ou manual)."""
    global led

    if auto_mode:
        nivel = ler_luminosidade_pct()
        novo_estado = 1 if nivel < threshold else 0
    else:
        novo_estado = manual_led_state

    led.value(novo_estado)
    return novo_estado


def mqtt_callback(topic, msg):
    """Trata comandos recebidos do dashboard Blynk (downlink)."""
    global auto_mode, threshold, manual_led_state

    topic = topic.decode()
    valor = msg.decode()
    print("Mensagem recebida em", topic, "->", valor)

    if topic == "downlink/ds/V1":
        auto_mode = valor == "1"
    elif topic == "downlink/ds/V2":
        threshold = float(valor)
    elif topic == "downlink/ds/V3":
        manual_led_state = int(valor)

    aplicar_estado_led()


def conectar_mqtt():
    client = MQTTClient(
        MQTT_CLIENT_ID,
        MQTT_BROKER,
        MQTT_PORT,
        user=BLYNK_AUTH_TOKEN,
        password="",
        keepalive=60,
    )
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(b"downlink/ds/V1")
    client.subscribe(b"downlink/ds/V2")
    client.subscribe(b"downlink/ds/V3")
    print("Conectado ao broker MQTT do Blynk!")
    return client


def main():
    conectar_wifi()
    client = conectar_mqtt()

    ultima_publicacao = time.ticks_ms()

    while True:
        try:
            client.check_msg()  # processa comandos vindos do dashboard

            agora = time.ticks_ms()
            if time.ticks_diff(agora, ultima_publicacao) >= PUBLISH_INTERVAL_MS:
                nivel = ler_luminosidade_pct()
                estado_led = aplicar_estado_led()

                client.publish(b"ds/V0", str(nivel).encode())
                client.publish(b"ds/V4", str(estado_led).encode())

                print("Luminosidade: {}% | Auto: {} | Limiar: {}% | LED: {}".format(
                    nivel, auto_mode, threshold, estado_led))

                ultima_publicacao = agora

            time.sleep(0.1)
        except OSError as e:
            print("Erro de conexao, reconectando...", e)
            time.sleep(2)
            client = conectar_mqtt()


if __name__ == "__main__":
    main()
