# Oficys - Discord Bot

## _Funcoes:_

Obs: Para explicacao dos comandos foi usado o prefixo ";" que NAO sera o prefixo final

Atual: o prefixo final é `&`.

1. flip (de 2 ou mais argumentos junto com o comando), exemplo: "&flip jogar dormir comer filme"

2. gamedump (inserir nomes de jogos ja jogados, para criar uma grande lista, juntamente com a sua nota pessoal para o jogo de 0-10, pra usar e jogar no gpt pra ele talvez recomendar um jogo bom que vc ainda nao tenha jogado.) exemplo: "&gamedump Minecraft 8"
2.1 gameshow (se usado sozinho, mostra todos os jogos numa lista, se usado com um parametro "maior que" ou "menor que" mostra todos os jogos com aquela ou maior/menor nota.) exemplo: "&gameshow <7" "&gameshow >7" "&gameshow"

3. now (horario agora em diferentes timezones, dia da semana (em um mostrador personalizado, tipo " S  T  Q  :regional_indicator_q:  S  S  D "), quantas horas faltam para o dia acabar, qual o dia do ano (231/365 (or 366))) exemplo: "&now" 

4. countdown (contador em minutos, apenas. O bot envia uma mensagem, e edita ela a acada 15 segundos informando o tempo restante) exemplo: "&countdown 7"

5. coin (diz cara ou coroa, simples assim.) exemplo "&coin"

6. timeuntil (te diz quantos anos (Y) meses (M) dias (d) horas (H) minutos (m) segundos (s) ate esta data) exemplo: "&timeuntil dd/MM/YYYY"

7. 8ball (responde perguntas com respostas aleatórias no estilo “bola 8”)
O usuário faz uma pergunta e o bot responde com algo como “sim”, “não”, “talvez”, “provavelmente”, “sem chance”, etc. Exemplo: "&8ball vou treinar hoje?"

8. help (mostra todos os comandos disponíveis e como usar cada um) Lista os comandos do bot com uma descrição curta e exemplos básicos de uso. Exemplo: "&help"

9. roll (gera um número aleatório entre 1 e N) Exemplo: "&roll 20"

10. stats \(mostra estatísticas simples de uso do bot pelo usuário, tipo quantos flips já usou quantos countdowns quantos jogos salvos) Exemplo: "&stats"

11. randomgame (escolhe aleatoriamente um jogo já salvo no gamedump) Opcional: só acima de certa nota. Exemplo: "&randomgame", "&randomgame >7"
