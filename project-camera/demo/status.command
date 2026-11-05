#!/bin/bash
# macOS: double-click to run "demo.py status" (查看状态). On Linux run: python3 project-camera/demo/demo.py status
cd "$(dirname "$0")/../.." || exit 1
python3 project-camera/demo/demo.py status "$@"
status=$?
echo
read -r -p "按回车关闭窗口… " _
exit $status
