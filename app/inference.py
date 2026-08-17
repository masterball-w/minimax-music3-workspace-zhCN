"""MiniMax Music 3 推理封装:懒加载管线、低显存 CPU offload、同步生成。"""

import os
import threading

import torch

MODEL_PATH_ENV = "MINIMAX_MUSIC3_PATH"

_lock = threading.Lock()
_state = {"pipe": None, "loading": False}


def default_model_path():
    env = os.environ.get(MODEL_PATH_ENV)
    if env:
        return env
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "models", "MiniMax-Music3")


def is_loaded():
    return _state["pipe"] is not None


def get_pipe(vram_mode="low", progress_cb=None):
    """加载管线。vram_mode:
    - "low": auto cpu offload + 语言模型逐层流式 offload,适配 8-12GB 显存
    - "standard": 仅 auto cpu offload,适配 22GB+ 显存
    """
    with _lock:
        if _state["pipe"] is not None:
            return _state["pipe"]
        if _state["loading"]:
            raise RuntimeError("模型正在加载中,请等待当前任务完成")
        _state["loading"] = True
    try:
        from diffusers import ComponentsManager, ModularPipeline
        from diffusers.hooks import apply_group_offloading

        model_path = default_model_path()
        if not os.path.isdir(model_path):
            raise FileNotFoundError(f"模型目录不存在: {model_path},请先完成权重下载")

        if progress_cb:
            progress_cb(0.05, "正在加载模型组件,首次加载约需数分钟...")
        manager = ComponentsManager()
        manager.enable_auto_cpu_offload(device="cuda")
        pipe = ModularPipeline.from_pretrained(model_path, components_manager=manager)
        pipe.load_components(dtype=torch.bfloat16)

        missing = [n for n in ("language_model", "transformer", "condition_encoder",
                               "vocoder", "rvq_depth_decoder", "tokenizer", "scheduler")
                   if getattr(pipe, n, None) is None]
        if missing:
            raise RuntimeError(f"组件加载失败: {missing},请检查 modular_model_index.json 中的组件路径")

        if vram_mode == "low":
            if progress_cb:
                progress_cb(0.5, "正在配置低显存逐层加载(首次约需数分钟)...")
            # low_cpu_mem_usage=True:跳过 pin_memory(),否则 pin 全部权重需复制
            # 等量系统内存并计入 WDDM 显存 commit,cudaHostAlloc 失败会被误报为 CUDA OOM
            apply_group_offloading(
                pipe.language_model,
                onload_device=torch.device("cuda"),
                offload_type="leaf_level",
                use_stream=True,
                low_cpu_mem_usage=True,
            )
            # transformer(Flow Matching 主力)按块搬运,避免整体驻留 GPU 导致生成阶段 OOM
            apply_group_offloading(
                pipe.transformer,
                onload_device=torch.device("cuda"),
                offload_type="block_level",
                num_blocks_per_group=1,
                use_stream=True,
                low_cpu_mem_usage=True,
            )
        with _lock:
            _state["pipe"] = pipe
            _state["loading"] = False
        return pipe
    except Exception:
        with _lock:
            _state["loading"] = False
        raise


def generate(caption, lyrics, audio_duration=60.0, seed=-1, num_inference_steps=30,
             vram_mode="low", output_dir=None, filename=None, progress_cb=None):
    """执行推理,返回 (sample_rate, waveform[frames, channels], 保存路径, seed)。

    caption: 音乐描述(英文效果最佳);lyrics: 歌词(段落标签独占一行)。
    """
    pipe = get_pipe(vram_mode=vram_mode, progress_cb=progress_cb)

    if progress_cb:
        progress_cb(0.55, "模型加载完成,开始生成音频(低显存模式速度较慢,请耐心等待)...")

    if seed is None or seed < 0:
        seed = int(torch.randint(0, 2**31 - 1, (1,)).item())
    generator = torch.Generator("cuda").manual_seed(int(seed))

    try:
        result = pipe(
            prompt=caption,
            lyrics=lyrics,
            audio_duration=float(audio_duration),
            num_inference_steps=int(num_inference_steps),
            generator=generator,
            output="audios",
        )
    except torch.cuda.OutOfMemoryError:
        # OOM 后显存上下文已损坏,必须卸载管线,下次生成重新加载
        unload()
        raise RuntimeError("CUDA 显存不足:请缩短生成时长,或关闭占用显存的程序后重试")
    audio = result[0]
    if isinstance(audio, torch.Tensor):
        audio = audio.float().cpu().numpy()

    waveform = audio[0].T if audio.ndim == 3 else audio.T
    sr = pipe.sampling_rate

    saved_path = None
    if output_dir:
        import soundfile as sf
        os.makedirs(output_dir, exist_ok=True)
        name = filename or f"music_seed{seed}.wav"
        saved_path = os.path.join(output_dir, name)
        sf.write(saved_path, waveform, sr)

    if progress_cb:
        progress_cb(1.0, "生成完成")
    return sr, waveform, saved_path, seed


def unload():
    """释放显存。"""
    with _lock:
        if _state["pipe"] is not None:
            del _state["pipe"]
            _state["pipe"] = None
        torch.cuda.empty_cache()
