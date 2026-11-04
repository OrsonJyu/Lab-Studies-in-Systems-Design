#!/bin/sh
# Stop the recorder (SIGINT, so an open event is saved as partial) and the web page.
pkill -INT -f "recorder.py run"
pkill -f "webview.py"
i=0
while pgrep -f "recorder.py run" >/dev/null && [ $i -lt 30 ]; do
  sleep 1; i=$((i + 1))
done
if pgrep -f "recorder.py run" >/dev/null; then
  echo "recorder still running after 30 s" >&2
  exit 1
fi
echo "stopped"
