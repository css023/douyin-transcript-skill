# Douyin Transcript Skill（抖音视频文案提取·通用版）

把抖音视频完整口播文案提取为文字。支持完整链接和短链（v.douyin.com）。

## 包内容

```
douyin-transcript-skill/
├── SKILL.md              # 技能文档（OpenClaw 读取）
├── scripts/
│   └── asr.py            # 独立 ASR 脚本（dashscope qwen3-asr-flash）
├── config.env.example    # API key 配置模板
├── requirements.txt      # Python 依赖
└── README.md             # 本说明
```

## 安装步骤（新电脑）

1. **放技能**：把整个目录放到 OpenClaw 的 skills 目录：
   ```bash
   mkdir -p ~/.agents/skills
   cp -r douyin-transcript-skill ~/.agents/skills/douyin-ingest
   ```
   （如果目标机器的 OpenClaw skills 目录路径不同，以实际为准）

2. **装 Python 依赖**：
   ```bash
   pip install -r ~/.agents/skills/douyin-ingest/requirements.txt
   ```

3. **装 ffmpeg**（用于音频转换）：
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   # macOS
   brew install ffmpeg
   ```

4. **配置 API key**（阿里云百炼 qwen3-asr-flash）：
   ```bash
   # 方式一：环境变量
   echo 'export DASHSCOPE_API_KEY=sk-你的key' >> ~/.bashrc && source ~/.bashrc
   # 方式二：复制模板填 key
   cp ~/.agents/skills/douyin-ingest/config.env.example ~/.agents/skills/douyin-ingest/config.env
   # 然后编辑 config.env 填入真实 key
   ```
   key 获取：https://bailian.console.aliyun.com/ → API-KEY 管理

5. **验证**：在 OpenClaw 里发一条抖音链接，技能自动触发。

## 使用

直接给 OpenClaw 发抖音链接即可：
- `https://www.douyin.com/video/xxxxx`
- `https://v.douyin.com/xxxxx/`（短链）
- 抖音 APP 分享文本（含"复制打开抖音"）

结果输出：标题 + 作者/时长/标签 + 完整口播文案。

## 注意事项
- 视频播放地址有时效（几分钟），抓到立即下载
- 部分视频音视频分离，技能会自动处理
- ASR 为阿里云按量计费服务，key 请妥善保管
