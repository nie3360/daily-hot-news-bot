import json
import os

CATEGORIES = {
    "运动健身": ["运动", "健身", "跑步", "瑜伽", "减肥", "减脂", "增肌", "马拉松",
               "游泳", "跳绳", "深蹲", "拉伸", "体测", "体能", "肌肉", "有氧"],
    "健康养生": ["健康", "猝死", "失眠", "腰椎", "颈椎", "焦虑", "抑郁", "体检",
               "血压", "血糖", "肥胖", "过敏", "近视", "脱发", "皮肤", "久坐",
               "腰痛", "背痛", "肩周炎", "关节炎", "血栓", "心脏"],
    "生活方式": ["加班", "996", "打工人", "离职", "内卷", "躺平", "考研", "考公",
               "通勤", "熬夜", "外卖", "奶茶", "咖啡", "游戏", "电竞", "手机",
               "屏幕时间", "居家", "带娃", "亲子", "驾驶", "自驾"],
    "饮食营养": ["奶茶", "外卖", "轻食", "蛋白粉", "碳水", "代餐", "维生素",
               "咖啡因", "能量饮料", "减脂餐", "断食", "糖"]
}

def filter_topics():
    input_path = "hot_topics.json"
    if not os.path.exists(input_path):
        print("未找到 hot_topics.json，请先运行 fetch_hot_topics.py")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    topics = data.get("topics", [])
    filtered = []

    for topic in topics:
        title = topic.get("title", "")
        excerpt = topic.get("excerpt", "")
        text = title + " " + excerpt

        matched_keywords = []
        matched_categories = []

        for category, keywords in CATEGORIES.items():
            for kw in keywords:
                if kw in text:
                    matched_keywords.append(kw)
                    if category not in matched_categories:
                        matched_categories.append(category)

        if matched_keywords:
            filtered.append({
                "title": title,
                "source": topic.get("source", ""),
                "hot_value": topic.get("hot_value", ""),
                "url": topic.get("url", ""),
                "matched_keywords": list(set(matched_keywords)),
                "matched_categories": matched_categories,
                "suggested_column": suggest_column(matched_categories)
            })

    output = {
        "filter_time": data.get("fetch_time", ""),
        "total_scanned": len(topics),
        "total_matched": len(filtered),
        "topics": filtered
    }

    with open("filtered_topics.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"扫描 {len(topics)} 条，筛选出 {len(filtered)} 条相关话题")
    for item in filtered:
        print(f"  [{item['source']}] {item['title']} -> {item['suggested_column']}")

def suggest_column(categories):
    if "运动健身" in categories:
        return "微动5分钟"
    if "健康养生" in categories:
        return "身体求救信号"
    if "生活方式" in categories:
        return "热点×微动"
    if "饮食营养" in categories:
        return "热点×微动"
    return "热点×微动"

if __name__ == "__main__":
    filter_topics()
