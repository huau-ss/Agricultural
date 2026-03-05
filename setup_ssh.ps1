# 生成 SSH key 并配置 GitHub

Write-Host "=== 配置 GitHub SSH 连接 ===" -ForegroundColor Green

# 1. 生成 SSH key
$email = Read-Host "请输入你的 GitHub 邮箱"
ssh-keygen -t ed25519 -C $email

Write-Host "`n=== SSH key 已生成 ===" -ForegroundColor Green

# 2. 显示公钥内容
Write-Host "`n请复制以下内容到剪贴板：" -ForegroundColor Yellow
Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard
Get-Content ~/.ssh/id_ed25519.pub

Write-Host "`n公钥已复制到剪贴板！" -ForegroundColor Green
Write-Host "`n下一步：" -ForegroundColor Yellow
Write-Host "1. 访问: https://github.com/settings/keys" -ForegroundColor Cyan
Write-Host "2. 点击 'New SSH key'" -ForegroundColor Cyan
Write-Host "3. Title: 填写名称（如: My PC）" -ForegroundColor Cyan
Write-Host "4. Key: 粘贴刚才复制的公钥" -ForegroundColor Cyan
Write-Host "5. 点击 'Add SSH key'" -ForegroundColor Cyan
Write-Host "`n完成后，按任意键继续..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 3. 测试 SSH 连接
Write-Host "`n测试 SSH 连接..." -ForegroundColor Yellow
ssh -T git@github.com

# 4. 配置 Git 使用 SSH
Write-Host "`n配置 Git 远程仓库使用 SSH..." -ForegroundColor Yellow
git remote remove origin
git remote add origin git@github.com:huau-ss/Agricultural.git

Write-Host "`n=== 配置完成 ===" -ForegroundColor Green
Write-Host "现在可以执行: git push -u origin main" -ForegroundColor Cyan


