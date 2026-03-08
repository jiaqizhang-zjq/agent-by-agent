import os
import json
import logging
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from src.utils.llm_client import llm_client

load_dotenv()

logger = logging.getLogger(__name__)

class FortuneAnalyzer:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
    
    def analyze(self, user_info, question):
        birth_date = user_info.get("birth_date", "未知")
        birth_time = user_info.get("birth_time", "未知")
        gender = user_info.get("gender", "未知")
        skill_result = user_info.get("skill_result")
        
        prompt = self._build_prompt(birth_date, birth_time, gender, question, skill_result)
        llm_result = self._call_llm(prompt)
        
        return {
            "bazi": skill_result.get("bazi", {}).get("full_chart", "未知") if skill_result else "未知",
            "wuxing": skill_result.get("wuxing", {}).get("analysis", "") if skill_result else "",
            "personality": llm_result.get("personality", "根据八字分析，您的性格独特而鲜明。"),
            "fortune": llm_result.get("fortune", "近期运势平稳，需保持积极心态。"),
            "specific": llm_result.get("specific", self._default_answer(question, gender)),
            "reasoning": llm_result.get("reasoning", f"根据您提供的信息：出生日期{birth_date}，出生时间{birth_time}，性别{gender}，我进行了详细的命理分析。")
        }
    
    def _build_prompt(self, birth_date, birth_time, gender, question, skill_result):
        skill_info = ""
        if skill_result:
            bazi = skill_result.get("bazi", {})
            wuxing = skill_result.get("wuxing", {})
            personality = skill_result.get("personality", "")
            
            skill_info = f"""
已计算的命理信息：
- 八字：{bazi.get('full_chart', '未知')}
- 年柱：{bazi.get('year_pillar', '')}
- 月柱：{bazi.get('month_pillar', '')}
- 日柱：{bazi.get('day_pillar', '')}
- 时柱：{bazi.get('hour_pillar', '')}
- 五行分析：{wuxing.get('analysis', '')}
- 性格特点：{personality}
"""
        
        return f"""你是一位专业的命理大师，精通八字命理、周易预测。请根据以下信息进行详细的命理分析。

用户信息：
- 出生日期：{birth_date}
- 出生时间：{birth_time}
- 性别：{gender}
- 问题：{question}

{skill_info}

请从以下几个方面进行分析：

1. 性格分析：根据八字推断用户的性格特点
2. 运势分析：近期（最近3个月）的整体运势
3. 具体问题解答：根据用户的问题给出专业建议
4. 分析依据：用八字命理的术语解释分析原因

请用专业但易懂的语言回答，让用户信服。"""
    
    def _call_llm(self, prompt):
        try:
            messages = [
                SystemMessage(content="你是一位专业的命理大师，精通八字命理、周易预测。你的分析应该专业、详细、有理有据，让用户信服。"),
                HumanMessage(content=prompt)
            ]
            
            response = llm_client.call(messages, purpose="命理分析")
            return self._parse_llm_response(response.content) if response.content else {}
        except Exception as e:
            logger.error(f"LLM调用异常: {e}")
            return {}
    
    def _parse_llm_response(self, content):
        if not content:
            return {}
        
        result = {}
        sections = content.split("\n\n")
        
        for section in sections:
            if "性格" in section:
                result["personality"] = section.replace("性格分析：", "").replace("1. 性格分析：", "").strip()
            elif "运势" in section or "整体运势" in section:
                result["fortune"] = section.replace("运势分析：", "").replace("2. 运势分析：", "").strip()
            elif "解答" in section or "建议" in section:
                result["specific"] = section.replace("具体问题解答：", "").replace("3. 具体问题解答：", "").strip()
            elif "依据" in section or "原因" in section:
                result["reasoning"] = section.replace("分析依据：", "").replace("4. 分析依据：", "").strip()
        
        if not result:
            result["personality"] = content[:200] if len(content) > 200 else content
            result["fortune"] = content[200:400] if len(content) > 400 else ""
            result["specific"] = content[400:600] if len(content) > 600 else ""
            result["reasoning"] = content[600:] if len(content) > 600 else ""
        
        return result
    
    def _default_answer(self, question, gender):
        if "事业" in question:
            return "您的事业运势较好，建议努力工作，把握机会。"
        elif "感情" in question:
            return "您的感情运势稳定，建议保持真诚和耐心。"
        elif "健康" in question:
            return "您的健康状况良好，建议保持规律作息。"
        elif "财运" in question:
            return "您的财运平稳，建议理性理财。"
        return "您的整体运势较好，建议保持积极心态。"
