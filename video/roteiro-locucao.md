# Roteiro de locução — vídeo demonstrativo

Versão enxuta pra ler/adaptar na hora de gravar. Edite à vontade — a
ideia é soar natural, não decorado. Ajuste nomes, gírias, e o que quiser.
Versão detalhada com mais contexto técnico: `roteiro-completo.md`.

---

**[0:00] Abertura**

> "Oi, meu nome é [SEU NOME], e esse é o meu projeto da Atividade
> Somativa 2 de Internet das Coisas: um sistema de automação de
> iluminação usando ESP32, MQTT e um dashboard na nuvem com o Blynk."

**[0:20] Arquitetura**

> "A ideia é simples: um sensor de luminosidade, um LDR, mede o quanto
> de luz tem no ambiente. Um LED representa a lâmpada. O ESP32 lê o
> sensor e publica esse valor via MQTT pro Blynk Cloud, e o dashboard
> mostra tudo em tempo real, além de permitir controlar o sistema de
> qualquer lugar."

**[0:55] Simulação rodando**

> "Aqui no Wokwi está a simulação rodando. No monitor serial dá pra ver
> que o ESP32 já conectou no WiFi e no broker MQTT do Blynk, e está
> publicando a luminosidade a cada 2 segundos."

*(mostrar tela do Wokwi com monitor serial)*

**[1:35] Regra automática**

> "Agora vou simular o ambiente escurecendo..."

*(arrastar o controle do LDR pra escuro)*

> "...e o LED acende sozinho, porque a luminosidade caiu abaixo do
> limiar configurado. Se eu clarear de novo..."

*(arrastar de volta pra claro)*

> "...o LED apaga automaticamente."

**[2:15] Dashboard Blynk**

> "Trocando pro dashboard do Blynk, dá pra ver o mesmo valor de
> luminosidade em tempo real, num gauge — isso permitiria monitorar o
> sistema remotamente, de qualquer lugar com internet."

*(mostrar gauge do Blynk batendo com o monitor serial)*

**[2:55] Controle manual**

> "Além do modo automático, o dashboard também permite controle manual.
> Vou desligar o modo automático aqui..."

*(desligar switch "Modo Automático")*

> "...e ligar o LED manualmente pelo switch..."

*(ligar "LED Manual", mostrar o LED acendendo no Wokwi)*

> "...e desligar de novo. Isso mostra que a comunicação funciona nos
> dois sentidos: o ESP32 manda dados pra nuvem, e também recebe
> comandos de volta."

**[3:35] Fechamento**

> "Então é isso: um sensor e um atuador conversando via MQTT com um
> dashboard na nuvem, com uma regra de automação e controle remoto.
> Obrigado!"

---

## Checklist antes de gravar

- [ ] Simulação do Wokwi rodando e estável (sem erros no monitor serial)
- [ ] Dashboard do Blynk aberto e atualizando ao vivo
- [ ] MQTTX desconectado (evita brigar pela conexão com o ESP32)
- [ ] Áudio testado (sem ruído/eco)
- [ ] Cronômetro de olho — o vídeo tem que ficar até 4 minutos
