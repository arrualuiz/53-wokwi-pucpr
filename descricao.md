# Automação de Iluminação com ESP32, MQTT e Blynk

**Aluno:** Luiz Arrua
**Disciplina:** Internet das Coisas em um Mundo Conectado — Atividade Somativa 2

## Objetivo

Automatizar o acionamento de uma lâmpada (representada por um LED) em função
do nível de luminosidade ambiente, medido por um LDR (fotoresistor), com
monitoramento e controle remoto via dashboard no Blynk Cloud.

## Arquitetura da solução

O ESP32 (simulado no Wokwi, programado em MicroPython) lê periodicamente o
sinal analógico do LDR, converte para um percentual de luminosidade (0–100%)
e publica esse valor via **MQTT** para o broker regional do **Blynk Cloud**
(`ny3.blynk.cloud`, porta 1883), usando a API nativa de datastreams do Blynk
(tópicos `ds/<nome do datastream>` para publicação e
`downlink/ds/<nome do datastream>` para comandos recebidos do dashboard). O
ESP32 também recebe, via MQTT, os comandos enviados pelo usuário no
dashboard, e decide se o LED deve acender automaticamente ou ser controlado
manualmente.

## Componentes

- **Sensor:** LDR (fotoresistor) em divisor de tensão, ligado ao ADC do
  ESP32 (GPIO34).
- **Atuador:** LED (representando a lâmpada), ligado ao GPIO2 com resistor
  de proteção.

## Lógica de funcionamento

1. A cada 2 segundos, o ESP32 lê o LDR e publica o nível de luminosidade
   (`ds/Luminosidade`, exibido no dashboard como **gauge**, pino V0).
2. Se o **modo automático** (switch, pino V1) estiver ativo, o LED acende
   automaticamente sempre que a luminosidade cair abaixo do **limiar**
   definido no slider (pino V2, padrão 30%) — simulando o anoitecer/ambiente
   escuro.
3. Se o modo automático estiver desativado, o usuário controla o LED
   manualmente pelo switch "LED Manual" (pino V3), direto do dashboard, em
   qualquer lugar.
4. O estado atual do LED é publicado em `ds/Estado LED` (pino V4), permitindo
   acompanhar o resultado da automação em tempo real.

## Dashboard (Blynk)

| Datastream | Elemento | Função |
|---|---|---|
| V0 | Gauge | Nível de luminosidade atual (%) |
| V1 | Switch | Ativa/desativa o modo automático |
| V2 | Slider | Define o limiar (%) que aciona o LED no modo automático |
| V3 | Switch | Controle manual do LED (usado com modo automático desligado) |
| V4 | Value Display | Confirma o estado atual do LED |

## Integração entre as plataformas

- **Wokwi**: simula o hardware (ESP32, LDR, LED) e executa o firmware em
  MicroPython.
- **MQTT (Blynk Cloud)**: transporta os dados do sensor até a nuvem e os
  comandos do dashboard até o dispositivo, em tempo real.
- **Blynk Dashboard**: interface de visualização e controle remoto,
  acessível via navegador ou app, refletindo o estado do sistema físico
  simulado.
- **MQTTX**: usado durante o desenvolvimento para inspecionar os tópicos
  `ds/#` e `downlink/ds/#`, o que foi essencial para descobrir o formato
  exato exigido pela API MQTT do Blynk (o nome do datastream, e não o
  identificador do pino, tanto na publicação quanto na assinatura).

## Personalização em relação ao projeto-base

Diferente da estação meteorológica de referência, este projeto foca em
**automação de iluminação com dois modos de operação (automático/manual)**,
usa um sensor de luminosidade (LDR) em vez de temperatura/umidade, e define
regras e datastreams próprios (limiar ajustável pelo dashboard). As
bibliotecas `umqttsimple.py` seguem o padrão do projeto-base, permitido pelo
enunciado da atividade.
