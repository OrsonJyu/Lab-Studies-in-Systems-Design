#!/bin/bash
# macOS: double-click to run "demo.py setup" (安装 / 检查). On Linux run: python3 project-camera/demo/demo.py setup
cd "$(dirname "$0")/../.." || exit 1
python3 project-camera/demo/demo.py setup "$@"
status=$?
echo
read -r -p "按回车关闭窗口… " _
exit $status
