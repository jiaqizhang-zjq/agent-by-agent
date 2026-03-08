#!/usr/bin/env python3
"""BaZi Analysis Tool.

Calculates and analyzes BaZi (Eight Characters) chart.
"""

import argparse
import datetime
import json
from typing import Dict


def calculate_bazi(birth_date: str, birth_time: str, gender: str) -> Dict:
    """Calculate BaZi chart from birth information.
    
    Parameters
    ----------
    birth_date : str
        Birth date in YYYY-MM-DD format
    birth_time : str
        Birth time in HH:MM format
    gender : str
        Gender (男/女 or male/female)
    
    Returns:
        Dictionary containing BaZi chart information
    """
    try:
        year, month, day = birth_date.split('-')
        hour, minute = birth_time.split(':')
        
        tian_gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        di_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        year_num = int(year)
        year_gan = tian_gan[(year_num - 4) % 10]
        year_zhi = di_zhi[(year_num - 4) % 12]
        year_pillar = year_gan + year_zhi
        
        month_num = int(month)
        month_gan = tian_gan[(year_num * 12 + month_num + 13) % 10]
        month_zhi = di_zhi[(month_num + 1) % 12]
        month_pillar = month_gan + month_zhi
        
        day_num = int(day)
        base_date = datetime.date(1900, 1, 31)
        target_date = datetime.date(int(year), int(month), int(day))
        days = (target_date - base_date).days
        day_gan = tian_gan[days % 10]
        day_zhi = di_zhi[days % 12]
        day_pillar = day_gan + day_zhi
        
        hour_num = int(hour)
        hour_zhi_index = (hour_num + 1) // 2 % 12
        hour_zhi = di_zhi[hour_zhi_index]
        hour_gan = tian_gan[(days * 12 + hour_zhi_index) % 10]
        hour_pillar = hour_gan + hour_zhi
        
        return {
            "success": True,
            "bazi": {
                "year_pillar": year_pillar,
                "month_pillar": month_pillar,
                "day_pillar": day_pillar,
                "hour_pillar": hour_pillar,
                "full_chart": f"{year_pillar} {month_pillar} {day_pillar} {hour_pillar}"
            },
            "birth_info": {
                "date": birth_date,
                "time": birth_time,
                "gender": gender
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_wuxing(bazi: Dict) -> Dict:
    """Analyze Five Elements distribution.
    
    Parameters
    ----------
    bazi : Dict
        BaZi chart information
    
    Returns:
        Dictionary containing Five Elements analysis
    """
    wuxing_map = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
        '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
        '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
        '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
        '戌': '土', '亥': '水'
    }
    
    wuxing_count = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
    
    for pillar in ['year_pillar', 'month_pillar', 'day_pillar', 'hour_pillar']:
        if pillar in bazi:
            for char in bazi[pillar]:
                if char in wuxing_map:
                    wuxing = wuxing_map[char]
                    wuxing_count[wuxing] += 1
    
    max_wuxing = max(wuxing_count, key=wuxing_count.get)
    min_wuxing = min(wuxing_count, key=wuxing_count.get)
    
    return {
        "distribution": wuxing_count,
        "strongest": max_wuxing,
        "weakest": min_wuxing,
        "missing": [k for k, v in wuxing_count.items() if v == 0],
        "analysis": f"五行分布：金{wuxing_count['金']}个，木{wuxing_count['木']}个，水{wuxing_count['水']}个，火{wuxing_count['火']}个，土{wuxing_count['土']}个。{max_wuxing}最旺，{min_wuxing}最弱。"
    }


def analyze_personality(day_pillar: str) -> str:
    """Analyze personality based on Day Master.
    
    Parameters
    ----------
    day_pillar : str
        Day pillar (日柱)
    
    Returns:
        Personality analysis
    """
    day_gan = day_pillar[0] if len(day_pillar) > 0 else ''
    
    personality_map = {
        '甲': '性格刚强，有领导力，正直无私，但有时过于固执。',
        '乙': '性格温和，善于交际，灵活变通，但有时优柔寡断。',
        '丙': '性格热情，光明磊落，积极向上，但有时急躁冲动。',
        '丁': '性格细腻，心思缜密，有艺术天赋，但有时多愁善感。',
        '戊': '性格稳重，诚实守信，有责任心，但有时过于保守。',
        '己': '性格温和，善于包容，脚踏实地，但有时缺乏主见。',
        '庚': '性格刚毅，果断坚决，有正义感，但有时过于严厉。',
        '辛': '性格清高，追求完美，有创新精神，但有时过于挑剔。',
        '壬': '性格聪明，善于应变，有远大抱负，但有时好高骛远。',
        '癸': '性格内敛，富有智慧，善于思考，但有时过于敏感。'
    }
    
    return personality_map.get(day_gan, '性格独特，有自己的特点。')


def main() -> None:
    """Main entry point for the BaZi analysis CLI tool."""
    parser = argparse.ArgumentParser(description="Analyze BaZi (Eight Characters) chart")
    parser.add_argument("birth_date", type=str, help="Birth date in YYYY-MM-DD format")
    parser.add_argument("birth_time", type=str, help="Birth time in HH:MM format")
    parser.add_argument("gender", type=str, help="Gender (男/女 or male/female)")
    parser.add_argument("--format", type=str, default="json", choices=["json", "text"], 
                        help="Output format (default: json)")

    args = parser.parse_args()
    
    result = calculate_bazi(args.birth_date, args.birth_time, args.gender)
    
    if not result["success"]:
        print(f"Error: {result['error']}")
        return
    
    bazi = result["bazi"]
    wuxing = analyze_wuxing(bazi)
    personality = analyze_personality(bazi["day_pillar"])
    
    if args.format == "json":
        output = {
            "bazi": bazi,
            "wuxing": wuxing,
            "personality": personality
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n八字排盘: {bazi['full_chart']}")
        print(f"  年柱: {bazi['year_pillar']}")
        print(f"  月柱: {bazi['month_pillar']}")
        print(f"  日柱: {bazi['day_pillar']}")
        print(f"  时柱: {bazi['hour_pillar']}")
        print(f"\n五行分析: {wuxing['analysis']}")
        print(f"  最旺: {wuxing['strongest']}")
        print(f"  最弱: {wuxing['weakest']}")
        if wuxing['missing']:
            print(f"  缺失: {', '.join(wuxing['missing'])}")
        print(f"\n性格特点: {personality}")


if __name__ == "__main__":
    main()
