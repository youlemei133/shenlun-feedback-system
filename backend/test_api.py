import requests
import json

response = requests.get('http://127.0.0.1:5000/api/question/1')
data = response.json()

print("=== API 返回数据结构 ===")
print(f"review_a 存在：{data.get('review_a') is not None}")

if data.get('review_a'):
    review_a = data['review_a']
    print(f"\nreview_a 类型：{type(review_a)}")
    print(f"\n字段列表：{list(review_a.keys())}")
    print(f"\n详细数据:")
    print(json.dumps(review_a, indent=2, ensure_ascii=False))
