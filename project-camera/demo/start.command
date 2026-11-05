#!/bin/bash
# macOS: double-click to run "demo.py start" (开始录制). On Linux run: python3 project-camera/demo/demo.py start
cd "$(dirname "$0")/../.." || exit 1
python3 project-camera/demo/demo.py start "$@"
status=$?
echo
read -r -p "按回车关闭窗口… " _
exit $status
