# Roteiro de locução — vídeo demonstrativo

Versão enxuta pra ler/adaptar na hora de gravar. Edite à vontade — a
ideia é soar natural, não decorado. Versão detalhada com mais contexto
técnico: `roteiro-completo.md`.

---

**[0:00] Abertura**

> "E aí! Meu nome é Luiz Arrua, e esse aqui é o meu projeto da
> Atividade Somativa 2 de IoT: um sistema que liga e desliga uma luz
> sozinho, dependendo de quanto de claridade tem no ambiente — tudo
> via ESP32, MQTT e um dashboard na nuvem."

**[0:20] Arquitetura**

> "Como funciona? Um sensor de luminosidade, o LDR, fica de olho no
> ambiente. Um LED faz o papel da lâmpada. O ESP32 lê o sensor e manda
> esse dado pra nuvem via MQTT, pro Blynk. E o Blynk devolve um
> dashboard onde eu vejo tudo em tempo real e ainda consigo controlar o
> sistema remotamente, de qualquer lugar."

**[0:55] Simulação rodando**

> "Olha, a simulação já tá rodando aqui no Wokwi. No monitor dá
> pra ver o ESP32 conectando no WiFi, entrando no broker MQTT do Blynk,
> e mandando a leitura de luminosidade a cada 2 segundos, com horário
> real e tudo."

*(mostrar tela do Wokwi com monitor serial rodando)*

**[1:30] Dashboard Blynk**

> "Agora vem a parte legal: no dashboard do Blynk, esse mesmo valor
> aparece aqui, ao vivo, num gauge. Repara que bate certinho com o que
> tá saindo no monitor serial — é o mesmo dado, só que acessível de
> qualquer lugar com internet."

*(mostrar gauge do Blynk batendo com o monitor serial)*

**[2:00] Regra automática**

> "Beleza, e a automação em si? Eu defini um valor de corte: se a
> luminosidade cai abaixo dele, a luz acende sozinha. Pra não precisar
> escurecer a sala inteira agora, vou simular isso subindo esse valor
> direto pelo dashboard..."

*(subir o slider "Limiar" para acima da luminosidade atual, ex: 80)*

> "...prontinho, o LED já acendeu sozinho, porque agora o valor de
> corte ficou maior que a luminosidade atual. Se eu abaixar de novo..."

*(abaixar o slider "Limiar" para abaixo da luminosidade atual, ex: 20)*

> "...ele apaga na hora. Essa é a lógica: comparar o que o sensor lê
> com esse número, e decidir se acende ou não."

**[2:40] Controle manual**

> "E não é só automático, não — dá pra assumir o controle na mão
> também. Vou desligar o modo automático aqui..."

*(desligar switch "Modo Automático")*

> "...e agora eu ligo o LED manualmente, direto pelo switch do
> dashboard..."

*(ligar "LED Manual", mostrar o LED acendendo no Wokwi)*

> "...e desligo de novo. Isso prova que a comunicação vai nos dois
> sentidos: o ESP32 manda dado pra nuvem, e também escuta comando de
> volta."

**[3:20] Fechamento**

> "Resumindo: um sensor e um atuador conversando via MQTT com um
> dashboard na nuvem, automação e controle remoto funcionando juntos.
> Valeu!"

---

## Checklist antes de gravar

- [ ] Simulação do Wokwi rodando e estável (sem erros no monitor serial)
- [ ] Dashboard do Blynk aberto na página real do device (Dispositivos →
  ESP32 Wokwi), não no preview do template
- [ ] MQTTX desconectado (evita brigar pela conexão com o ESP32)
- [ ] Áudio testado (sem ruído/eco)
- [ ] Cronômetro de olho — o vídeo tem que ficar até 4 minutos
