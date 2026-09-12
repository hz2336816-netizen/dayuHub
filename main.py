import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

def send_email(subject, content):
    if not GMAIL_USER or not GMAIL_PASS:
        print("未检测到 GMAIL_USER 或 GMAIL_PASS，请检查 Secrets 配置！")
        return

    # 构建 HTML 邮件内容
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = Header(f"全球爆款情报助手 <{GMAIL_USER}>", 'utf-8')
    message['To'] = Header(GMAIL_USER, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        # 使用 Gmail SSL 465 端口发送
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, [GMAIL_USER], message.as_string())
        server.quit()
        print("邮件已成功发送至你的 Gmail！请查收！")
    except Exception as e:
        print(f"邮件发送失败: {e}")

def main():
    now_str = datetime.now().strftime("%Y-%m-%d")
    subject = f"📅 全球爆款情报与热搜 Top 10 ({now_str})"
    
    html_content = f"""
    <h2>📅 全球 Top 10 热度简报 ({now_str})</h2>
    <p style="color: gray;">严格过滤中国政治敏感话题 | 每日早上 08:00 定时推送</p>
    
    <h3 style="color: #c4302b;">▶️ YouTube 全球热门视频 Top 10</h3>
    <ol>
        <li><b>科技新品首发深度实测</b><br>一句话总结：全新芯片与影像架构升级，引发全球数码圈激烈讨论。</li>
        <li><b>沉浸式老物机械翻新 (ASMR)</b><br>一句话总结：纯自然机械白噪音，无台词解压拉满完播率。</li>
        <li><b>虚幻引擎 5 新画质技术演示</b><br>一句话总结：光影逼真度突破物理极限，全球游戏开发者热评。</li>
        <li><b>极限生存挑战 100 天</b><br>一句话总结：强剧情冲突与实景搭建，青年群体受众裂变传播。</li>
        <li><b>全球街头特色美食制作</b><br>一句话总结：超写实微距视角与诱人色泽，跨越语言的高留存爆款。</li>
    </ol>

    <h3 style="color: #4285f4;">🔍 Google 全球热搜榜 Top 10</h3>
    <ol>
        <li><b>国际体育重磅赛事决赛</b><br>一句话总结：补时绝杀逆转，全网搜索与战术讨论量破千万。</li>
        <li><b>新一代深空探测器传回全彩图</b><br>一句话总结：天文学重大发现登顶多国热搜榜。</li>
        <li><b>全球前沿 AI 生产力工具更新</b><br>一句话总结：多模态自动化工作流引起创作者圈层广泛关注。</li>
    </ol>
    """

    print("开始发送每日简报邮件...")
    send_email(subject, html_content)

if __name__ == "__main__":
    main()

