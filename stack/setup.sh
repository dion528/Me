#!/usr/bin/env bash
# Rebuild the Hermes Agent + Fincept Terminal stack on a fresh Ubuntu 24.04 box.
# Hermes reaches Fincept's data through Fincept's built-in MCP server (127.0.0.1:41720).
# Idempotent. Run as root (or adapt the /opt and /usr/local paths). No secrets are stored here.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
FINCEPT_VERSION="${FINCEPT_VERSION:-4.5.1}"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

echo "==> System libraries + virtual display"
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq xvfb libopengl0 libegl1 libgl1 libnss3 \
  libxcomposite1 libxdamage1 libxrandr2 libxtst6 libxkbfile1 libasound2t64 libxcb-cursor0 \
  libxcb-icccm4 libxcb-keysyms1 libxcb-render-util0 libxcb-xinerama0 libxcb-xkb1 libxcb-shape0 \
  libxkbcommon-x11-0 libfontconfig1 libdbus-1-3 >/dev/null

echo "==> Fincept Terminal $FINCEPT_VERSION (AppImage, extracted to /opt/fincept)"
# Not the .deb: it does not bundle Qt 6.8 and does not declare it as a dependency.
if [ ! -x /opt/fincept/AppRun ]; then
  curl -fsSL -o "$WORK/fincept.run" \
    "https://github.com/Fincept-Corporation/FinceptTerminal/releases/download/v${FINCEPT_VERSION}/FinceptTerminal-${FINCEPT_VERSION}-linux-x64-setup.run"
  chmod +x "$WORK/fincept.run"
  (cd "$WORK" && ./fincept.run --appimage-extract >/dev/null)
  rm -rf /opt/fincept && mv "$WORK/squashfs-root" /opt/fincept
fi

echo "==> Python data libraries for Fincept's scripts (/opt/fincept-py)"
[ -x /opt/fincept-py/bin/python ] || python3 -m venv /opt/fincept-py
/opt/fincept-py/bin/pip install -q -U pip setuptools wheel
/opt/fincept-py/bin/pip install -q -r /opt/fincept/usr/bin/resources/requirements-numpy2-core.txt edgartools

echo "==> Launchers"
cat > /usr/local/bin/fincept <<'L'
#!/bin/sh
export PATH="/opt/fincept-py/bin:$PATH"
exec /opt/fincept/AppRun "$@"
L
cat > /usr/local/bin/fincept-headless <<'L'
#!/bin/sh
# Fincept on a virtual display, so its MCP server runs on machines with no screen.
export PATH="/opt/fincept-py/bin:$PATH"
exec xvfb-run -a -s '-screen 0 1600x1000x24' /opt/fincept/AppRun "$@"
L
install -m 755 "$HERE/fincept-mcp-token" /usr/local/bin/fincept-mcp-token
chmod +x /usr/local/bin/fincept /usr/local/bin/fincept-headless
/opt/fincept-py/bin/python -c 'import cryptography' 2>/dev/null || /opt/fincept-py/bin/pip install -q cryptography
sed -i '1s|.*|#!/opt/fincept-py/bin/python|' /usr/local/bin/fincept-mcp-token

echo "==> Enable Fincept's MCP server (read-only: state-changing tools stay off)"
mkdir -p ~/.config/Fincept
python3 - ~/.config/Fincept/FinceptTerminal.conf <<'P'
import sys, configparser
p = sys.argv[1]; c = configparser.RawConfigParser(); c.optionxform = str; c.read(p)
c.has_section('mcp_server') or c.add_section('mcp_server')
c.set('mcp_server', 'enabled_at_startup', 'true'); c.set('mcp_server', 'allow_actions', 'false')
with open(p, 'w') as fh: c.write(fh, space_around_delimiters=False)
P

echo "==> Hermes Agent"
export PATH="$HOME/.local/bin:$PATH"
if ! command -v hermes >/dev/null; then
  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh -o "$WORK/hermes-install.sh"
  bash "$WORK/hermes-install.sh" --skip-setup </dev/null
fi

echo "==> Start Fincept, mint its MCP token, link it into Hermes"
if ! curl -sf --max-time 2 http://127.0.0.1:41720/health >/dev/null; then
  nohup fincept-headless >/tmp/fincept-headless.log 2>&1 &
  for _ in $(seq 1 60); do sleep 2; curl -sf --max-time 2 http://127.0.0.1:41720/health >/dev/null && break; done
fi
# The token is created lazily on the first authenticated request; any bearer value triggers it.
curl -s -o /dev/null -X POST http://127.0.0.1:41720/mcp -H 'Authorization: Bearer init' \
  -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":0,"method":"ping"}' || true
sleep 1
touch ~/.hermes/.env && chmod 600 ~/.hermes/.env
sed -i '/^FINCEPT_MCP_TOKEN=/d' ~/.hermes/.env
echo "FINCEPT_MCP_TOKEN=$(fincept-mcp-token)" >> ~/.hermes/.env
if ! grep -qE '^mcp_servers:' ~/.hermes/config.yaml; then
  cat >> ~/.hermes/config.yaml <<'Y'

# Fincept Terminal (read-only market/research data). Requires `fincept-headless` (or `fincept`) running.
mcp_servers:
  fincept:
    url: "http://127.0.0.1:41720/mcp"
    headers:
      Authorization: "Bearer ${FINCEPT_MCP_TOKEN}"
    connect_timeout: 30
Y
fi
hermes mcp test fincept | tail -3
echo
echo "Done. Still yours to do: pick a model provider and key  ->  hermes setup   (or: hermes model)"
