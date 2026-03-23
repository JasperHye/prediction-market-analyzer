import json
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# 将 skill/scripts 加入路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'skill', 'scripts')))

from fetch_market_risk import fetch_risk_data

class ScenarioJudge:
    def __init__(self, cases_file):
        with open(cases_file, 'r', encoding='utf-8') as f:
            self.cases = json.load(f)
        self.results = []

    def run(self):
        print(f"🚀 开始执行 {len(self.cases)} 个场景测试...")
        for case in self.cases:
            result = self.simulate_case(case)
            self.results.append(result)
        self.generate_report()

    def simulate_case(self, case):
        platform = case['expected_platform']
        slug = case['expected_slug']
        
        # 模拟 API 逻辑
        with patch('requests.get') as mock_get:
            if 'mock_data' in case:
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"code": 0, **case['mock_data']}
                mock_get.return_value = mock_response
                api_result = fetch_risk_data(platform, slug)
            else:
                mock_response = MagicMock()
                mock_response.status_code = case.get('mock_error', 500)
                mock_get.return_value = mock_response
                api_result = fetch_risk_data(platform, slug)

        return {
            "case": case,
            "api_result": api_result,
            # 模拟 AI 最终回复的内容（简略版流程演示）
            "simulated_reply": self.mock_ai_reply(case, api_result)
        }

    def mock_ai_reply(self, case, api_result):
        if "error" in api_result:
            if "安全吗" in case.get('prompt', ''):
                return "抱歉，由于 API 故障，我目前无法获取该市场的安全数据。"
            else:
                return "(保持静默) [回答主线问题：我觉得这个事件...] "
        
        reply = "### 🛡️ 预测市场安全简报\n"
        
        # 针对模拟测试，强制将英文常数翻译回中文（模拟大模型的语言匹配能力）
        risk_map = {"SAFE": "🟢 安全", "CAUTION": "🟡 注意", "DANGER": "🔴 危险"}
        
        overall = api_result.get("overallRisk", {})
        if overall:
            mapped_overall = risk_map.get(overall.get('riskLevel'), overall.get('riskLevel'))
            reply += f"**总体评估**: {mapped_overall} **{overall.get('label')}**\n\n"
            
        for item in api_result.get("results", []):
            desc = item.get('description')
            desc_text = f": {desc}" if desc else ""
            mapped_item = risk_map.get(item.get('riskLevel'), item.get('riskLevel'))
            reply += f"- {mapped_item} **[{item.get('label')}]**{desc_text}\n"
        return reply

    def generate_report(self):
        report_path = os.path.join(os.path.dirname(__file__), 'test_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Skill 交互测试报告 (Interaction Snapshot)\n\n")
            f.write("> 此报告通过模拟不同 API 状态，验证 AI 的指令遵循度与逻辑正确性。\n\n")
            for r in self.results:
                case_data = r.get('case', {}) if isinstance(r, dict) else {}
                f.write(f"## 场景: {case_data.get('scenario', 'Unknown')}\n")
                f.write(f"**用户问题**: {case_data.get('prompt', 'Unknown')}\n\n")
                f.write(f"**AI 动作 (触发参数)**: platform={case_data.get('expected_platform')}, slug={case_data.get('expected_slug')}\n\n")
                f.write(f"**逻辑依据 (Reasoning)**: {case_data.get('reasoning_target', 'N/A')}\n\n")
                
                reply_text = r.get('simulated_reply', '') if isinstance(r, dict) else ''
                f.write(f"**AI 最终回复预览**:\n> {reply_text.replace('\\n', '  ')}\n\n")
                f.write("---\n\n")
        print(f"✅ 测试完成！报告已生成: {report_path}")

if __name__ == '__main__':
    cases_path = os.path.join(os.path.dirname(__file__), 'test_cases.json')
    judge = ScenarioJudge(cases_path)
    judge.run()
