import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from caption_builder import build_caption, build_lyrics
import presets

p = {
    "prompt_mode": "structured",
    "genre": "流行 Pop",
    "subgenre": "dream pop",
    "bpm": 96,
    "key": "C",
    "scale": "大调 Major (明亮)",
    "emotional_arc": "由静到爆发(副歌高潮)",
    "scenario": "咖啡馆",
    "production": "精致录音棚",
    "vocal_gender": "女声",
    "vocal_timbre": "气声轻盈",
    "vocal_register": "中音区",
    "vocal_delivery": "轻声吟唱",
    "harmony": "轻叠加和声(副歌)",
    "backing_vocals": None,
    "vocal_effect": None,
    "primary_instruments": ["指弹吉他", "钢琴"],
    "secondary_instruments": ["刷鼓", "木贝斯"],
    "groove": "慵懒松弛 Pocket",
    "bass": "木贝斯",
    "percussion": "刷鼓轻击",
    "textures": ["温暖 Pad 垫底"],
    "spatial": "小房间",
    "arrangement_notes": "Intro piano only, chorus full band.",
    "lyrics": "[Verse]\n测试歌词\n[Chorus]\n测试副歌",
    "instrumental": False,
}
cap = build_caption(p)
print(cap)
print("=" * 40)

p2 = dict(p, vocal_gender="纯器乐(无人声)", instrumental=True)
cap2 = build_caption(p2)
print(cap2)
print("=" * 40)
print(repr(build_lyrics("[Intro]\n词会被丢弃在这里\n[Instrumental]", True)))

# 简单模式
p3 = dict(p, prompt_mode="simple", simple_prompt="A warm acoustic pop song.")
print(build_caption(p3))

# UI 构建
import app as app_module
demo = app_module.build_ui()
print("UI OK, blocks:", len(demo.blocks))
