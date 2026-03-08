---
name: bazi-analysis
description: Use this skill when analyzing a user's BaZi (Eight Characters) chart for personality, destiny, and fortune insights
---

# BaZi Analysis Skill

This skill provides a structured workflow for analyzing BaZi charts and providing fortune-telling insights.

## When to Use This Skill

Use this skill when asked to:
- Analyze a user's BaZi (八字) chart
- Provide personality analysis based on birth date/time
- Predict fortune and luck cycles
- Answer questions about career, relationships, health, or wealth

## Required Information

Before analysis, collect the following:
1. **Birth Date** (公历出生日期): Year-Month-Day format (e.g., 1990-05-15)
2. **Birth Time** (出生时间): Hour:Minute format (e.g., 14:30)
3. **Gender** (性别): Male/Female

## How to Use

The skill provides a Python script that calculates and analyzes BaZi chart.

### Basic Usage

```bash
python .agents/skills/bazi-analysis/bazi_analyzer.py "1990-05-15" "14:30" "男"
```

Or with JSON output (default):
```bash
python .agents/skills/bazi-analysis/bazi_analyzer.py "1990-05-15" "14:30" "男" --format json
```

With text output:
```bash
python .agents/skills/bazi-analysis/bazi_analyzer.py "1990-05-15" "14:30" "男" --format text
```

**Arguments:**
- `birth_date` (required): Birth date in YYYY-MM-DD format
- `birth_time` (required): Birth time in HH:MM format
- `gender` (required): Gender (男/女 or male/female)
- `--format` (optional): Output format (json or text, default: json)

### Output Format

**JSON Format:**
```json
{
  "bazi": {
    "year_pillar": "庚午",
    "month_pillar": "辛巳",
    "day_pillar": "壬申",
    "hour_pillar": "癸未",
    "full_chart": "庚午 辛巳 壬申 癸未"
  },
  "wuxing": {
    "distribution": {"金": 3, "木": 0, "水": 2, "火": 2, "土": 1},
    "strongest": "金",
    "weakest": "木",
    "missing": ["木"],
    "analysis": "五行分布：金3个，木0个，水2个，火2个，土1个。金最旺，木最弱。"
  },
  "personality": "性格聪明，善于应变，有远大抱负，但有时好高骛远。"
}
```

**Text Format:**
```
八字排盘: 庚午 辛巳 壬申 癸未
  年柱: 庚午
  月柱: 辛巳
  日柱: 壬申
  时柱: 癸未

五行分析: 五行分布：金3个，木0个，水2个，火2个，土1个。金最旺，木最弱。
  最旺: 金
  最弱: 木
  缺失: 木

性格特点: 性格聪明，善于应变，有远大抱负，但有时好高骛远。
```

## Analysis Workflow

### Step 1: Calculate BaZi Chart

Calculate the Four Pillars (四柱):
- Year Pillar (年柱): Based on birth year
- Month Pillar (月柱): Based on birth month
- Day Pillar (日柱): Based on birth day
- Hour Pillar (时柱): Based on birth hour

### Step 2: Analyze Five Elements (五行)

Count and balance the Five Elements:
- Metal (金)
- Wood (木)
- Water (水)
- Fire (火)
- Earth (土)

### Step 3: Personality Analysis (性格分析)

Based on the Day Master (日主), analyze personality traits.

### Step 4: Provide Recommendations

Based on the analysis, provide specific advice for the user's question.

## Important Notes

1. Always use professional but accessible language
2. Provide specific, actionable advice
3. Balance traditional concepts with modern understanding
4. Be respectful of the user's beliefs
5. Never make absolute predictions - use probability language
