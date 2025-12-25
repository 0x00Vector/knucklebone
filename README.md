# Knucklebone 🦴

**Knucklebone** is a modern, modular Discord bot designed to handle dice rolling and system-specific mechanics for tabletop RPGs, specifically focusing on OSR games.

## Features

- **Generic Roller:** Parse complex dice expressions (e.g., `/roll 4d6kh3`, `/roll 1d20+5`) using the powerful `d20` library.
- **Mörk Borg Support:**
  - `/mb check`: Handles standard DR tests, automatically flagging **Critical Successes** (Nat 20) and **Fumbles** (Nat 1).
  - `/mb reaction`: Automates the 2d6 reaction roll table.
- **Async Architecture:** Built on `discord.py` 2.0+ with `aiosqlite` for non-blocking database operations.
- **Dockerized:** Ready for easy deployment with `docker-compose`.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- A Discord Bot Token (from the [Discord Developer Portal](https://discord.com/developers/applications))

### Installation (Docker)

This is the recommended way to run the bot.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/0x00Vector/knucklebone.git
   cd dicebot
   ```

2. **Configure the environment:**
   Create a `.env` file in the root directory:
   ```bash
   DISCORD_TOKEN=your_token_here
   GUILD_ID=your_debug_guild_id_optional
   ```

3. **Run the bot:**
   ```bash
   docker-compose up -d --build
   ```

### Local Development

If you prefer running without Docker for development:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the bot:**
   ```bash
   # Linux/macOS
   export DISCORD_TOKEN=your_token_here
   python -m bot.main

   # Windows (PowerShell)
   $env:DISCORD_TOKEN="your_token_here"
   python -m bot.main
   ```

## Project Structure

```text
dicebot/
├── bot/
│   ├── cogs/          # Modular command extensions
│   │   ├── general.py # Generic /ping and /roll
│   │   └── morkborg.py# Mörk Borg specific logic
│   ├── db.py          # Async SQLite wrapper
│   └── main.py        # Entry point and bot setup
├── data/              # Persistent database storage
├── Dockerfile
└── requirements.txt
```

## Roadmap

- [ ] Character persistence (save stats/HP)
- [ ] Pirate Borg support (naval combat, black powder)
- [ ] Cy_Borg support (glitches)
- [ ] Initiative tracking
- [ ] More OSR games

## License

This project is licensed under the [MIT License](LICENSE).

## Legal

### MÖRK BORG
Knucklebone is an independent production by 0x00Vector and is not affiliated with Ockult Örtmästare Games or Stockholm Kartell. It is published under the MÖRK BORG Third Party License.

MÖRK BORG is copyright Ockult Örtmästare Games and Stockholm Kartell.
