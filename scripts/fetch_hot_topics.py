import json
import requests
from datetime import datetime

def fetch_weibo_hot():
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", {}).get("realtime", [])
        results = []
        for item in items[:10]:
            results.append({
                "source": "weibo",
                "title": item.get("word", ""),
                "hot_value": item.get("num", 0),
                "url": f"https://s.weibo.com/weibo?q=%23{item.get('word', '')}%23"
            })
        return results
    except Exception as e:
        print(f"[Weibo] 抓取失败: {e}")
        return []

def fetch_zhihu_hot():
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", [])
        results = []
        for item in items[:5]:
            target = item.get("target", {})
            results.append({
                "source": "zhihu",
                "title": target.get("title", ""),
                "hot_value": item.get("detail_text", ""),
                "excerpt": target.get("excerpt", ""),
                "url": f"https://www.zhihu.com/question/{target.get('id', '')}"
            })
        return results
    except Exception as e:
        print(f"[Zhihu] 抓取失败: {e}")
        return []

if __name__ == "__main__":
    all_topics = []
    all_topics.extend(fetch_weibo_hot())
    all_topics.extend(fetch_zhihu_hot())

    output = {
        "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(all_topics),
        "topics": all_topics
    }

    with open("hot_topics.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"共抓取 {len(all_topics)} 条热搜，已保存到 hot_topics.json")
