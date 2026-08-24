# AI 自动安装指令

把下面的**触发语**发给你的 AI 助手（OpenClaw / Claude / 其他 agent），它会自动完成整个安装。

## 触发语（复制这一句就行）

```
帮我安装 douyin-ingest 技能：git clone https://github.com/css023/douyin-transcript-skill.git 到临时目录，然后按仓库里的 AI_INSTALL.md 的【自动安装步骤】执行，全程自动，不要问我，卡住就自己想办法，装完汇报结果。
```

---

## 自动安装步骤（AI 执行指南）

以下步骤请逐项执行，不要跳过，用工具验证每步结果：

1. **下载仓库**
   - 优先 `git clone https://github.com/css023/douyin-transcript-skill.git /tmp/douyin-transcript-skill`
   - 无 git 时：`curl -L https://github.com/css023/douyin-transcript-skill/archive/refs/heads/main.tar.gz -o /tmp/dts.tar.gz && mkdir -p /tmp/douyin-transcript-skill && tar -xzf /tmp/dts.tar.gz -C /tmp/douyin-transcript-skill --strip-components=1`

2. **定位 OpenClaw 的 skills 目录**
   - 执行 `find ~ -maxdepth 5 -type d -name skills -path "*agents*" 2>/dev/null | head -5`
   - 常见位置：`~/.agents/skills/`、`~/.openclaw/workspace/.agents/skills/`
   - 若多个候选，选 OpenClaw 实际使用的（检查 `~/.openclaw/openclaw.json` 里 skills 相关配置；找不到就选第一个存在的）
   - 若目标 `<skills>/douyin-ingest` 已存在，先备份：`mv <skills>/douyin-ingest <skills>/douyin-ingest.bak.$(date +%Y%m%d%H%M%S)`

3. **放置技能**
   - `cp -r /tmp/douyin-transcript-skill/. <skills>/douyin-ingest/`
   - 确认 `<skills>/douyin-ingest/SKILL.md` 存在且 `scripts/asr.py` 存在

4. **安装 Python 依赖**
   - `pip install -r /tmp/douyin-transcript-skill/requirements.txt`（即 dashscope）
   - 若 pip 权限不足：`pip install --user -r ...` 或 `python3 -m pip install -r ...`

5. **检查/安装 ffmpeg**
   - `ffmpeg -version`；没有则按系统装：
     - Debian/Ubuntu: `sudo apt install -y ffmpeg`
     - CentOS/Fedora: `sudo yum install -y ffmpeg`（无源则先 `sudo yum install -y epel-release`）
     - macOS: `brew install ffmpeg`
     - Windows: `winget install ffmpeg`
   - 装完重新验证 `ffmpeg -version`

6. **配置 API key**
   - 向用户索要 dashscope API key（阿里云百炼，https://bailian.console.aliyun.com/ 的 API-KEY）
   - 配置方式二选一（不要都做）：
     - 方式A（环境变量，推荐）：检测 shell 是 bash 还是 zsh，追加 `export DASHSCOPE_API_KEY='<key>'` 到 `~/.bashrc` 或 `~/.zshrc`，然后 `source` 之
     - 方式B（config.env）：`cp /tmp/douyin-transcript-skill/config.env.example <skills>/douyin-ingest/config.env` 并填入真实 key
   - ⚠️ 如果 `config.env` 已存在且为空/模板，直接填；确保 key 前后无空格引号

7. **验证（全部必须通过）**
   - [ ] `<skills>/douyin-ingest/SKILL.md` 存在
   - [ ] `python3 -c "import dashscope; print('dashscope OK')"` 输出 OK
   - [ ] `ffmpeg -version | head -1` 有输出
   - [ ] key 已配置：`echo $DASHSCOPE_API_KEY | cut -c1-6` 有输出（**不要完整打印 key**）

8. **汇报**
   - 列出每步验证结果
   - 提示用户：重启 OpenClaw 让技能加载，然后发一条抖音链接（如 `https://v.douyin.com/xxxxx/`）测试

## 约束
- 不要删除/覆盖用户现有文件（同名先备份）
- 不要执行与安装无关的命令
- 任何时候不要完整输出 API key
- 卡住时自己排查（查报错、装依赖、换方式），不要中途停下来问用户
