#!/bin/sh
# Start the recorder and the web page on the ROCK if they are not running.
# Uses config.json next to this script. Logs go to /tmp/recorder.out and /tmp/webview.out.
cd "$(dirname "$0")" || exit 1
started=""
if pgrep -f "recorder.py run" >/dev/null; then
  echo "recorder already running"
else
  setsid nohup python3 recorder.py run --config config.json </dev/null >>/tmp/recorder.out 2>&1 &
  started="$started recorder"
fi
if pgrep -f "webview.py" >/dev/null; then
  echo "web page already running"
else
  setsid nohup python3 webview.py --config config.json </dev/null >>/tmp/webview.out 2>&1 &
  started="$started webview"
fi
sleep 3
for name in "recorder.py run" "webview.py"; do
  if ! pgrep -f "$name" >/dev/null; then
    echo "failed to start: $name (see /tmp/recorder.out, /tmp/webview.out)" >&2
    exit 1
  fi
done
[ -n "$started" ] && echo "started:$started"
exit 0
