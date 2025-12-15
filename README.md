# Oficys Bot (Discord)

Bot simples em `discord.py` (prefixo `&`) com comandos de diversão, tempo e listinha de jogos + stats por usuário.

## Requisitos

- Python 3.10+
- Um bot criado no Discord Developer Portal (token)
- **Privileged Gateway Intents**: habilite **Message Content Intent** (o bot usa prefix commands)

## Setup rápido

1) Crie/ative um venv (opcional, mas recomendado):

```bash
python -m venv .venv
source .venv/bin/activate
```

2) Instale as dependências:

```bash
pip install -r bot/requirements.txt
```

3) Crie `bot/.env`:

```env
BOT_TOKEN=coloque_seu_token_aqui
# APP_ID=opcional
```

4) Rode:

```bash
./run_bot.sh
```

Atalho: `./run_bot.sh --install` instala `bot/requirements.txt` antes de iniciar.

## Comandos

Prefixo padrão: `&`

- `&help` — lista comandos e exemplos
- `&flip a b c` — escolhe uma opção aleatória entre 2+
- `&coin` — cara ou coroa
- `&roll 20` — número aleatório de 1 a N
- `&8ball vou treinar hoje?` — respostas estilo “bola 8”
- `&now` — horários em vários fusos + info do dia
- `&countdown 7` — contagem regressiva (edita a mensagem a cada 15s)
- `&timeuntil 31/12/2025` — quanto falta até uma data
- `&gamedump Nome do Jogo 8` — salva/atualiza jogo + nota (0–10)
- `&gameshow` (opcional: `>7` / `<7`) — lista seus jogos
- `&randomgame` (opcional: `>7` / `<7`) — escolhe um jogo aleatório
- `&stats` — estatísticas simples de uso

## Configuração

- `BOT_TOKEN` (obrigatório): token do bot (em `bot/.env`)
- `APP_ID` (opcional): application id do bot (em `bot/.env`)
- `LOG_LEVEL` (opcional, default `INFO`): nível de log do app
- `DISCORD_LOG_LEVEL` (opcional, default `WARNING`): nível de log do `discord.py`
- `LOG_FILE` (opcional): caminho para salvar logs em arquivo

Outras configs ficam em `bot/config.py` (ex.: `COMMAND_PREFIX`, `MAIN_TIMEZONE`, `TIMEZONES`).

## Dados

O bot persiste dados locais em `bot/data/store.json` (gitignored):

- `games`: jogos salvos por usuário
- `command_stats`: contador de uso de comandos por usuário

## Segurança

Não commite tokens. Se um token vazar, gere um novo no Developer Portal imediatamente.

