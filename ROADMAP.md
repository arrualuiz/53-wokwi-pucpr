# Roadmap

Acompanhamento da evolução do projeto de automação de iluminação (ESP32 +
MQTT + Blynk), da entrega da Atividade Somativa 2 em diante.

## Concluído

- [x] Definição do escopo: automação de iluminação (LDR + LED), diferente do
  projeto-base (estação meteorológica)
- [x] `main.py`: lógica de leitura do LDR, publicação/assinatura MQTT,
  modo automático/manual
- [x] `umqttsimple.py`: biblioteca MQTT para MicroPython
- [x] `diagram.json`: circuito no Wokwi (ESP32 + LDR + LED), com correção do
  pino do LDR (AO em vez de GND) e conexão do monitor serial
- [x] Template e datastreams (V0–V4) criados no Blynk.Cloud
- [x] Dashboard no Blynk com 5 widgets (gauge, 2 switches, slider, value
  display) vinculados aos datastreams
- [x] Descrição escrita do projeto (`descricao.md`)

## Concluído (cont.)

- [x] Correção do `diagram.json`: LDR ligado no pino AO (não GND) e conexão
  do monitor serial adicionada
- [x] Correção da conexão MQTT: broker `blynk.cloud` (não `mqtt.blynk.cloud`,
  que não resolve) e autenticação `user="device"` + `password=<token>`
  (estava invertido)
- [x] Simulação validada de ponta a ponta: WiFi → MQTT → Blynk conectando
  com sucesso

- [x] Orientação do LDR confirmada: `INVERT_LDR = True` (módulo dá tensão
  maior no escuro), validado com testes em 0,1 lux e 479 lux — ver
  [relatorio-teste-wokwi.md](relatorio-teste-wokwi.md)

- [x] Corrigido redirecionamento de broker (Blynk manda `downlink/redirect`
  para o broker regional `ny3.blynk.cloud`) e o formato correto dos tópicos
  MQTT (Pin exatamente como cadastrado, ex. `V0`, não `v0` nem o nome de
  exibição)
- [x] Dashboard Blynk validado ao vivo: gauge de luminosidade atualizando
  em tempo real com a simulação do Wokwi

- [x] Downlink (comandos do dashboard) corrigido e validado: o tópico usa o
  **nome do datastream** (`downlink/ds/Modo Automatico`, `.../Limiar`,
  `.../LED Manual`), não o Pin — diagnosticado com MQTTX. Modo
  automático/manual e controle do LED testados via dashboard com sucesso.
- [x] Uplink também corrigido para usar o nome do datastream
  (`ds/Luminosidade`, `ds/Estado LED`, não `ds/V0`/`ds/V4`) — descoberto
  via aba "Erros" do Blynk Console (955+ erros de "pino não encontrado")
- [x] Client ID único por execução (`time.ticks_ms()`), eliminando
  desconexões intermitentes por sessão duplicada no broker
- [x] Confirmado que a página real do device (Dispositivos → ESP32 Wokwi)
  mostra o valor real (75%), batendo com o monitor serial — a página de
  preview do template mostra dados aleatórios/fake e não deve ser usada
  como referência
- [x] Roteiro do vídeo criado (`video/roteiro-completo.md` e
  `video/roteiro-locucao.md`)

## Em andamento

- [ ] Gravar vídeo demonstrativo (até 4 min) usando a página real do
  device (nunca o preview do template)
- [ ] Capturas de tela da simulação e do dashboard
- [ ] Montar o `.zip` de entrega e enviar no AVA (prazo estendido: 23/09)

## Próximas melhorias (pós-entrega)

- [ ] Adicionar histórico/gráfico de luminosidade ao longo do tempo no
  dashboard
- [ ] Notificação (push/e-mail) quando o LED for acionado automaticamente
- [ ] Persistir configurações (limiar, modo) na memória flash do ESP32 para
  sobreviver a reinícios
- [ ] Testar em hardware real (ESP32 físico + LDR + LED), não só simulado
- [ ] Adicionar um segundo sensor (ex.: PIR de presença) para lógica mais
  rica: só acender à noite E com presença detectada
