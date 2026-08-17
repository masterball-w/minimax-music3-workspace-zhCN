"""音乐生成选项库:所有下拉/多选选项及其中文标签到英文 caption 片段的映射。"""

GENRES = {
    "流行 Pop": "pop",
    "摇滚 Rock": "rock",
    "民谣 Folk": "folk",
    "爵士 Jazz": "jazz",
    "电子 Electronic": "electronic",
    "嘻哈 Hip-Hop": "hip-hop",
    "R&B / 灵魂乐": "R&B / soul",
    "古典跨界 Classical crossover": "classical crossover",
    "乡村 Country": "country",
    "金属 Metal": "metal",
    "拉丁 Latin": "latin",
    "雷鬼 Reggae": "reggae",
    "布鲁斯 Blues": "blues",
    "波萨诺瓦 Bossa nova": "bossa nova",
    "凯尔特 Celtic": "celtic",
    "福音 Gospel": "gospel",
    "Lo-fi": "lo-fi",
    "氛围 Ambient": "ambient",
    "合成器浪潮 Synthwave": "synthwave",
    "国风 Chinese traditional": "Chinese traditional style",
    "音乐剧 Musical theatre": "musical theatre",
}

SUBGENRE_HINTS = {
    "流行 Pop": ["dream pop 梦幻流行", "indie pop 独立流行", "synth-pop 合成器流行", "chamber pop 室内流行",
               "power pop 强力流行", "city pop 城市流行", "art pop 艺术流行"],
    "摇滚 Rock": ["alternative rock 另类摇滚", "indie rock 独立摇滚", "punk 朋克", "post-rock 后摇",
                "progressive rock 前卫摇滚", "garage rock 车库摇滚", "soft rock 柔和摇滚"],
    "民谣 Folk": ["acoustic folk 原声民谣", "folk rock 民谣摇滚", "singer-songwriter 唱作人", "indie folk 独立民谣"],
    "爵士 Jazz": ["bebop 比波普", "cool jazz 冷爵士", "jazz fusion 融合爵士", "vocal jazz 人声爵士", "swing 摇摆"],
    "电子 Electronic": ["house 浩室", "techno 科技舞曲", "drum and bass 鼓打贝斯", "trance 出神", "IDM 智能舞曲",
                      "future bass", "chillwave"],
    "嘻哈 Hip-Hop": ["boom bap", "trap", "lo-fi hip-hop", "drill", "jazz rap 爵士说唱", "cloud rap"],
    "R&B / 灵魂乐": ["contemporary R&B 当代节奏布鲁斯", "neo soul 新灵魂乐", "motown", "quiet storm"],
    "国风 Chinese traditional": ["古风 gufeng", "民乐融合 folk fusion", "戏腔 opera-influenced vocal"],
}

SCALES = {
    "大调 Major (明亮)": "major",
    "小调 Minor (暗淡)": "minor",
    "多利亚 Dorian (朦胧)": "dorian",
    "混合利底亚 Mixolydian (摇滚感)": "mixolydian",
    "和声小调 Harmonic minor (异域)": "harmonic minor",
    "五声音阶 Pentatonic (东方/民谣)": "pentatonic",
    "布鲁斯音阶 Blues scale": "blues scale",
}

KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
KEY_MODES = {"自然音": "", "升半音": "#", "降半音": "b"}

EMOTIONAL_ARCS = {
    "平静温暖贯穿始终": "steady warmth throughout",
    "由静到爆发(副歌高潮)": "gentle build into a soaring, wide chorus",
    "忧郁转向希望": "melancholy verses resolving into hope",
    "紧张到释放": "tension and release across sections",
    "黑暗走向胜利": "dark verses rising to a triumphant finale",
    "轻盈俏皮贯穿": "light and playful throughout",
    "怀旧感伤贯穿": "nostalgic and wistful throughout",
    "史诗感层层推进": "epic, layer-by-layer escalation",
}

SCENARIOS = {
    "清晨通勤": "a morning commute",
    "深夜驾车": "a late-night drive",
    "咖啡馆": "a quiet coffee shop",
    "运动健身": "a workout session",
    "学习专注": "a focused study session",
    "雨天窗边": "a rainy window at dusk",
    "海滩日落": "a beach sunset",
    "音乐节现场": "a festival stage",
    "篝火旁": "a campfire gathering",
    "游戏副本": "an epic game quest",
}

PRODUCTION_PROFILES = {
    "精致录音棚": "polished studio production",
    "Lo-fi 家庭录音": "lo-fi home-recording character",
    "复古模拟磁带": "vintage analog tape warmth",
    "电台级成品": "radio-ready, loud and glossy",
    "现场房间感": "live-room, band-in-a-room feel",
    "卧室 DIY": "bedroom-pop DIY aesthetic",
    "电影级宽阔": "cinematic, wide-screen mix",
    "车库粗粝": "raw garage energy",
}

VOCAL_GENDERS = {
    "女声": "female",
    "男声": "male",
    "混合(男女对唱)": "a female/male duet",
    "童声": "a child",
    "合唱团主导": "a choir",
    "纯器乐(无人声)": None,
}

VOCAL_TIMBRES = {
    "气声轻盈": "airy and breathy",
    "温暖醇厚": "warm and rounded",
    "沙哑粗粝": "husky and raspy",
    "清亮通透": "bright and clear",
    "低沉浑厚": "deep and resonant",
    "鼻腔共鸣": "nasal and forward",
    "丝滑柔顺": "smooth and silky",
    "中性特质": "androgynous",
    "野性原始": "raw and gritty",
}

VOCAL_REGISTERS = {
    "低音区": "low register",
    "中音区": "mid register",
    "高音区": "high register",
    "宽音域跨越": "wide range across registers",
    "假声为主": "falsetto-leaning",
}

VOCAL_DELIVERIES = {
    "轻声吟唱": "soft crooning",
    "叙事说书": "conversational storytelling",
    "爆发式高唱": "powerful belting",
    "说唱 Flow": "rapped verses with tight flow",
    "R&B 转音": "melismatic R&B runs",
    "耳语式": "whispered intimacy",
    "念白式": "spoken-word",
    "歌剧式": "operatic legato",
    "戏腔": "Chinese opera-influenced ornamentation",
    "呐喊式": "anthemic shouting",
}

HARMONIES = {
    "无和声": None,
    "轻叠加和声(副歌)": "light stacked harmonies in the chorus",
    "全程和声垫": "harmonies doubling the lead throughout",
    "呼应式和声": "call-and-response harmonies",
    "完整合唱团": "a full choir",
}

BACKING_VOCALS = {
    "无伴唱": None,
    "副歌合唱垫": "chorus gang vocals",
    "人声切片/Pad": "vocal chops and pads",
    "哼鸣伴唱": "wordless humming pads",
    "福音式应答": "gospel-style answers",
}

VOCAL_EFFECTS = {
    "无效果": None,
    "轻微混响": "light plate reverb",
    "电话音 EQ": "telephone-band EQ",
    "磁带饱和": "tape saturation",
    "轻微自动调谐": "subtle pitch correction",
    "回声延迟": "slap-back delay",
    "声码器": "vocoder treatment",
    "双重录音": "doubled lead vocal",
}

INSTRUMENTS = {
    "木吉他": "acoustic guitar",
    "指弹吉他": "fingerpicked guitar",
    "电吉他(清音)": "clean electric guitar",
    "电吉他(失真)": "distorted electric guitars",
    "钢琴": "piano",
    "三角钢琴": "grand piano",
    "电钢琴": "electric piano",
    "合成器 Pad": "warm synth pads",
    "模拟合成器 Lead": "analog synth lead",
    "弦乐组": "string section",
    "大提琴": "cello",
    "小提琴": "violin",
    "铜管组": "brass section",
    "萨克斯": "saxophone",
    "小号": "trumpet",
    "长笛": "flute",
    "摇滚鼓组": "full rock drum kit",
    "刷鼓": "brushed drums",
    "电子鼓": "electronic drums",
    "鼓机": "drum machine",
    "木贝斯": "upright bass",
    "电贝斯": "electric bass",
    "合成贝斯": "synth bass",
    "808 贝斯": "808 bass",
    "班卓琴": "banjo",
    "曼陀林": "mandolin",
    "尤克里里": "ukulele",
    "口琴": "harmonica",
    "风琴": "organ",
    "竖琴": "harp",
    "马林巴": "marimba",
    "钢片琴": "celesta",
    "手风琴": "accordion",
    "西塔琴": "sitar",
    "二胡": "erhu",
    "古筝": "guzheng",
    "琵琶": "pipa",
    "笛子": "bamboo flute",
    "古琴": "guqin",
    "太鼓": "taiko drums",
    "手打击乐": "hand percussion",
    "拍手声": "handclaps",
    "铃鼓与碰铃": "tambourine and bells",
    "人声合唱": "choir vocals",
    "黑胶噪声": "vinyl crackle",
    "环境声采样": "field-recording ambience",
}

GROOVES = {
    "四四平直(舞曲)": "steady four-on-the-floor",
    "切分律动": "syncopated groove",
    "摇摆 Swing": "swinging groove",
    "半拍感 Half-time": "half-time feel",
    "双倍速 Double-time": "double-time drive",
    "平直八分音符推进": "driving straight eighths",
    "慵懒松弛 Pocket": "laid-back pocket",
    "雷鬼反拍": "reggae skank",
    "Shuffle": "shuffle pattern",
    "碎拍 Breakbeat": "breakbeat pattern",
    "Trap Hi-hat": "trap hi-hat patterns",
}

PERCUSSION_STYLES = {
    "完整鼓组": "a full drum kit",
    "刷鼓轻击": "soft brushed kit",
    "电子鼓机": "programmed electronic drums",
    "手打击乐": "hand percussion only",
    "无鼓": "no drums",
    "管弦打击": "orchestral percussion",
    "极简点缀": "sparse, minimal hits",
}

TEXTURES = {
    "温暖 Pad 垫底": "warm pad beds",
    "闪亮混响尾": "shimmering reverb tails",
    "磁带底噪": "tape hiss",
    "黑胶噼啪": "vinyl crackle",
    "白噪上扬": "white-noise risers",
    "次贝斯涌动": "sub-bass swells",
    "氛围田野录音": "ambient field recordings",
    "毛刺切割": "glitch stutters",
    "八位机音色": "8-bit chiptune bleeps",
}

SPATIAL_EFFECTS = {
    "干而贴近": "dry and close",
    "小房间": "small-room ambience",
    "大厅混响": "cavernous hall reverb",
    "宽立体声": "wide stereo image",
    "教堂空间": "cathedral-like space",
    "板式混响": "plate reverb",
    "磁带延迟": "tape delay throws",
    "乒乓延迟": "ping-pong delay",
}

SONG_STRUCTURES = {
    "标准流行曲式": "[Intro]\n[Verse]\n[Pre-Chorus]\n[Chorus]\n[Verse]\n[Chorus]\n[Bridge]\n[Chorus]\n[Outro]",
    "短版双段": "[Verse]\n[Chorus]\n[Verse]\n[Chorus]",
    "叙事民谣": "[Intro]\n[Verse]\n[Verse]\n[Chorus]\n[Verse]\n[Chorus]\n[Outro]",
    "带器乐段": "[Intro]\n[Verse]\n[Chorus]\n[Instrumental]\n[Verse]\n[Chorus]\n[Solo]\n[Chorus]\n[Outro]",
    "纯器乐曲": "[Intro]\n[Instrumental]\n[Instrumental]\n[Solo]\n[Instrumental]\n[Outro]",
    "副歌后置钩子": "[Verse]\n[Pre-Chorus]\n[Chorus]\n[Post-Chorus]\n[Verse]\n[Pre-Chorus]\n[Chorus]\n[Post-Chorus]\n[Outro]",
}

SECTION_TAGS = ["[Intro]", "[Verse]", "[Pre-Chorus]", "[Chorus]", "[Post-Chorus]", "[Bridge]",
                "[Instrumental]", "[Solo]", "[Outro]"]

STYLE_PRESETS = {
    "温暖原声流行": {
        "genre": "流行 Pop", "subgenre": "acoustic pop", "bpm": 96, "key": "C", "scale": "大调 Major (明亮)",
        "arc": "由静到爆发(副歌高潮)", "production": "精致录音棚",
        "vocal_gender": "女声", "timbre": "气声轻盈", "delivery": "轻声吟唱",
        "harmony": "轻叠加和声(副歌)", "primary": ["指弹吉他", "钢琴"], "secondary": ["刷鼓", "木贝斯"],
        "groove": "慵懒松弛 Pocket", "spatial": "小房间", "texture": ["温暖 Pad 垫底"],
    },
    "深夜合成驰放": {
        "genre": "电子 Electronic", "subgenre": "chillwave", "bpm": 88, "key": "F#", "scale": "小调 Minor (暗淡)",
        "arc": "怀旧感伤贯穿", "production": "复古模拟磁带",
        "vocal_gender": "女声", "timbre": "温暖醇厚", "delivery": "耳语式",
        "harmony": "全程和声垫", "primary": ["模拟合成器 Lead", "合成器 Pad"], "secondary": ["鼓机", "合成贝斯"],
        "groove": "慵懒松弛 Pocket", "spatial": "宽立体声", "texture": ["磁带底噪", "黑胶噼啪"],
    },
    "热血摇滚": {
        "genre": "摇滚 Rock", "subgenre": "alternative rock", "bpm": 138, "key": "E", "scale": "混合利底亚 Mixolydian (摇滚感)",
        "arc": "黑暗走向胜利", "production": "车库粗粝",
        "vocal_gender": "男声", "timbre": "沙哑粗粝", "delivery": "爆发式高唱",
        "harmony": "呼应式和声", "primary": ["电吉他(失真)", "摇滚鼓组"], "secondary": ["电贝斯", "风琴"],
        "groove": "平直八分音符推进", "spatial": "宽立体声", "texture": [],
    },
    "国风戏韵": {
        "genre": "国风 Chinese traditional", "subgenre": "古风 gufeng", "bpm": 72, "key": "D", "scale": "五声音阶 Pentatonic (东方/民谣)",
        "arc": "忧郁转向希望", "production": "电影级宽阔",
        "vocal_gender": "女声", "timbre": "清亮通透", "delivery": "戏腔",
        "harmony": "无和声", "primary": ["古筝", "笛子", "琵琶"], "secondary": ["弦乐组", "手打击乐"],
        "groove": "切分律动", "spatial": "大厅混响", "texture": ["氛围田野录音"],
    },
    "Lo-fi 学习节拍": {
        "genre": "Lo-fi", "subgenre": "lo-fi hip-hop", "bpm": 78, "key": "A", "scale": "多利亚 Dorian (朦胧)",
        "arc": "平静温暖贯穿始终", "production": "Lo-fi 家庭录音",
        "vocal_gender": "纯器乐(无人声)", "timbre": "", "delivery": "",
        "harmony": "无和声", "primary": ["电钢琴"], "secondary": ["鼓机", "电贝斯"],
        "groove": "慵懒松弛 Pocket", "spatial": "小房间", "texture": ["黑胶噼啪", "磁带底噪"],
    },
    "爵士酒吧": {
        "genre": "爵士 Jazz", "subgenre": "vocal jazz 人声爵士", "bpm": 108, "key": "Bb", "scale": "大调 Major (明亮)",
        "arc": "轻盈俏皮贯穿", "production": "现场房间感",
        "vocal_gender": "女声", "timbre": "丝滑柔顺", "delivery": "R&B 转音",
        "harmony": "呼应式和声", "primary": ["三角钢琴", "木贝斯"], "secondary": ["刷鼓", "萨克斯"],
        "groove": "摇摆 Swing", "spatial": "小房间", "texture": [],
    },
}
