# JARVIS Assistant

This repository currently contains a Windows-oriented voice-command prototype. It is
being rebuilt into a testable assistant platform. The audit deliberately does not claim
that the existing voice, browser, news, or playback workflows are production-ready.

## Current capabilities

The legacy scripts contain commands for:

- Google speech recognition and a `jarvis` wake word;
- text-to-speech through `pyttsx3`;
- opening fixed websites and web searches;
- requesting Indian headlines from NewsAPI;
- opening or playing entries from a static music dictionary.

There is no active LLM integration yet. `gpt_enhanced.py` contains no executable GPT
client. Grok/xAI integration is planned only after the deterministic core and tests are
in place.

## Prerequisites

- Python 3.12
- Windows for the current voice implementation
- a microphone and supported audio drivers for voice mode
- a NewsAPI key for headlines

## Development setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Set `NEWS_API_KEY` in your process environment before using news. The current scripts
do not automatically load `.env`; that will be added through the configuration layer.

## Verification

```powershell
python -m ruff check .
python -m mypy jarvis
python -m pytest
```

These commands document the target verification workflow. At the audit revision, the
package and tests have not yet been implemented, and no usable Python installation was
available on the audited host.

## Engineering status

Read [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) and
[FINAL_SCORECARD.md](FINAL_SCORECARD.md) before relying on the project. The detailed
implementation order is in [ROADMAP.md](ROADMAP.md).

## Security

The previously committed NewsAPI key must be considered compromised and revoked by its
owner. Source cleanup does not revoke a credential or erase it from Git history. Do not
report credentials in public issues.

## License

No license has been selected yet. Until the owner adds one, normal copyright restrictions
apply and the repository is not an open-source release.

