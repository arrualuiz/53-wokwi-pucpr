# Automação de Iluminação — ESP32 + MQTT + Blynk

Projeto de IoT desenvolvido para a disciplina **Internet das Coisas em um Mundo
Conectado** (PUCPR). Simula, via [Wokwi](https://wokwi.com), um ESP32 em
MicroPython que automatiza o acionamento de uma lâmpada (LED) com base na
luminosidade ambiente, medida por um LDR, com monitoramento e controle remoto
via dashboard no [Blynk Cloud](https://blynk.io).

## Como funciona

- Um **LDR** mede a luminosidade e o valor é publicado via **MQTT** para o
  broker `mqtt.blynk.cloud`.
- Um **LED** acende automaticamente quando a luminosidade cai abaixo de um
  limiar configurável.
- O **dashboard no Blynk** permite acompanhar o nível de luz em tempo real,
  ajustar o limiar, alternar entre modo automático/manual e controlar o LED
  remotamente.

Detalhes completos da lógica e da arquitetura em [descricao.md](descricao.md).

## Estrutura do projeto

| Arquivo | Função |
|---|---|
| `main.py` | Firmware MicroPython: leitura do sensor, lógica de automação, comunicação MQTT |
| `umqttsimple.py` | Biblioteca MQTT minimalista para MicroPython |
| `diagram.json` | Circuito simulado no Wokwi (ESP32 + LDR + LED) |
| `wokwi.toml` | Configuração do simulador Wokwi |
| `descricao.md` | Descrição escrita do projeto (objetivo, arquitetura, dashboard) |

## Rodando o projeto

1. Abra um novo projeto MicroPython para ESP32 em
   [wokwi.com/projects/new/micropython-esp32](https://wokwi.com/projects/new/micropython-esp32).
2. Copie `main.py`, `diagram.json` e crie `umqttsimple.py` com o conteúdo
   deste repositório.
3. Em `main.py`, substitua `BLYNK_AUTH_TOKEN` pelo token do seu device no
   [Blynk.Cloud](https://blynk.cloud) (crie um template com hardware ESP32 e
   os datastreams V0–V4 descritos em `descricao.md`).
4. Rode a simulação (▶) no Wokwi.

## Roadmap

O andamento e as próximas melhorias estão em [ROADMAP.md](ROADMAP.md).
