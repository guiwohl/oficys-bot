## discord.py Embeds in one page (LLM-ready)

### What an embed is

An embed is a rich “card” attached to a message (title, description, fields, images, footer, etc.). On the API side it’s the **Embed object** inside a message payload. ([Discord][1])

---

## Create an embed

### Minimal

```py
import discord

embed = discord.Embed(
    title="Title",
    description="Text here",
    color=discord.Color.blurple()
)
```

### Common setters

* `embed.add_field(name="X", value="Y", inline=False)`
* `embed.set_author(name="...", icon_url="...", url="...")`
* `embed.set_footer(text="...", icon_url="...")`
* `embed.set_thumbnail(url="...")`
* `embed.set_image(url="...")`

(These are the standard patterns used in discord.py embed examples.) ([Stack Overflow][2])

---

## Send an embed

### In prefix commands (`ctx`)

```py
@bot.command()
async def test(ctx):
    embed = discord.Embed(title="Hello", description="Embed test")
    await ctx.send(embed=embed)
```

discord.py sends embeds via the `embed=` argument. ([Stack Overflow][2])

### In channels / interactions

* `await channel.send(embed=embed)`
* If you use app commands / interactions, the concept is the same: you include the embed in the send call (the method name differs by framework surface).

---

## Edit a message that contains an embed

Useful for `countdown` if you want embeds instead of plain text.

```py
msg = await ctx.send(embed=embed)

# later
embed.description = "Updated text"
await msg.edit(embed=embed)
```

Editing messages is done via `Message.edit(...)`. ([Python Discord][3])

---

## Embed limits you must obey (or you get “Invalid Form Body”)

Discord embed payload limits are strict. Key ones:

* Title: 256 chars
* Description: 4096 chars
* Max fields: 25
* Field name: 256 chars
* Field value: 1024 chars
* Footer text: 2048 chars
* Author name: 256 chars
* Total characters across all embed parts in a message: 6000
* Up to 10 embeds per message ([Python Discord][3])

Practical takeaway: for `help` / `gameshow` lists, you’ll need pagination if your output grows. ([Python Discord][3])

---

## Best practices (keeps your bot clean)

### 1) Prefer embeds for structured output

* `help`: one embed per “page”
* `now`: one embed with fields per timezone
* `stats`: fields per stat

### 2) Don’t spam edits

Your countdown plan (update every 15s) is good. Don’t do sub-second embed edits or you’ll hit rate limits.

### 3) Use fields for columns, description for narrative

* `description` for short summary
* `add_field` for “Name / Value” items (e.g., “Hours left today: …”)

---

## Drop-in embed templates for your bot

### Help embed skeleton

```py
def build_help_embed(prefix: str) -> "discord.Embed":
    import discord
    e = discord.Embed(title="Oficys — Help", description="Commands:", color=discord.Color.blurple())

    e.add_field(name=f"{prefix}flip a b c", value="Pick one option randomly.", inline=False)
    e.add_field(name=f"{prefix}coin", value="Heads or tails.", inline=False)
    # ... add the rest

    e.set_footer(text="Tip: keep outputs short; paginate when needed.")
    return e
```

### Stats embed skeleton

```py
def build_stats_embed(user_display: str, stats: dict) -> "discord.Embed":
    import discord
    e = discord.Embed(title=f"Stats — {user_display}", color=discord.Color.blurple())
    for cmd, count in stats.items():
        e.add_field(name=cmd, value=str(count), inline=True)
    return e
```

---

## What your LLM/codegen should remember

* Create with `discord.Embed(...)`
* Add structure with `add_field`, `set_footer`, `set_author`, `set_thumbnail`, `set_image`
* Send with `await ctx.send(embed=embed)` ([Stack Overflow][2])
* Edit with `await message.edit(embed=embed)` ([Python Discord][3])
* Enforce embed limits (25 fields / 6000 total chars / etc.) ([Python Discord][3])

[1]: https://discord.com/developers/docs/resources/message?utm_source=chatgpt.com "Messages Resource | Documentation | Discord Developer Portal"
[2]: https://stackoverflow.com/questions/44862112/how-can-i-send-an-embed-via-my-discord-bot-w-python?utm_source=chatgpt.com "How can I send an embed via my Discord bot, w/python?"
[3]: https://www.pythondiscord.com/pages/guides/python-guides/discord-embed-limits/?utm_source=chatgpt.com "Discord Embed Limits - Python Discord"
