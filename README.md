# CipherLab

**Secure text encryption playground · v1.0**

A small Python desktop app for exploring classic ciphers and authenticated encryption.
Built with CustomTkinter and cryptography. Text processing runs locally with no network calls.

## Features

- Encrypt and decrypt text with Caesar, ROT13, Vigenère, Atbash, Rail Fence, or Fernet.
- Copy output to the clipboard; preserve Unicode, whitespace, and line breaks.
- Generate, show/hide, save, and load Fernet keys.
- Compact dark interface with live educational cipher output, shift buttons, and Ctrl+Enter.
- Fernet uses an explicit Encrypt/Decrypt button to avoid generating new tokens on every keystroke.
- Input validation and clear error messages; automated algorithm tests and GitHub Actions.

## Quick start

Requires Python 3.12+ with Tk support (included in the standard Windows Python installer).
On Linux install your distribution's `python3-tk` package if Tk is missing.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Try it

1. Select **Caesar Cipher**, **Encrypt**, and shift **3**.
2. Enter `Hello World!` and the live output becomes `Khoor Zruog!`.
3. Paste the result into Input, select **Decrypt**, to restore the original text.
4. For Fernet, generate a key and save it. Click **Encrypt text**, then use that same key to decrypt the resulting token. Load the saved key after restarting the app.

For Vigenère, select the algorithm and enter a keyword such as `LEMON`. For Rail Fence, use the −/+ controls or type a rail count from 2 to 100. Atbash needs no key. These five educational ciphers update the output as you type.

## Algorithms and security

| Algorithm | Behavior | Intended use |
| --- | --- | --- |
| Caesar | Shift ASCII A–Z / a–z by an integer, wrapping at 26 | Education only |
| ROT13 | Fixed Caesar shift of 13; applying twice restores the text | Education only |
| Vigenère | Repeating keyword shifts (English letters A–Z) | Education only |
| Atbash | Mirror the ASCII alphabet; no key required | Education only |
| Rail Fence | Zigzag transposition across 2–100 rails | Education only |
| Fernet | AES-128-CBC encryption with HMAC-SHA256 authentication | Authenticated symmetric encryption |

Caesar, ROT13, Vigenère, Atbash, and Rail Fence offer no meaningful confidentiality. Non-ASCII letters (including Bulgarian) remain unchanged in the substitution ciphers. Vigenère advances its keyword only for ASCII letters. Rail Fence rearranges all characters, including spaces, newlines, and Unicode, and restores them on decryption. Fernet supports all UTF-8 text.

Fernet is provided by the [cryptography library](https://cryptography.io/en/latest/fernet/); this project does not implement its own cryptographic primitives. Fernet tokens expose their creation timestamp. The desktop app is an educational project, not an audited secrets manager.

Keys are saved as **plaintext** only when you choose Save key. Protect those files and keep them separately from encrypted messages. A lost key means lost access; anyone with the key can decrypt and forge messages. Keys and messages are not automatically saved. Saving a key does not secure it with a password. Clipboard contents can be read by other applications or clipboard history. `.gitignore` excludes `*.key`; never commit secrets under other extensions either.

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The tests cover cipher examples, wraparound, negative shifts, Unicode, empty text, round trips, invalid keys, wrong keys, malformed tokens, and tampering. GUI behavior is checked separately from these headless tests.

## Structure

```text
CipherLab/
├── main.py
├── gui.py
├── encryption/
│   ├── __init__.py
│   ├── caesar.py
│   ├── rot13.py
│   ├── atbash.py
│   ├── vigenere.py
│   ├── rail_fence.py
│   └── fernet_cipher.py
├── tests/
├── .github/workflows/tests.yml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
```

## Roadmap — v1.1

- Encrypt/decrypt files with explicit destination selection.
- Password-based encryption using a KDF and stored salt.
- Windows executable packaging with PyInstaller.

File encryption and password-based encryption are not included in v1.0.

## License

MIT — see [LICENSE](LICENSE).
