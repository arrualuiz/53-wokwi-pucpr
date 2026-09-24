# Roteiro completo — vídeo demonstrativo (até 4 min)

Rascunho detalhado (Claude), com timing sugerido e pontos técnicos a
cobrir em cada bloco. Use como referência; o roteiro de locução
(`roteiro-locucao.md`) é a versão enxuta pra ler/adaptar na hora.

## Estrutura geral (alvo: ~3:30 a 4:00)

| Bloco | Tempo | Conteúdo |
|---|---|---|
| 1. Abertura | 0:00–0:20 | Quem é você, nome do projeto, disciplina, objetivo em 1 frase |
| 2. Arquitetura | 0:20–0:55 | ESP32 + LDR + LED, MQTT, Blynk — como as peças se conectam |
| 3. Simulação rodando | 0:55–1:35 | Wokwi ao vivo: WiFi conectando, MQTT conectando, monitor serial |
| 4. Regra automática | 1:35–2:15 | Escurecer o LDR → LED acende; clarear → LED apaga; ler os logs |
| 5. Dashboard Blynk | 2:15–2:55 | Gauge de luminosidade batendo com o monitor serial, em tempo real |
| 6. Controle manual | 2:55–3:35 | Desligar modo automático, ligar/desligar LED pelo switch do dashboard |
| 7. Fechamento | 3:35–3:55 | Recapitular o que foi mostrado, mencionar o contexto de aplicação |

## Bloco 1 — Abertura (0:00–0:20)

- Diga seu nome, a disciplina e o nome do projeto.
- Uma frase objetivo: "Esse projeto automatiza o acionamento de uma
  lâmpada com base na luminosidade ambiente, usando ESP32, MQTT e um
  dashboard na nuvem."

## Bloco 2 — Arquitetura (0:20–0:55)

Pontos a cobrir (pode ser falado sobre o diagrama do Wokwi ou uma tela
com o `README.md`/`descricao.md` aberta):

- **Sensor:** um LDR (fotoresistor) mede a luminosidade do ambiente.
- **Atuador:** um LED representa a lâmpada.
- **Comunicação:** o ESP32 publica a leitura via **MQTT** para o
  **Blynk Cloud**.
- **Dashboard:** o Blynk mostra os dados em tempo real e permite
  controlar o sistema remotamente.
- Diferencial do seu projeto (evita parecer cópia do projeto-base): é
  automação de **iluminação** (não estação meteorológica), com dois
  modos de operação (automático/manual) e limiar configurável.

## Bloco 3 — Simulação rodando (0:55–1:35)

- Mostre a tela do Wokwi com o circuito (ESP32, LDR, LED).
- Clique em play (▶) se ainda não estiver rodando, ou já mostre rodando.
- Aponte o monitor serial mostrando:
  ```
  Conectando ao WiFi...
  WiFi conectado: (...)
  Conectado ao broker MQTT do Blynk!
  Luminosidade: 75.0% | Auto: True | Limiar: 30% | LED: 0
  ```
- Fale brevemente: "aqui o ESP32 já conectou no WiFi e no broker MQTT do
  Blynk, e está publicando a leitura do sensor a cada 2 segundos."

## Bloco 4 — Regra automática (1:35–2:15)

- Clique no componente LDR no diagrama do Wokwi e arraste o controle de
  luminosidade para bem escuro (perto de 0 lux).
- Mostre o LED do circuito acendendo.
- Aponte a linha do monitor serial mudando para `LED: 1` com
  luminosidade baixa.
- Arraste de volta pra claro (bastante lux) e mostre o LED apagando,
  com `LED: 0` no monitor.
- Fale: "essa é a regra lógica do projeto: quando a luminosidade cai
  abaixo do limiar configurado, o LED acende automaticamente."

## Bloco 5 — Dashboard Blynk (2:15–2:55)

- Troque para a aba/janela do Blynk Console, na página do device
  (Dispositivos → ESP32 Wokwi).
- Mostre o gauge "Luminosidade (%)" com o valor batendo com o que
  aparece no monitor serial do Wokwi (grave as duas telas lado a lado
  se possível, ou alterne rapidamente entre elas).
- Fale: "esse é o dashboard no Blynk Cloud, mostrando em tempo real o
  que o sensor está lendo — dá pra acompanhar de qualquer lugar."

## Bloco 6 — Controle manual (2:55–3:35)

- No dashboard, desligue o switch **"Modo Automático"**.
- Ligue o switch **"LED Manual"** — mostre o LED do Wokwi acendendo em
  resposta ao comando vindo do dashboard.
- Desligue de novo — mostre o LED apagando.
- Fale: "além do modo automático, dá pra assumir o controle manual do
  LED direto pelo dashboard, em qualquer lugar — isso mostra a
  comunicação nos dois sentidos: o ESP32 manda dados pra nuvem, e
  também recebe comandos de volta."

(Opcional, se sobrar tempo: mostre o slider "Limiar (%)" e explique que
dá pra ajustar o ponto em que o LED aciona automaticamente.)

## Bloco 7 — Fechamento (3:35–3:55)

- Recapitule em 1-2 frases: "então esse projeto mostra um sensor de
  luminosidade e um LED se comunicando via MQTT com um dashboard na
  nuvem, com automação e controle remoto."
- Contexto de aplicação (opcional): "isso pode ser aplicado em
  iluminação de corredores, varandas, ou qualquer ambiente onde faça
  sentido economizar energia acendendo a luz só quando necessário."
- Encerre agradecendo/finalizando.

## Dicas de gravação

- Teste o áudio antes de gravar tudo (silêncio de fundo, sem eco).
- Se for gravar em duas janelas (Wokwi + Blynk), considere usar
  gravação de tela inteira e alternar entre as abas, ou dividir a tela
  em duas.
- Não precisa ser perfeito/sem cortes — pode gravar em partes e editar
  depois, contanto que o resultado final mostre o fluxo completo em até
  4 minutos.
