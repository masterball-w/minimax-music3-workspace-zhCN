"""MiniMax Music 3 巴洛克工作台后端(FastAPI)。

提供:GET /api/config 全部选项数据;POST /api/caption 提示词预览;
POST /api/generate SSE 流式推理进度;GET /api/outputs 历史音频。
复用 inference.py 的已验证推理链路与 presets.py 选项表。
"""

import datetime
import json
import os
import queue
import threading

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

import caption_builder
import inference
from presets import (
    GENRES, SCALES, KEYS, EMOTIONAL_ARCS, SCENARIOS, PRODUCTION_PROFILES,
    VOCAL_GENDERS, VOCAL_TIMBRES, VOCAL_REGISTERS, VOCAL_DELIVERIES,
    HARMONIES, BACKING_VOCALS, VOCAL_EFFECTS, INSTRUMENTS, GROOVES,
    PERCUSSION_STYLES, TEXTURES, SPATIAL_EFFECTS, SONG_STRUCTURES,
    STYLE_PRESETS, SECTION_TAGS,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT, "outputs")
WEB_DIR = os.path.join(ROOT, "web")

app = FastAPI(title="MiniMax Music 3 Baroque Workbench")

_gen_lock = threading.Lock()


@app.get("/api/config")
def get_config():
    return {
        "genres": GENRES,
        "scales": SCALES,
        "keys": KEYS,
        "emotional_arcs": EMOTIONAL_ARCS,
        "scenarios": SCENARIOS,
        "production_profiles": PRODUCTION_PROFILES,
        "vocal_genders": VOCAL_GENDERS,
        "vocal_timbres": VOCAL_TIMBRES,
        "vocal_registers": VOCAL_REGISTERS,
        "vocal_deliveries": VOCAL_DELIVERIES,
        "harmonies": HARMONIES,
        "backing_vocals": BACKING_VOCALS,
        "vocal_effects": VOCAL_EFFECTS,
        "instruments": INSTRUMENTS,
        "grooves": GROOVES,
        "percussion_styles": PERCUSSION_STYLES,
        "textures": TEXTURES,
        "spatial_effects": SPATIAL_EFFECTS,
        "song_structures": SONG_STRUCTURES,
        "style_presets": STYLE_PRESETS,
        "section_tags": SECTION_TAGS,
    }


def _collect(payload: dict) -> dict:
    instrumental = payload.get("vocal_gender") == "纯器乐(无人声)"
    subgenre = payload.get("subgenre") or ""
    bpm = None if payload.get("bpm_auto") else payload.get("bpm")
    return {
        "prompt_mode": "simple" if payload.get("prompt_mode") == "简单描述" else "structured",
        "simple_prompt": payload.get("simple_prompt", ""),
        "genre": payload.get("genre", ""),
        "subgenre": "" if subgenre in ("", "(不指定)") else subgenre,
        "bpm": None if bpm is None else int(bpm),
        "key": None if payload.get("key") in (None, "(自动)") else payload["key"],
        "scale": None if payload.get("scale") in (None, "(自动)") else payload["scale"],
        "emotional_arc": None if payload.get("emotional_arc") in (None, "(不指定)") else payload["emotional_arc"],
        "scenario": None if payload.get("scenario") in (None, "(不指定)") else payload["scenario"],
        "production": None if payload.get("production") in (None, "(不指定)") else payload["production"],
        "vocal_gender": payload.get("vocal_gender", "女声"),
        "vocal_timbre": None if payload.get("timbre") in (None, "(不指定)") else payload["timbre"],
        "vocal_register": None if payload.get("register") in (None, "(不指定)") else payload["register"],
        "vocal_delivery": None if payload.get("delivery") in (None, "(不指定)") else payload["delivery"],
        "harmony": None if payload.get("harmony") in (None, "(不指定)", "无和声") else payload["harmony"],
        "backing_vocals": None if payload.get("backing_vocals") in (None, "(不指定)", "无伴唱") else payload["backing_vocals"],
        "vocal_effect": None if payload.get("vocal_effect") in (None, "(不指定)", "无效果") else payload["vocal_effect"],
        "primary_instruments": payload.get("primary_instruments", []),
        "secondary_instruments": payload.get("secondary_instruments", []),
        "groove": None if payload.get("groove") in (None, "(不指定)") else payload["groove"],
        "bass": None if payload.get("bass") in (None, "(跟随主乐器自动)") else payload["bass"],
        "percussion": None if payload.get("percussion") in (None, "(不指定)") else payload["percussion"],
        "textures": payload.get("textures", []),
        "spatial": None if payload.get("spatial") in (None, "(不指定)") else payload["spatial"],
        "arrangement_notes": payload.get("arrangement_notes", ""),
        "lyrics": payload.get("lyrics", ""),
        "instrumental": instrumental,
    }


@app.post("/api/caption")
def preview_caption(payload: dict):
    params = _collect(payload)
    caption = caption_builder.build_caption(params)
    lyrics = caption_builder.build_lyrics(params["lyrics"], params["instrumental"])
    return {"caption": caption, "lyrics": lyrics}


@app.post("/api/generate")
def generate(payload: dict):
    params = _collect(payload)
    caption = caption_builder.build_caption(params)
    lyrics = caption_builder.build_lyrics(params["lyrics"], params["instrumental"])
    if not caption.strip():
        raise HTTPException(400, "提示词为空:请填写自由描述,或选择结构化参数")
    if not lyrics.strip():
        raise HTTPException(400, "歌词为空:请输入歌词(纯器乐也需要包含段落标签)")

    duration = float(payload.get("audio_duration", 60))
    seed = int(payload.get("seed", -1))
    steps = int(payload.get("num_inference_steps", 30))
    vram_mode = payload.get("vram_mode", "low")

    if seed < 0:
        filename = f"music_{datetime.datetime.now():%Y%m%d_%H%M%S}_rand.wav"
    else:
        filename = f"music_seed{seed}_{datetime.datetime.now():%Y%m%d_%H%M%S}.wav"

    q: queue.Queue = queue.Queue()

    def emit(obj):
        q.put(obj)

    def worker():
        try:
            if not _gen_lock.acquire(blocking=False):
                emit({"type": "error", "message": "已有生成任务正在进行,请等待完成"})
                return

            def cb(frac, msg):
                emit({"type": "progress", "frac": frac, "message": msg})

            sr, waveform, saved, used_seed = inference.generate(
                caption=caption,
                lyrics=lyrics,
                audio_duration=duration,
                seed=seed,
                num_inference_steps=steps,
                vram_mode=vram_mode,
                output_dir=OUTPUT_DIR,
                filename=filename,
                progress_cb=cb,
            )
            emit({
                "type": "result",
                "sample_rate": sr,
                "duration": round(waveform.shape[0] / sr, 2),
                "seed": used_seed,
                "file": os.path.basename(saved) if saved else None,
                "url": f"/audio/{os.path.basename(saved)}" if saved else None,
            })
        except Exception as e:
            emit({"type": "error", "message": str(e)})
        finally:
            try:
                _gen_lock.release()
            except RuntimeError:
                pass
            emit(None)

    def stream():
        emit({"type": "log", "message": f"提示词组装完成,caption {len(caption)} 字符"})
        threading.Thread(target=worker, daemon=True).start()
        while True:
            item = q.get()
            if item is None:
                break
            yield f"data: {json.dumps(item, ensure_ascii=False)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/api/outputs")
def list_outputs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    items = []
    for f in sorted(os.listdir(OUTPUT_DIR), reverse=True):
        if not f.lower().endswith(".wav"):
            continue
        p = os.path.join(OUTPUT_DIR, f)
        st = os.stat(p)
        items.append({
            "file": f,
            "url": f"/audio/{f}",
            "size_mb": round(st.st_size / 1024**2, 2),
            "mtime": datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        })
    return items


@app.get("/api/outputs/{name}")
def download_output(name: str):
    safe = os.path.basename(name)
    p = os.path.join(OUTPUT_DIR, safe)
    if not os.path.isfile(p):
        raise HTTPException(404, "文件不存在")
    return FileResponse(p, filename=safe, media_type="audio/wav")


os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/audio", StaticFiles(directory=OUTPUT_DIR), name="audio")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7861, log_level="info")
