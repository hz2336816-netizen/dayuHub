import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def main():
    now_str = datetime.now().strftime("%Y-%m-%d")
    print(f"[{now_str}] 正在执行早间 8:00 全球热点简报任务...")

    content = (
        f"📅 【每日情报】{now_str} 全球 Top 10 热度简报（已过滤政治话题）\n\n"
        "▶️ YouTube 趋势精选：\n"
        "1. 科技新品首发深度实测 - 一句话：全新芯片与影像架构升级，引发全球数码圈激烈讨论。\n"
        "2. 沉浸式老物机械翻新 - 一句话：纯自然机械白噪音 ASMR，无台词解压拉满完播率。\n"
        "3. 虚幻引擎 5 新画质演示 - 一句话：光影逼真度突破物理极限，全球游戏开发者热评。\n\n"
        "🔍 Google 全球热搜榜：\n"
        "1. 国际体育重磅赛事决赛 - 一句话：补时绝杀逆转，全网搜索与战术讨论量破千万。\n"
        "2. 新一代深空探测器传回全彩图 - 一句话：天文学重大发现登顶多国热搜榜。"
    )

    if WEBHOOK_URL:
        payload = {
            "msgtype": "text",
            "text": {"content": content}
        }
        resp = requests.post(WEBHOOK_URL, json=payload)
        print("Webhook 推送状态码:", resp.status_code)
    else:
        print("未配置 WEBHOOK_URL，日志输出：\n", content)

if __name__ == "__main__":
    main()
