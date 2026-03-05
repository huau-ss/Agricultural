# 上传代码到 GitHub 的步骤

## 已完成 ✅
- ✅ 初始化 Git 仓库
- ✅ 添加所有文件到 Git
- ✅ 创建初始提交

## 接下来需要做的：

### 1. 在 GitHub 上创建新仓库
1. 访问 https://github.com 并登录
2. 点击右上角的 "+" → "New repository"
3. 填写仓库信息：
   - Repository name: `Agricultural-Platform`（或你喜欢的名字）
   - Description: `农产品分析决策平台 - Agricultural Product Analysis Platform`
   - 选择 Public 或 Private
   - **不要勾选** "Initialize this repository with a README"
4. 点击 "Create repository"

### 2. 连接本地仓库到 GitHub

创建仓库后，GitHub 会显示仓库 URL，类似：
- HTTPS: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git`
- SSH: `git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git`

**在项目目录下执行以下命令（替换为你的实际 URL）：**

```bash
# 添加远程仓库（使用 HTTPS）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 或者使用 SSH（如果你配置了 SSH key）
# git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# 查看远程仓库配置
git remote -v

# 推送代码到 GitHub（首次推送）
git push -u origin master

# 如果 GitHub 默认分支是 main，使用：
# git branch -M main
# git push -u origin main
```

### 3. 如果遇到认证问题

#### 使用 HTTPS（推荐新手）：
- 如果提示输入用户名和密码，使用：
  - Username: 你的 GitHub 用户名
  - Password: 使用 **Personal Access Token**（不是密码）
  - 如何创建 Token：https://github.com/settings/tokens
  - 权限选择：`repo`（完整仓库权限）

#### 使用 SSH（推荐有经验用户）：
1. 生成 SSH key：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. 将公钥添加到 GitHub：
   - 复制 `~/.ssh/id_ed25519.pub` 的内容
   - GitHub → Settings → SSH and GPG keys → New SSH key
3. 使用 SSH URL 连接仓库

### 4. 后续更新代码

以后修改代码后，使用以下命令更新 GitHub：

```bash
# 查看修改的文件
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述你的修改内容"

# 推送到 GitHub
git push
```

## 常用 Git 命令

```bash
# 查看状态
git status

# 查看提交历史
git log

# 查看远程仓库
git remote -v

# 拉取最新代码
git pull

# 查看分支
git branch
```

## 注意事项

1. **不要提交敏感信息**：
   - 数据库密码
   - API 密钥
   - `.env` 文件（已在 .gitignore 中）

2. **.gitignore 已配置**：
   - 虚拟环境（.venv/）
   - 日志文件（logs/）
   - 数据库文件（db.sqlite3）
   - 静态文件（staticfiles/）
   - node_modules/

3. **如果推送失败**：
   - 检查网络连接
   - 确认 GitHub 仓库 URL 正确
   - 确认有推送权限
   - 检查认证信息是否正确


