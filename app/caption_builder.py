"""将界面参数组装为 MiniMax Music 3 官方推荐的 Structured Caption。

三段式结构:Global Metadata / Vocal Details / Arrangement,输出为英文。
"""

from presets import (
    GENRES, SCALES, EMOTIONAL_ARCS, SCENARIOS, PRODUCTION_PROFILES,
    VOCAL_GENDERS, VOCAL_TIMBRES, VOCAL_REGISTERS, VOCAL_DELIVERIES,
    HARMONIES, BACKING_VOCALS, VOCAL_EFFECTS, INSTRUMENTS,
    GROOVES, PERCUSSION_STYLES, TEXTURES, SPATIAL_EFFECTS,
)


def _join(items):
    return ", ".join(items)


def build_caption(p):
    """p: 参数字典(键名与 app.py 的 UI 组件一一对应)。返回英文 Structured Caption。"""
    if p.get("prompt_mode") == "simple":
        return p.get("simple_prompt", "").strip()

    lines = []

    # ---------- Global Metadata ----------
    meta = []
    genre_en = GENRES.get(p.get("genre"), p.get("genre", ""))
    sub = (p.get("subgenre") or "").strip()
    style_bits = [genre_en] + ([sub] if sub else [])
    meta.append(f"Genre: {_join(style_bits)}.")
    if p.get("bpm"):
        meta.append(f"BPM: {int(p['bpm'])}.")
    if p.get("key"):
        key_line = f"Key: {p['key']}"
        if p.get("scale"):
            key_line += f" {SCALES.get(p['scale'], p['scale'])}"
        meta.append(key_line + ".")
    if p.get("emotional_arc"):
        meta.append(f"Emotional progression: {EMOTIONAL_ARCS.get(p['emotional_arc'], p['emotional_arc'])}.")
    if p.get("scenario"):
        meta.append(f"Listening scenario: {SCENARIOS.get(p['scenario'], p['scenario'])}.")
    if p.get("production"):
        meta.append(f"Production profile: {PRODUCTION_PROFILES.get(p['production'], p['production'])}.")
    lines.append("Global Metadata\n" + " ".join(meta))

    # ---------- Vocal Details ----------
    gender = p.get("vocal_gender") or ""
    gender_en = VOCAL_GENDERS.get(gender, gender)
    if gender_en is None or p.get("instrumental"):
        vocal_lead = []
        prim = [INSTRUMENTS.get(x, x) for x in (p.get("primary_instruments") or [])]
        if prim:
            vocal_lead.append(f"The {prim[0]} carries the lead melodic role.")
        lines.append("Vocal Details\nThis piece is instrumental with no lead vocals. " + " ".join(vocal_lead))
    else:
        vocal = []
        bits = [f"{gender_en} lead vocal"]
        if p.get("vocal_timbre") and p["vocal_timbre"] in VOCAL_TIMBRES:
            bits.append(VOCAL_TIMBRES[p["vocal_timbre"]])
        if p.get("vocal_register") and p["vocal_register"] in VOCAL_REGISTERS:
            bits.append(f"singing mostly in {VOCAL_REGISTERS[p['vocal_register']]}")
        vocal.append("Vocals: " + ", ".join(bits) + ".")
        if p.get("vocal_delivery") and p["vocal_delivery"] in VOCAL_DELIVERIES:
            vocal.append(f"Delivery: {VOCAL_DELIVERIES[p['vocal_delivery']]}.")
        if p.get("harmony") and p["harmony"] in HARMONIES and HARMONIES[p["harmony"]]:
            vocal.append(f"Harmony: {HARMONIES[p['harmony']]}.")
        if p.get("backing_vocals") and p["backing_vocals"] in BACKING_VOCALS and BACKING_VOCALS[p["backing_vocals"]]:
            vocal.append(f"Backing vocals: {BACKING_VOCALS[p['backing_vocals']]}.")
        if p.get("vocal_effect") and p["vocal_effect"] in VOCAL_EFFECTS and VOCAL_EFFECTS[p["vocal_effect"]]:
            vocal.append(f"Vocal effects: {VOCAL_EFFECTS[p['vocal_effect']]}.")
        lines.append("Vocal Details\n" + " ".join(vocal))

    # ---------- Arrangement ----------
    arr = []
    prim = [INSTRUMENTS.get(x, x) for x in (p.get("primary_instruments") or [])]
    sec = [INSTRUMENTS.get(x, x) for x in (p.get("secondary_instruments") or [])]
    if prim:
        arr.append(f"Primary instruments: { _join(prim)}.")
    if sec:
        arr.append(f"Secondary instruments: {_join(sec)}.")
    if p.get("groove") and p["groove"] in GROOVES:
        arr.append(f"Groove: {GROOVES[p['groove']]}.")
    if p.get("bass") and p["bass"] in INSTRUMENTS:
        arr.append(f"Bass: {INSTRUMENTS[p['bass']]}.")
    if p.get("percussion") and p["percussion"] in PERCUSSION_STYLES:
        arr.append(f"Percussion: {PERCUSSION_STYLES[p['percussion']]}.")
    textures = [TEXTURES[t] for t in (p.get("textures") or []) if t in TEXTURES]
    if textures:
        arr.append(f"Textures: {_join(textures)}.")
    if p.get("spatial") and p["spatial"] in SPATIAL_EFFECTS:
        arr.append(f"Spatial character: {SPATIAL_EFFECTS[p['spatial']]}.")
    notes = (p.get("arrangement_notes") or "").strip()
    if notes:
        arr.append(notes)
    if arr:
        lines.append("Arrangement\n" + " ".join(arr))

    return "\n\n".join(lines)


def build_lyrics(lyrics_text, instrumental):
    """器乐模式下清空歌词文本,仅保留段落标签骨架。"""
    text = (lyrics_text or "").strip()
    if instrumental and text:
        tags = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("[")]
        return "\n".join(tags) if tags else "[Instrumental]"
    return text
