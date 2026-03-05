# GitHub 推送解决方案

## 问题：无法连接到 GitHub

如果遇到 `Failed to connect to github.com` 错误，可能是以下原因：

### 解决方案 1：配置代理（如果使用代理）

```bash
# 设置 HTTP 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 如果使用 SOCKS5 代理
git config --global http.proxy socks5://127.0.0.1:7890
git config --global https.proxy socks5://127.0.0.1:7890

# 取消代理设置
# git config --global --unset http.proxy
# git config --global --unset https.proxy
```

### 解决方案 2：使用 SSH 连接（推荐）

SSH 连接通常更稳定，特别是在网络受限的环境中。

#### 步骤 1：检查是否已有 SSH key

```bash
# 检查是否存在 SSH key
ls ~/.ssh/id_ed25519.pub
# 或
ls ~/.ssh/id_rsa.pub
```

#### 步骤 2：如果没有，生成 SSH key

```bash
# 生成新的 SSH key（替换为你的邮箱）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 按 Enter 使用默认路径
# 设置密码（可选，直接按 Enter 跳过）
```

#### 步骤 3：复制公钥

```bash
# Windows PowerShell
cat ~/.ssh/id_ed25519.pub | clip

# 或手动复制文件内容
notepad ~/.ssh/id_ed25519.pub
```

#### 步骤 4：添加到 GitHub

1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key"
3. Title: 填写一个名称（如：My PC）
4. Key: 粘贴刚才复制的公钥内容
5. 点击 "Add SSH key"

#### 步骤 5：使用 SSH URL 连接

```bash
# 删除现有的 HTTPS 远程仓库
git remote remove origin

# 添加 SSH 远程仓库
git remote add origin git@github.com:huau-ss/Agricultural.git

# 验证连接
ssh -T git@github.com

# 推送代码
git push -u origin main
```

### 解决方案 3：使用 GitHub CLI（gh）

```bash
# 安装 GitHub CLI
# Windows: 使用 winget 或下载安装包
# https://cli.github.com/

# 登录
gh auth login

# 推送代码
git push -u origin main
```

### 解决方案 4：检查网络和防火墙

1. **检查网络连接**：
   ```bash
   ping github.com
   ```

2. **检查防火墙设置**：
   - 确保防火墙允许 Git 和 HTTPS 连接

3. **尝试使用不同的 DNS**：
   - 使用 8.8.8.8 或 1.1.1.1

### 解决方案 5：使用 Personal Access Token

如果使用 HTTPS，需要 Personal Access Token 而不是密码：

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置权限：勾选 `repo`（完整仓库权限）
4. 生成后复制 Token（只显示一次）

推送时：
- Username: 你的 GitHub 用户名
- Password: 粘贴刚才生成的 Token

### 当前配置状态

远程仓库已配置为：
```
origin  https://github.com/huau-ss/Agricultural.git
```

分支已重命名为：`main`

### 推荐操作

**如果在中国大陆，强烈推荐使用 SSH 方式**，因为：
- 更稳定
- 不需要每次输入密码
- 不受 HTTPS 连接限制影响

执行以下命令切换到 SSH：

```bash
# 删除 HTTPS 远程仓库
git remote remove origin

# 添加 SSH 远程仓库
git remote add origin git@github.com:huau-ss/Agricultural.git

# 测试 SSH 连接
ssh -T git@github.com

# 如果看到 "Hi huau-ss! You've successfully authenticated..." 说明成功

# 推送代码
git push -u origin main
```


