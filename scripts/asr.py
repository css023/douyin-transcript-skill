#!/usr/bin/env python3
"""
独立版 ASR 脚本：dashscope qwen3-asr-flash 语音转文字
不依赖任何 douyin-mcp 旧包，只需 dashscope SDK。

用法：
    python3 asr.py /path/to/audio.wav
    python3 asr.py /path/to/audio.wav --language zh

key 读取顺序：--api-key 参数 > 环境变量 DASHSCOPE_API_KEY > 同目录 config.env
"""
import os
import sys
import argparse

try:
    import dashscope
except ImportError:
    sys.exit("缺少依赖：请先运行 pip install dashscope")


def load_key_from_config_env(config_path=None):
    """从 config.env 读取 DASHSCOPE_API_KEY"""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.env")
    if not os.path.exists(config_path):
        return None
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("DASHSCOPE_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def recognize(audio_path, api_key=None, model="qwen3-asr-flash", language="zh"):
    """识别音频文件，返回文字"""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    key = api_key or os.getenv("DASHSCOPE_API_KEY") or load_key_from_config_env()
    if not key:
        raise SystemExit(
            "未找到 API key。请设置环境变量 DASHSCOPE_API_KEY，"
            "或创建 config.env（参考 config.env.example），或用 --api-key 传入"
        )

    dashscope.api_key = key
    audio_input = f"file://{os.path.abspath(audio_path)}"

    messages = [
        {"role": "system", "content": [{"text": ""}]},
        {"role": "user", "content": [{"audio": audio_input}]},
    ]
    asr_options = {"enable_lid": True, "enable_itn": False}
    if language:
        asr_options["language"] = language

    response = dashscope.MultiModalConversation.call(
        model=model,
        messages=messages,
        result_format="message",
        asr_options=asr_options,
    )

    if response.status_code != 200:
        raise RuntimeError(f"API 调用失败: {response.message}")

    text = ""
    if response.output and response.output.choices:
        choice = response.output.choices[0]
        if choice.message and choice.message.content:
            text = choice.message.content[0].get("text", "")
    return text


def main():
    parser = argparse.ArgumentParser(description="dashscope qwen3-asr-flash 语音转文字")
    parser.add_argument("audio", help="音频文件路径（wav/mp3/m4a 等）")
    parser.add_argument("--api-key", help="dashscope API key（默认读环境变量或 config.env）")
    parser.add_argument("--language", default="zh", help="语言，默认 zh")
    args = parser.parse_args()

    text = recognize(args.audio, args.api_key, language=args.language)
    print(text)


if __name__ == "__main__":
    main()
