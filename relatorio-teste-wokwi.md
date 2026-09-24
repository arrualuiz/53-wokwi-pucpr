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

### Rodada 5: broker recusa conexão no subscribe (redirect)

```
Mensagem recebida em downlink/redirect -> mqtt://ny3.blynk.cloud:1883
Traceback (most recent call last):
  ...
  File "umqttsimple.py", line 156, in subscribe
  File "umqttsimple.py", line 170, in wait_msg
OSError: -1
```

- **Causa:** o broker genérico `blynk.cloud` aceita a conexão, mas envia uma
  mensagem em `downlink/redirect` apontando para o broker regional da conta
  (`ny3.blynk.cloud`) e fecha a conexão em seguida. O código não tratava
  esse redirecionamento.

**Correção:** usar direto o broker regional, já visto como "Região: NY3" no
Blynk Console: `MQTT_BROKER = "ny3.blynk.cloud"`.

### Rodada 6: conecta e publica, mas o dashboard não atualiza

- Com o broker regional, a conexão MQTT ficou estável e os logs mostravam
  `Luminosidade: 75.0% | ...` a cada ciclo, e o contador de "Mensagens
  usadas" do Blynk Console subia — mas o gauge V0 continuava em 0.
- **Tentativa errada:** trocar os tópicos para minúsculo (`ds/v0`,
  `downlink/ds/v1` etc.), supondo que a API seguisse o padrão da API HTTP
  do Blynk. Não resolveu.
- **Causa real:** confirmada com o assistente de IA do próprio Blynk
  Console — o tópico deve usar o **Pin exatamente como cadastrado no
  datastream**, que neste projeto é maiúsculo (`V0`, `V1`, `V2`, `V3`,
  `V4`), não o nome de exibição ("Luminosidade" etc.) nem minúsculo.

**Correção:** reverter os tópicos para maiúsculo (voltando ao padrão
original `ds/V0`, `downlink/ds/V1` etc.).

### Rodada 7: validação final do dashboard ✅

- Com o broker regional e os tópicos em maiúsculo, o gauge "Luminosidade
  (%)" no Blynk Console passou a atualizar em tempo real (valor 62%
  confirmado ao vivo), e os 5 widgets (gauge, 2 switches, slider, value
  display) estão corretamente vinculados aos datastreams V0–V4.
- Sistema validado de ponta a ponta: ESP32 (Wokwi) → MQTT → Blynk Cloud →
  Dashboard, em ambas as direções (publicação de sensor e comandos do
  dashboard).

### Rodada 8: downlink (comandos do dashboard) não chegava ao ESP32

- Com uplink e gauge funcionando, os switches "Modo Automático" e "LED
  Manual" no dashboard não tinham nenhum efeito no LED simulado, e nenhuma
  mensagem aparecia no monitor serial ao clicar neles.
- **Diagnóstico com MQTTX:** conectado em `ny3.blynk.cloud:1883` com
  `user=device` / `password=<token>`, inscrito em `downlink/ds/#`, o clique
  no switch "Modo Automático" no dashboard chegou como:
  `Topic: downlink/ds/Modo Automatico` (nome do datastream, com espaço),
  e **não** `downlink/ds/V1` (o Pin).
- **Causa:** ao contrário do uplink (que aceita `ds/V0` pelo Pin), o
  downlink usa o **nome do datastream** cadastrado no Blynk Console, não o
  identificador do Pin. A resposta da IA do Blynk sobre isso estava errada;
  o teste empírico com MQTTX foi decisivo.

**Correção no `main.py`:** assinar e comparar pelos nomes exatos dos
datastreams (`Modo Automatico`, `Limiar`, `LED Manual`) em vez de
`V1`/`V2`/`V3`.

**Validação final (log real):**

```
Luminosidade: 75.0% | Auto: True | Limiar: 30% | LED: 0
Mensagem recebida em downlink/ds/Modo Automatico -> 0
Luminosidade: 75.0% | Auto: False | Limiar: 30% | LED: 0
Mensagem recebida em downlink/ds/LED Manual -> 1
Luminosidade: 75.0% | Auto: False | Limiar: 30% | LED: 1
Mensagem recebida em downlink/ds/LED Manual -> 0
Luminosidade: 75.0% | Auto: False | Limiar: 30% | LED: 0
```

Modo automático desligado, controle manual do LED ligando e desligando —
tudo respondendo em tempo real via MQTT.

## Configuração final validada

- `MQTT_BROKER = "ny3.blynk.cloud"` (broker regional direto, evita o
  redirecionamento)
- Autenticação: `user="device"`, `password=<BLYNK_AUTH_TOKEN>`
- Uplink (device → cloud): `ds/V0`, `ds/V4` (usa o Pin)
- Downlink (cloud → device): `downlink/ds/Modo Automatico`,
  `downlink/ds/Limiar`, `downlink/ds/LED Manual` (usa o **nome** do
  datastream, não o Pin — assimetria confirmada via MQTTX)
- `INVERT_LDR = True`

**Referências:** Blynk MQTT: Authentication · Blynk MQTT: Topic Structure ·
Blynk MQTT: Datastreams
