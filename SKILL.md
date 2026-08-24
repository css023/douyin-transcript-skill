---
name: douyin-ingest
description: 抖音链接转文案（视频口播提取）。收到 v.douyin.com/douyin.com 链接或抖音分享文本时触发。流程：浏览器打开→抓播放地址→curl下载→ffmpeg提音频→dashscope ASR转写。
---

# Douyin 视频文案提取 Skill（通用版）

收到抖音链接/分享文本时，提取视频完整口播文案。

## 环境要求
- OpenClaw 浏览器工具可用（可正常访问 douyin.com）
- 系统已装：`curl`、`ffmpeg`
- Python 依赖：`dashscope`（`pip install dashscope`）
- 已配置 dashscope API key（环境变量 `DASHSCOPE_API_KEY` 或 `config.env`）

## 标准流程

### 第一步：打开视频页
```text
browser open <链接> label=douyin
```
短链 `v.douyin.com/xxx/` 会自动重定向到完整视频页。等 5-6 秒让视频开始加载。

### 第二步：抓播放地址
对视频 tab evaluate：
```js
() => { const v = document.querySelector('video'); return JSON.stringify({url: location.href, title: document.title, videoSrc: v ? (v.currentSrc || v.src) : null, readyState: v ? v.readyState : null}); }
```
- 拿到 `videoSrc`（douyinvod.com 带签名 URL）→ **立即下载**，签名几分钟后失效
- videoSrc 为 null 或 readyState<4 → 等 3 秒重试一次
- 记录 `title`（含作者和话题标签）、`url`（真实视频 ID）

### 第三步：下载视频
```bash
curl -sL -o /tmp/dy_video.mp4 \
  -H "Referer: https://www.douyin.com/" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36" \
  "<videoSrc>"
ffprobe -v error -show_streams /tmp/dy_video.mp4 | grep -E "codec_type|codec_name|duration"
```
- 有 audio 流 → 直接进第四步
- **只有 video 流（音视频分离）** → 从页面 performance API 找独立音频 URL 单独下载：
  ```js
  () => performance.getEntriesByType('resource').map(r => r.name).filter(n => /media-audio|und-mp4a/i.test(n))
  ```

### 第四步：转 wav（16kHz 单声道）
```bash
ffmpeg -y -i /tmp/dy_video.mp4 -acodec pcm_s16le -ar 16000 -ac 1 /tmp/dy_audio.wav
```

### 第五步：ASR 转写
```bash
python3 scripts/asr.py /tmp/dy_audio.wav
```
（脚本会自动读环境变量或 config.env 里的 key；也可 `--api-key` 显式传入）

### 第六步：输出
- **模式A（直接发）**：RJ 说"结果不用存/直接发" → 整理成「标题 + 作者/时长/标签 + 完整口播文案」直接发送，不存知识库
- **模式B（存入知识库）**：按本机知识库规则存储（原文+笔记双存、更新 INDEX/log）

## 平台级注意事项（与运行环境无关）
1. **播放地址有时效**：douyinvod 签名 URL 几分钟失效，抓到立即下载；失效需重新打开页面抓
2. **音视频可能分离**：网页版有时 video URL 无音频流，需单独下载 media-audio URL（见第三步）
3. **抖音无感验证**：页面可能加载验证 iframe，不影响主页面渲染，忽略即可

## 存储流程（模式B，仅在本机知识库使用）
按本机 `workspace/wiki` 规则：选题建子文件夹（原文+笔记双存）、更新 INDEX.md、写 log.md。存放位置判断：
| 内容类型 | 存放 |
|---------|------|
| 视频文案/脚本 | 01-选题库 |
| 素材/故事/案例 | 02-素材库 |
| 行业知识 | 03-行业知识 |
| 客户实战故事 | 04-客户案例 |
| 模板/框架/公式 | 05-内容框架 |
| 思考/反思 | 06-个人成长 |
| 专项学习 | 07-学习系列 |
| 临时中转 | 00-收件箱 |
