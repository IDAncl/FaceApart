
import threading, unicodedata,time, re
from bs4 import BeautifulSoup
from flask import Flask, render_template_string
from playwright.sync_api import sync_playwright


app = Flask(__name__)
GROUPS_HISTORY = {}
LIVE_POSTS = [] 

# רשימת הקבוצות לניטור (הקבוצות שלך)
TARGET_GROUPS = [

    # האידיאל הוא לסדר את נתוני הפייסבוק לפי תאריך יציאה
    "https://www.facebook.com/groups/101875683484689/?sorting_setting=CHRONOLOGICAL",
    "https://www.facebook.com/groups/7298031916930520",
    "https://www.facebook.com/groups/458499457501175/?sorting_setting=CHRONOLOGICAL"
    "https://www.facebook.com/groups/5612809662118963?locale=he_IL"
    "https://www.facebook.com/groups/173289029523204/?sorting_setting=CHRONOLOGICAL&locale=he_IL"
    "https://www.facebook.com/groups/608325962573249/"
    "https://www.facebook.com/groups/333022240594651/"
]


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>חמ"ל דירות פייסבוק - LIVE</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; background: #f0f2f5; margin: 0; padding: 15px; color: #1c1e21; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { text-align: center; color: #1877f2; font-size: 24px; margin-bottom: 5px; }
        .subtitle { text-align: center; color: #65676b; font-size: 14px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 8px; }
        
        /* אינדיקטור LIVE מהבהב */
        .live-pulse { width: 8px; height: 8px; background-color: #2db742; border-radius: 50%; display: inline-block; box-shadow: 0 0 0 0 rgba(45, 183, 66, 0.7); animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(45, 183, 66, 0.7); } 70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(45, 183, 66, 0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(45, 183, 66, 0); } }
        
        .post-card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.2); margin-bottom: 15px; }
        .post-header { font-size: 12px; color: #65676b; margin-bottom: 10px; border-bottom: 1px solid #e4e6eb; padding-bottom: 5px; }
        .post-header a { color: #1877f2; text-decoration: none; font-weight: bold; }
        .post-content { font-size: 15px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; }
        .no-posts { text-align: center; color: #65676b; margin-top: 20px; font-style: italic; }
    </style>
    
    <!-- שינוי קצב הרענון האוטומטי ל-10 שניות בדיוק -->
    <meta http-equiv="refresh" content="10">
</head>
<body>
    <div class="container">
        <h1>חמ"ל דירות פייסבוק</h1>
        <div class="subtitle">
            <span class="live-pulse"></span>
            מתעדכן אוטומטית כל 10 שניות | סה"כ פוסטים: {{ posts|length }}
        </div>
        
        {% if not posts %}
            <div class="no-posts">ממתין לפוסטים חדשים שיעלו... הסורק מבצע סבב ראשוני.</div>
        {% endif %}

        {% for post in posts %}
            <div class="post-card">
                <div class="post-header">
                    קבוצה: <a href="{{ post.url }}" target="_blank">לינק למקור</a> | נסרק ב- {{ post.time }}
                </div>
                <div class="post-content">{{ post.text }}</div>
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, posts=list(reversed(LIVE_POSTS)))

def parse_and_print_posts(html, group_url):
    global GROUPS_HISTORY, LIVE_POSTS
    LTR_MARK = unicodedata.lookup('LEFT-TO-RIGHT EMBEDDING')
    RESET_MARK = unicodedata.lookup('POP DIRECTIONAL FORMATTING')
    
    if group_url not in GROUPS_HISTORY:
        GROUPS_HISTORY[group_url] = set()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    articles = soup.find_all('div', role='article')
    feed_stories = soup.find_all('div', attrs={"data-ad-preview": "feed_story"})
    all_raw_posts = articles + feed_stories
    
    new_posts_count = 0
    
    for post in all_raw_posts:
        post_text = post.get_text(separator=' | ', strip=True)
        
        keywords = ["דיר", "שותף", "חדר", "שכ\"ד", "השכרה", "חוזה", "מחיר", "שח", "₪", "סאבלט"]
        if not any(word in post_text for word in keywords):
            continue
            
        if len(post_text) < 70 or "הגיב/ה" in post_text or "צפייה בתגובה" in post_text:
            continue
            
        clean_id_text = re.sub(r'\|\s*(לפני|‏)\s*\d*\s*(דקות|שעות|ימים|שניות|יום)\s*\|', '|', post_text)
        unique_id = clean_id_text[40:180] 
        
        if len(unique_id) < 50:
            unique_id = clean_id_text
            
        if unique_id not in GROUPS_HISTORY[group_url]:
            GROUPS_HISTORY[group_url].add(unique_id)
            new_posts_count += 1
            
            # הדפסה לטרמינל (לגיבוי)
            print(f"\n{LTR_MARK}🚨 [פוסט חדש זוהה בקבוצה!] 🚨{RESET_MARK}")
            print(f"{LTR_MARK}לינק לקבוצה: {group_url}{RESET_MARK}")
            print(f"{LTR_MARK}{post_text}{RESET_MARK}")
            print("-" * 60)
            
            LIVE_POSTS.append({
                "url": group_url,
                "text": post_text,
                "time": time.strftime('%H:%M:%S')
            })
            
    return new_posts_count

def scan_single_group(page, url):
    print(f"Scanning: {url}")
    try:
        page.goto(url)
        page.wait_for_timeout(5000)
        
        total_new_found = 0
        
        for scroll_round in range(3):
            try:
                buttons = page.locator('div[role="button"]:has-text("עוד"), div[role="button"]:has-text("See more")')
                count = buttons.count()
                for i in range(count):
                    try:
                        btn = buttons.nth(i)
                        btn.scroll_into_view_if_needed(timeout=1000)
                        page.wait_for_timeout(200)
                        btn.dispatch_event("click")
                        btn.click(timeout=500, force=True)
                    except Exception:
                        continue
                page.wait_for_timeout(1500)
            except Exception:
                pass
            
            current_html = page.content()
            total_new_found += parse_and_print_posts(current_html, url)
            
            page.evaluate("window.scrollBy(0, window.innerHeight * 1.3);")
            page.wait_for_timeout(2000)
            
        return total_new_found
    except Exception as e:
        print(f"Error scanning group {url}: {e}")
        return 0

# הלולאה של הבוט  
def run_bot_loop():
    print("Facebook Multi-Group Monitor Started in background...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("\n--- Performing initial baseline scan for all groups ---")
        for url in TARGET_GROUPS:
            scan_single_group(page, url)
        print("\n✅ Baseline setup complete. History saved. Live monitoring is active.")
        
        while True:
            print(f"\n⏰ Starting new scan cycle at {time.strftime('%H:%M:%S')}...")
            
            for url in TARGET_GROUPS:
                new_found = scan_single_group(page, url)
                if new_found > 0:
                    print(f" Found {new_found} new posts in this group.")
                else:
                    print(" No new updates here.")
                    
            print("Cycle finished. Sleeping for  minutes...")
            time.sleep(100)
            
        browser.close()

if __name__ == "__main__":
    # 1. הפעלת הבוט בתוך ת'רד נפרד (Thread) כדי שלא יתקע את הדפדפן
    bot_thread = threading.Thread(target=run_bot_loop, daemon=True)
    bot_thread.start()
    
    # 2. הפעלת השרת על פורט 5000 ופתיחתו לכל הרשת (host='0.0.0.0') לצורך ה-Port Forward
    app.run(host='0.0.0.0', port=5000, debug=False)