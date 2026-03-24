import sys
import json
import time

try:
    import requests
except ImportError:
    # 引导 Agent 自动修复依赖
    print(json.dumps({
        "error": "The 'requests' library is not installed.",
        "hint": "Please run 'pip install requests' in your environment."
    }))
    sys.exit(1)

BASE_URL = "https://api.secwarex.io"

def fetch_risk_data(platform, slug, retries=3):
    # 参数名高度敏感处理
    if platform == "polymarket":
        url = f"{BASE_URL}/api/v1/plugin/polymarket/risk?slug={slug}"
    elif platform == "kalshi":
        # Kalshi 必须使用 eventTicker (注意驼峰)
        url = f"{BASE_URL}/api/v1/plugin/kalshi/risk?eventTicker={slug}"
    else:
        return {"error": f"Unsupported platform: {platform}"}

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for attempt in range(1, retries + 1):
        try:
            print(f"DEBUG: Attempt {attempt} - GET {url}")
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"DEBUG: RAW RESPONSE: {data}")
                
                # 根据实际抓取到的结构，关键数据在 'result' 字段中
                # 且 code 可能为 1 表示成功（message 为 'ok'）
                if data and 'result' in data and data.get('result'):
                    return parse_tags(data.get("result"))
                
                # fallback
                if data and data.get("code") == 0 and 'data' in data:
                    return parse_tags(data.get("data"))
                else:
                    msg = data.get('message') or data.get('msg') or 'Unknown error'
                    print(f"DEBUG: API returned code {data.get('code')}: {msg}")
            else:
                print(f"DEBUG: HTTP status {response.status_code} on attempt {attempt}")
        except Exception as e:
            print(f"DEBUG: Exception on attempt {attempt}: {str(e)}")
        
        if attempt < retries:
            time.sleep(2)
            
    return {"error": f"Failed after {retries} attempts."}

def parse_tags(data):
    if not data:
        return {"error": "No data found to parse"}
    
    def map_risk(level):
        if level == 1:
            return "SAFE"
        elif level == 2:
            return "CAUTION"
        elif level == 3:
            return "DANGER"
        return "UNKNOWN"

    parsed_results = []
    
    # 提取总评并映射风险等级
    overall = data.get('overallRisk', {})
    overall_mapped = {
        "label": overall.get("label", "Unknown"),
        "riskLevel": map_risk(overall.get("riskLevel"))
    }
    
    # 解析 tags 数组
    for tag in data.get('tags', []):
        parsed_results.append({
            "type": "tag",
            "item": tag.get("name"),
            "label": tag.get("label", tag.get("name")),
            "riskLevel": map_risk(tag.get("riskLevel")),
            "description": tag.get("description")
        })
    
    # 解析 notices 数组 (如有)
    for notice in data.get('notices', []):
        parsed_results.append({
            "type": "notice",
            "item": notice.get("name"),
            "label": notice.get("label", notice.get("name")),
            "riskLevel": map_risk(notice.get("riskLevel")),
            "description": notice.get("description")
        })
        
    return {
        "overallRisk": overall_mapped,
        "results": parsed_results
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: [platform] [slug]"}))
        sys.exit(1)
        
    platform = sys.argv[1].lower()
    slug = sys.argv[2]
    
    result = fetch_risk_data(platform, slug)
    print(json.dumps(result, ensure_ascii=False))
