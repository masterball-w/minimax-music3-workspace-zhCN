"""MiniMax Music 3 本地音乐生成工作站(Gradio)。

用法: python app.py  →  浏览器访问 http://127.0.0.1:7860
"""

import os
import sys
import time
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr

from presets import (
    GENRES, SUBGENRE_HINTS, SCALES, KEYS, EMOTIONAL_ARCS, SCENARIOS,
    PRODUCTION_PROFILES, VOCAL_GENDERS, VOCAL_TIMBRES, VOCAL_REGISTERS,
    VOCAL_DELIVERIES, HARMONIES, BACKING_VOCALS, VOCAL_EFFECTS,
    INSTRUMENTS, GROOVES, PERCUSSION_STYLES, TEXTURES, SPATIAL_EFFECTS,
    SONG_STRUCTURES, STYLE_PRESETS, SECTION_TAGS,
)
from caption_builder import build_caption, build_lyrics
import inference

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT, "outputs")

BASS_OPTIONS = ["(跟随主乐器自动)"] + [k for k in INSTRUMENTS if "贝斯" in k or "bass" in k]
KEY_OPTIONS = ["(自动)"] + KEYS
SCALE_OPTIONS = ["(自动)"] + list(SCALES.keys())
NONE_OPTIONS = ["(不指定)"]

DEFAULT_LYRICS = """[Verse]
晨光穿过高高的白杨
风把昨夜的梦轻轻晾干
[Pre-Chorus]
我数着心跳靠近答案
[Chorus]
把热爱唱成漫天星光
每一步都朝着远方"""


def _opt(options, label=None):
    return label if label in options else (options[0] if options else None)


def apply_preset(preset_name):
    p = STYLE_PRESETS.get(preset_name)
    if not p:
        return [gr.update()] * len(ORDERED_COMPONENT_KEYS)
    updates = {
        "genre": gr.update(value=p["genre"]),
        "subgenre": gr.update(value=p["subgenre"]),
        "bpm_auto": gr.update(value=False),
        "bpm": gr.update(value=p.get("bpm", 100)),
        "key": gr.update(value=p.get("key", "(自动)")),
        "scale": gr.update(value=p.get("scale", "(自动)")),
        "emotional_arc": gr.update(value=_opt(list(EMOTIONAL_ARCS.keys()), p.get("arc"))),
        "scenario": gr.update(value="(不指定)"),
        "production": gr.update(value=_opt(list(PRODUCTION_PROFILES.keys()), p.get("production"))),
        "vocal_gender": gr.update(value=_opt(list(VOCAL_GENDERS.keys()), p.get("vocal_gender"))),
        "timbre": gr.update(value=_opt(list(VOCAL_TIMBRES.keys()), p.get("timbre")) or "(不指定)"),
        "register": gr.update(value=_opt(list(VOCAL_REGISTERS.keys()), p.get("register")) or "(不指定)"),
        "delivery": gr.update(value=_opt(list(VOCAL_DELIVERIES.keys()), p.get("delivery")) or "(不指定)"),
        "harmony": gr.update(value=_opt(list(HARMONIES.keys()), p.get("harmony")) or "无和声"),
        "backing_vocals": gr.update(value=_opt(list(BACKING_VOCALS.keys()), p.get("backing_vocals")) or "无伴唱"),
        "vocal_effect": gr.update(value="无效果"),
        "primary_instruments": gr.update(value=p.get("primary", [])),
        "secondary_instruments": gr.update(value=p.get("secondary", [])),
        "groove": gr.update(value=_opt(list(GROOVES.keys()), p.get("groove")) or "(不指定)"),
        "bass": gr.update(value=BASS_OPTIONS[0]),
        "percussion": gr.update(value=_opt(list(PERCUSSION_STYLES.keys()), p.get("percussion")) or "(不指定)"),
        "textures": gr.update(value=p.get("texture", [])),
        "spatial": gr.update(value=_opt(list(SPATIAL_EFFECTS.keys()), p.get("spatial")) or "(不指定)"),
    }
    return [updates[k] for k in ORDERED_COMPONENT_KEYS]


ORDERED_COMPONENT_KEYS = [
    "genre", "subgenre", "bpm_auto", "bpm", "key", "scale", "emotional_arc", "scenario", "production",
    "vocal_gender", "timbre", "register", "delivery", "harmony", "backing_vocals", "vocal_effect",
    "primary_instruments", "secondary_instruments", "groove", "bass", "percussion", "textures", "spatial",
]


def insert_structure(structure_name):
    return SONG_STRUCTURES.get(structure_name, "")


def append_tag(lyrics, tag):
    if not lyrics:
        return tag
    return lyrics.rstrip() + "\n" + tag


def preview_caption(**kw):
    params = _collect(kw)
    caption = build_caption(params)
    lyrics = build_lyrics(params["lyrics"], params["instrumental"])
    token_note = f"歌词已处理(段落标签独占一行),共 {len(lyrics)} 字符"
    return caption, token_note


def _collect(kw):
    instrumental = kw["vocal_gender"] == "纯器乐(无人声)"
    params = {
        "prompt_mode": "simple" if kw["prompt_mode"] == "简单描述" else "structured",
        "simple_prompt": kw["simple_prompt"],
        "genre": kw["genre"],
        "subgenre": kw["subgenre"] if kw["subgenre"] != "(不指定)" else "",
        "bpm": None if (kw["bpm_auto"] or kw["bpm"] is None) else int(kw["bpm"]),
        "key": None if kw["key"] == "(自动)" else kw["key"],
        "scale": None if kw["scale"] == "(自动)" else kw["scale"],
        "emotional_arc": None if kw["emotional_arc"] == "(不指定)" else kw["emotional_arc"],
        "scenario": None if kw["scenario"] == "(不指定)" else kw["scenario"],
        "production": None if kw["production"] == "(不指定)" else kw["production"],
        "vocal_gender": kw["vocal_gender"],
        "vocal_timbre": None if kw["timbre"] == "(不指定)" else kw["timbre"],
        "vocal_register": None if kw["register"] == "(不指定)" else kw["register"],
        "vocal_delivery": None if kw["delivery"] == "(不指定)" else kw["delivery"],
        "harmony": None if kw["harmony"] in NONE_OPTIONS + ["无和声"] else kw["harmony"],
        "backing_vocals": None if kw["backing_vocals"] in NONE_OPTIONS + ["无伴唱"] else kw["backing_vocals"],
        "vocal_effect": None if kw["vocal_effect"] in NONE_OPTIONS + ["无效果"] else kw["vocal_effect"],
        "primary_instruments": kw["primary_instruments"],
        "secondary_instruments": kw["secondary_instruments"],
        "groove": None if kw["groove"] == "(不指定)" else kw["groove"],
        "bass": None if kw["bass"] == BASS_OPTIONS[0] else kw["bass"],
        "percussion": None if kw["percussion"] == "(不指定)" else kw["percussion"],
        "textures": kw["textures"],
        "spatial": None if kw["spatial"] == "(不指定)" else kw["spatial"],
        "arrangement_notes": kw["arrangement_notes"],
        "lyrics": kw["lyrics"],
        "instrumental": instrumental,
    }
    return params


def run_generate(progress=gr.Progress(), *vals):
    kw = dict(zip(GENERATE_KEYS, vals))
    params = _collect(kw)
    caption = build_caption(params)
    if not caption.strip():
        raise gr.Error("音乐描述为空:请填写简单描述或选择结构化参数")
    lyrics = build_lyrics(params["lyrics"], params["instrumental"])
    if not lyrics.strip():
        raise gr.Error("歌词为空:请输入歌词(纯器乐也需包含段落标签)")

    log = [f"[{datetime.datetime.now():%H:%M:%S}] 组装提示词完成,caption {len(caption)} 字符"]
    yield None, "", "\n".join(log), ""

    def cb(frac, msg):
        progress(frac, desc=msg)

    t0 = time.time()
    try:
        sr, waveform, saved, seed = inference.generate(
            caption=caption,
            lyrics=lyrics,
            audio_duration=float(kw["audio_duration"]),
            seed=int(kw["seed"]),
            num_inference_steps=int(kw["num_inference_steps"]),
            vram_mode=kw["vram_mode"],
            output_dir=OUTPUT_DIR,
            filename=f"music_{datetime.datetime.now():%Y%m%d_%H%M%S}_seed{abs(int(kw['seed']))}.wav"
            if int(kw["seed"]) < 0 else f"music_seed{int(kw['seed'])}.wav",
            progress_cb=cb,
        )
    except Exception as e:
        log.append(f"[错误] {e}")
        yield None, "", "\n".join(log), ""
        return

    elapsed = time.time() - t0
    log.append(f"生成完成:采样率 {sr} Hz,时长 {waveform.shape[0] / sr:.1f} 秒,耗时 {elapsed / 60:.1f} 分钟,seed={seed}")
    log.append(f"已保存: {saved}")
    yield (sr, waveform), os.path.basename(saved) if saved else "", "\n".join(log), caption


def build_ui():
    with gr.Blocks(title="MiniMax Music 3 音乐生成工作站") as demo:
        gr.Markdown(
            "# MiniMax Music 3 本地音乐生成工作站\n"
            "模型: **MiniMaxAI/MiniMax-Music3**(8B 全局 LLM + 0.6B 局部 LLM + Flow Matching 合成,"
            "输出 44.1kHz 立体声)。本机为低显存模式运行,生成速度较慢,请耐心等待。"
        )

        with gr.Row():
            with gr.Column(scale=5):
                gr.Markdown("### 一、歌词\n支持段落标签:`[Verse]` `[Chorus]` `[Bridge]` 等。**标签必须独占一行**,与标签同行的文字会被丢弃。")
                structure_dd = gr.Dropdown(list(SONG_STRUCTURES.keys()), label="插入曲式骨架")
                with gr.Row():
                    tag_btns = [gr.Button(tag, size="sm") for tag in SECTION_TAGS[:6]]
                with gr.Row():
                    tag_btns2 = [gr.Button(tag, size="sm") for tag in SECTION_TAGS[6:]]
                lyrics = gr.Textbox(DEFAULT_LYRICS, label="歌词", lines=12, max_lines=30)

            with gr.Column(scale=7):
                gr.Markdown("### 二、音乐描述")
                prompt_mode = gr.Radio(["结构化参数", "简单描述"], value="结构化参数", label="描述模式")

                simple_prompt = gr.Textbox(
                    "", label="简单描述(英文效果最佳,例如: A warm acoustic pop song with intimate female vocals...)",
                    visible=False, lines=3,
                    placeholder="A warm acoustic pop song with intimate female vocals, fingerpicked guitar and a gradual build into a wide chorus.")

                with gr.Group(visible=True) as structured_group:
                    preset_dd = gr.Dropdown(list(STYLE_PRESETS.keys()), label="一键风格预设")
                    with gr.Tab("全局元数据"):
                        genre = gr.Dropdown(list(GENRES.keys()), value=list(GENRES.keys())[0], label="流派")
                        subgenre = gr.Textbox("", label="子风格(自由填写,如 dream pop / trap / 古风)")
                        with gr.Row():
                            bpm_auto = gr.Checkbox(False, label="BPM 自动")
                            bpm = gr.Slider(40, 220, 100, step=1, label="BPM(速度)")
                        with gr.Row():
                            key = gr.Dropdown(KEY_OPTIONS, value="(自动)", label="调性")
                            scale = gr.Dropdown(SCALE_OPTIONS, value="(自动)", label="音阶")
                        emotional_arc = gr.Dropdown(["(不指定)"] + list(EMOTIONAL_ARCS.keys()), value="(不指定)", label="情绪推进")
                        with gr.Row():
                            scenario = gr.Dropdown(["(不指定)"] + list(SCENARIOS.keys()), value="(不指定)", label="聆听场景")
                            production = gr.Dropdown(["(不指定)"] + list(PRODUCTION_PROFILES.keys()), value="(不指定)", label="制作质感")

                    with gr.Tab("人声"):
                        vocal_gender = gr.Dropdown(list(VOCAL_GENDERS.keys()), value="女声", label="人声配置")
                        with gr.Row():
                            timbre = gr.Dropdown(NONE_OPTIONS[:1] + list(VOCAL_TIMBRES.keys()), value="(不指定)", label="音色")
                            register = gr.Dropdown(NONE_OPTIONS[:1] + list(VOCAL_REGISTERS.keys()), value="(不指定)", label="音域")
                        delivery = gr.Dropdown(NONE_OPTIONS[:1] + list(VOCAL_DELIVERIES.keys()), value="(不指定)", label="演唱风格")
                        with gr.Row():
                            harmony = gr.Dropdown(list(HARMONIES.keys()), value="无和声", label="和声")
                            backing_vocals = gr.Dropdown(list(BACKING_VOCALS.keys()), value="无伴唱", label="伴唱")
                        vocal_effect = gr.Dropdown(list(VOCAL_EFFECTS.keys()), value="无效果", label="人声效果")

                    with gr.Tab("编曲"):
                        primary_instruments = gr.CheckboxGroup(list(INSTRUMENTS.keys()), label="主奏乐器(可多选)")
                        secondary_instruments = gr.CheckboxGroup(list(INSTRUMENTS.keys()), label="辅奏/色彩乐器(可多选)")
                        with gr.Row():
                            groove = gr.Dropdown(["(不指定)"] + list(GROOVES.keys()), value="(不指定)", label="律动")
                            bass = gr.Dropdown(BASS_OPTIONS, value=BASS_OPTIONS[0], label="贝斯")
                        with gr.Row():
                            percussion = gr.Dropdown(["(不指定)"] + list(PERCUSSION_STYLES.keys()), value="(不指定)", label="打击乐")
                            spatial = gr.Dropdown(["(不指定)"] + list(SPATIAL_EFFECTS.keys()), value="(不指定)", label="空间效果")
                        textures = gr.CheckboxGroup(list(TEXTURES.keys()), label="质感层(可多选)")
                        arrangement_notes = gr.Textbox(
                            "", label="逐段编曲说明(可选,英文/中文均可)",
                            placeholder="例如: Intro 只有钢琴,Verse 加入指弹吉他,Chorus 全乐队进入,Bridge 抽掉鼓只留弦乐。")

            with gr.Column(scale=4):
                gr.Markdown("### 三、生成")
                with gr.Row():
                    audio_duration = gr.Slider(10, 360, 60, step=5, label="时长(秒,上限 6 分钟)")
                    num_inference_steps = gr.Slider(10, 60, 30, step=1, label="Flow Matching 步数")
                with gr.Row():
                    seed = gr.Number(-1, label="随机种子(-1 为随机)")
                    vram_mode = gr.Radio(["low", "standard"], value="low", label="显存模式")
                preview_btn = gr.Button("预览最终提示词")
                caption_preview = gr.Textbox("", label="最终 Caption 预览", lines=10, interactive=False)
                generate_btn = gr.Button("生成音乐", variant="primary", size="lg")
                audio_out = gr.Audio(label="生成结果", type="numpy")
                file_out = gr.Textbox("", label="保存文件", interactive=False)
                log_out = gr.Textbox("", label="运行日志", lines=6, interactive=False)

        all_inputs = [
            prompt_mode, simple_prompt, genre, subgenre, bpm_auto, bpm, key, scale,
            emotional_arc, scenario, production,
            vocal_gender, timbre, register, delivery, harmony, backing_vocals, vocal_effect,
            primary_instruments, secondary_instruments, groove, bass, percussion, textures,
            spatial, arrangement_notes, lyrics,
        ]

        def toggle_mode(mode):
            show_simple = mode == "简单描述"
            return gr.update(visible=show_simple), gr.update(visible=not show_simple)

        prompt_mode.change(toggle_mode, prompt_mode, [simple_prompt, structured_group])

        structured_outputs = [
            genre, subgenre, bpm_auto, bpm, key, scale, emotional_arc, scenario, production,
            vocal_gender, timbre, register, delivery, harmony, backing_vocals, vocal_effect,
            primary_instruments, secondary_instruments, groove, bass, percussion, textures, spatial,
        ]
        preset_dd.select(apply_preset, preset_dd, structured_outputs)
        structure_dd.select(insert_structure, structure_dd, lyrics)

        for btn in tag_btns + tag_btns2:
            btn.click(lambda lyr, t=btn.value: append_tag(lyr, t), lyrics, lyrics)

        preview_btn.click(
            lambda *vals: preview_caption(**dict(zip(COLLECT_KEYS, vals))),
            all_inputs, [caption_preview, log_out],
        )

        generate_btn.click(
            run_generate, all_inputs + [audio_duration, num_inference_steps, seed, vram_mode],
            [audio_out, file_out, log_out, caption_preview],
        )
    return demo


COLLECT_KEYS = [
    "prompt_mode", "simple_prompt", "genre", "subgenre", "bpm_auto", "bpm", "key", "scale",
    "emotional_arc", "scenario", "production",
    "vocal_gender", "timbre", "register", "delivery", "harmony", "backing_vocals", "vocal_effect",
    "primary_instruments", "secondary_instruments", "groove", "bass", "percussion", "textures",
    "spatial", "arrangement_notes", "lyrics",
]

GENERATE_KEYS = COLLECT_KEYS + ["audio_duration", "num_inference_steps", "seed", "vram_mode"]


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    demo = build_ui()
    demo.queue(max_size=4).launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
