@echo off
echo 上传到GitHub...

git add .
git commit -m "修复radius参数问题并清理冗余文件"
git push origin main

echo 完成！
pause
