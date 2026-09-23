# Relatório de testes: automacao-iluminacao-iot (Wokwi)

**Data:** 23/09/2026
**Projeto:** https://wokwi.com/projects/475827556390004737
**Hardware:** ESP32 DevKit v1 com MicroPython v1.28.0, módulo LDR
(`wokwi-photoresistor-sensor`) no D34 e LED amarelo com resistor de 220 Ω no D2
**Comunicação:** WiFi Wokwi-GUEST e MQTT com o Blynk Cloud

## Conclusão

✅ Funciona de ponta a ponta na simulação. O ESP32 conecta no WiFi e no
broker MQTT do Blynk, publica a luminosidade e o estado do LED a cada 2
segundos, e o LED responde ao LDR como esperado:

| Luz no LDR | Monitor serial | LED |
|---|---|---|
| 0,1 lux (escuro) | `Luminosidade: 0.8% \| Auto: True \| Limiar: 30% \| LED: 1` | Aceso |
| 479 lux (claro) | `Luminosidade: 75.0% \| Auto: True \| Limiar: 30% \| LED: 0` | Apagado |

Log do último teste, depois de todas as correções:

```
Conectando ao WiFi...
WiFi conectado: ('10.10.0.2', '255.255.0.0', '10.0.0.1', '10.0.0.1')
Conectado ao broker MQTT do Blynk!
Luminosidade: 0.8% | Auto: True | Limiar: 30% | LED: 1
...
Luminosidade: 75.0% | Auto: True | Limiar: 30% | LED: 0
```

**O que ainda não foi verificado:** o dashboard do Blynk (gauge V0, switches
V1 e V3, slider V2) não estava visível durante o teste. Os tópicos MQTT do
Blynk usam o nome do datastream (`ds/<nome>`, `downlink/ds/<nome>`), então os
datastreams no Blynk Console precisam se chamar exatamente V0, V1, V2, V3 e
V4. Se tiverem outros nomes, é preciso ajustar os tópicos no `main.py`.

## Histórico

### Rodada 1: nenhuma saída

- Os passos 1 a 3 (aba `main.py`, painel Simulation, botão ▶) funcionaram, e
  a simulação rodou.
- O monitor serial não aparecia na página, e não havia divisória nem aba
  escondida.
- Com o LDR em 0,1 lux, o LED não acendeu.

Causas encontradas no `diagram.json`:

- Faltavam as conexões do monitor serial (`$serialMonitor`).
- O D34 estava ligado no pino GND do módulo LDR (`"ldr1:GND", "esp:D34"`),
  com um resistor de 10k (`r1`) entre o GND e o terra. O correto é ligar o
  D34 no pino AO.
- A suspeita de que também faltava o atributo `env` do MicroPython não se
  confirmou: o firmware carregou sem ele.

**Correção:** o `diagram.json` foi reescrito sem o `r1`, com o LDR ligado em
`ldr1:AO → esp:D34` e `ldr1:GND → esp:GND.1`, e com as conexões
`esp:TX0/RX0 ↔ $serialMonitor` adicionadas. O `main.py` ganhou a flag
`INVERT_LDR`.

### Rodada 2: WiFi OK, MQTT falhou

```
Conectando ao WiFi...
WiFi conectado: ('10.10.0.2', '255.255.0.0', '10.0.0.1', '10.0.0.1')
Traceback (most recent call last):
  File "main.py", line 159, in <module>
  File "main.py", line 130, in main
  File "main.py", line 120, in conectar_mqtt
  File "umqttsimple.py", line 61, in connect
OSError: -202
```

- O erro se repetiu nas duas execuções. O -202 vem da função
  `socket.getaddrinfo` (linha 61 do `umqttsimple.py`) e indica que o nome do
  servidor não foi resolvido.
- **Causa 1:** o host `mqtt.blynk.cloud` não resolve em DNS. O host correto
  é `blynk.cloud`, que resolveu normalmente no teste.
- **Causa 2:** as credenciais estavam trocadas. Pela documentação do Blynk,
  o usuário é `"device"` e a senha é o Auth Token. O código enviava o token
  como usuário e a senha vazia.

**Correção no `main.py`:**

```python
MQTT_BROKER = "blynk.cloud"
...
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT,
                    user="device", password=BLYNK_AUTH_TOKEN, keepalive=45)
```

### Rodada 3: MQTT OK, LDR invertido

- A conexão com o broker funcionou e o loop passou a publicar normalmente.
- Porém, a 500 lux (claro) o monitor mostrava
  `Luminosidade: 24.4% ... LED: 1`, e a 0,1 lux (escuro) mostrava
  `Luminosidade: 99.2% ... LED: 0`.
- **Causa:** o módulo LDR dá tensão mais alta no escuro, então a leitura sai
  invertida.

**Correção:** `INVERT_LDR = True` no `main.py`.

### Rodada 4: validação final ✅

- Reiniciei a simulação com o código salvo.
- No escuro, a leitura foi 0,8% e o LED acendeu. No claro, foi 75,0% e o LED
  apagou.

## Estado final dos arquivos (resumo)

- **`diagram.json`:** ESP32 com `attrs: {}`, LDR com VCC → 3V3, GND → GND.1
  e AO → D34, LED com A → r2 (220 Ω) → D2 e C → GND.2, e serial com
  TX0/RX0 ↔ `$serialMonitor`.
- **`main.py`:** `MQTT_BROKER = "blynk.cloud"`, porta 1883, usuário
  `"device"`, senha igual ao Auth Token, `keepalive=45` e
  `INVERT_LDR = True`.

## Próximos passos sugeridos

- Conferir no Blynk Console os nomes dos datastreams (V0 a V4) e ver se o
  gauge atualiza em tempo real.
- Testar os comandos do dashboard: desligar o modo Auto (V1), mudar o
  limiar (V2) e controlar o LED manualmente (V3).
- Se o broker recusar a conexão, usar o servidor regional que aparece nas
  informações do device (algo como `ny3.blynk.cloud`).

**Referências:** Blynk MQTT: Authentication · Blynk MQTT: Topic Structure
