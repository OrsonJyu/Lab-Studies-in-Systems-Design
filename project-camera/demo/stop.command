#!/bin/bash
# macOS: double-click to run "demo.py stop" (停止录制). On Linux run: python3 project-camera/demo/demo.py stop
cd "$(dirname "$0")/../.." || exit 1
python3 project-camera/demo/demo.py stop "$@"
status=$?
echo
read -r -p "按回车关闭窗口… " _
exit $status
