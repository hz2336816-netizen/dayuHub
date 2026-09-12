import os
import smtplib
import xml.etree.ElementTree as ET
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
import requests

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

# 敏感词简易过滤列表
BLOCKED_KEYWORDS = ["中共", "习近平", "六四", "政治局", "台海战争", "统战"]

def is_safe(text):
    for kw in BLOCKED_KEYWORDS:
        if kw in text:
            return False
    return True

def fetch_google_trends():
    """抓取 Google 实时热搜榜"""
    url = "https://trends.google.com/trending/rss?geo=US"
    headers = {"User-Agent": "Mozilla/5.0"}
    items = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(resp.content)
        for item in root.findall(".//item"):
            title = item.find("title").text if item.find("title") is not None else ""
            approx_traffic = item.find("{https://trends.google.com/trending/rss}approx_traffic")
            traffic = approx_traffic.text if approx_traffic is not None else "热度飙升"
            if title and is_safe(title):
                items.append(f"<b>{title}</b> <span style='color:gray;'>({traffic} 次搜索)</span>")
            if len(items) >= 10:
                break
    except Exception as e:
        items.append(f"获取 Google Trends 失败: {e}")
    return items

def fetch_youtube_trending():
    """抓取 YouTube 全球热门视频"""
    # 抓取全球热门频道/分类的公开更新源
    url = "https://www.youtube.com/feeds/videos.xml?chart=mostpopular"
    headers = {"User-Agent": "Mozilla/5.0"}
    items = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(resp.content)
        # XML 命名空间处理
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text if entry.find("atom:title", ns) is not None else ""
            link = entry.find("atom:link", ns).attrib.get("href", "") if entry.find("atom:link", ns) is not None else ""
            if title and is_safe(title):
                items.append(f"<a href='{link}' style='text-decoration:none; color:#1a0dab;'><b>{title}</b></a>")
            if len(items) >= 10:
                break
    except Exception as e:
        # 备用方案：抓取前沿科技/爆款精选
        items.append(f"获取 YouTube 实时源异常: {e}")
    return items

def send_email(subject, content):
    if not GMAIL_USER or not GMAIL_PASS:
        print("未检测到密钥配置！")
        return

    user = GMAIL_USER.strip()
    pwd = GMAIL_PASS.strip().replace(" ", "")

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = f"TrendBot <{user}>"
    message['To'] = user
    message['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(user, pwd)
        server.sendmail(user, [user], message.as_string())
        server.quit()
        print("最新实时简报已成功发送！")
    except Exception as e:
        print(f"邮件发送失败: {e}")

def main():
    now_str = datetime.now().strftime("%Y-%m-%d")
    subject = f"🔥 全球实时爆款与热搜 Top 10 ({now_str})"

    print("正在抓取实时数据...")
    yt_list = fetch_youtube_trending()
    gt_list = fetch_google_trends()

    yt_html = "".join([f"<li style='margin-bottom:8px;'>{item}</li>" for item in yt_list])
    gt_html = "".join([f"<li style='margin-bottom:8px;'>{item}</li>" for item in gt_list])

    html_content = f"""
    <div style="max-width: 600px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6;">
        <h2 style="color: #202124; border-bottom: 2px solid #ea4335; padding-bottom: 8px;">🌍 全球实时爆款情报 Top 10 ({now_str})</h2>
        <p style="color: #5f6368; font-size: 13px;">自动过滤政治敏感话题 | 每日早上 08:00 定时推送</p>
        
        <h3 style="color: #c4302b; margin-top: 24px;">▶️ YouTube 全球热门视频</h3>
        <ol style="padding-left: 20px;">
            {yt_html}
        </ol>

        <h3 style="color: #1a73e8; margin-top: 24px;">🔍 Google 全球热搜飙升榜</h3>
        <ol style="padding-left: 20px;">
            {gt_html}
        </ol>
        <hr style="border: none; border-top: 1px solid #dadce0; margin-top: 30px;">
        <p style="color: #9aa0a6; font-size: 12px; text-align: center;">由 GitHub Actions 自动化引擎提供驱动</p>
    </div>
    """

    print("开始发送邮件...")
    send_email(subject, html_content)

if __name__ == "__main__":
    main()

