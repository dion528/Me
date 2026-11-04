# Hermes Agent + Fincept Terminal

Hermes Agent uses Fincept Terminal's data through Fincept's built-in MCP server.

```
Hermes  --MCP over HTTP + bearer token-->  Fincept Terminal (127.0.0.1:41720/mcp, read-only, 53 tools)
```

## Rebuild

```bash
sudo bash stack/setup.sh   # Ubuntu 24.04; safe to rerun
hermes setup               # pick a model provider + API key (not automated)
hermes                     # then ask e.g. "use fincept get_quote for AAPL"
```

## What you get
- `fincept` runs the desktop app. `fincept-headless` runs it on a virtual display (servers, containers).
- `fincept-mcp-token` prints Fincept's MCP bearer token. It's stored encrypted, keyed to this machine's ID.
- Hermes reads the token from `~/.hermes/.env` (`FINCEPT_MCP_TOKEN`), never from this repo.

## Things that will bite you
- **Fincept must be running** or Hermes' `fincept` tools fail to connect.
- **Read-only by design.** `mcp_server/allow_actions=false`. Turn it on only on purpose (it unlocks state-changing tools).
- **New machine = new token.** Rerun `setup.sh` to re-mint it and update `.env`.
- **Data needs the open internet.** Yahoo Finance, SEC EDGAR, DBnomics, IMF and news feeds are all external. In a locked-down network every data tool returns errors even though the link works.
- **The Linux `.deb` (v4.5.1) is broken**: it doesn't bundle Qt 6.8. The script uses the AppImage instead.
- Fincept is AGPL-3.0. The free build's AI features bill against your own LLM keys with no cap.
