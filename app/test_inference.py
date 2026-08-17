"""推理冒烟测试:加载管线并生成一小段音频验证全链路。"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import inference

LYRICS = """[Verse]
Morning light filtering through the pine
Every quiet street is yours and mine
[Chorus]
Softly the world begins to breathe"""

PROMPT = (
    "Genre: acoustic pop. BPM: 96. Key: C major. Warm and intimate, building gently into the chorus. "
    "Vocals: soft female lead, close and breathy, light stacked harmonies in the chorus. "
    "Arrangement: fingerpicked guitar and soft piano; brushed drums and upright bass enter in the chorus."
)


def main():
    duration = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
    t0 = time.time()

    def cb(frac, msg):
        print(f"[{time.time()-t0:7.1f}s] {int(frac*100):3d}% {msg}", flush=True)

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    sr, waveform, saved, seed = inference.generate(
        caption=PROMPT,
        lyrics=LYRICS,
        audio_duration=duration,
        seed=7,
        vram_mode="low",
        output_dir=out,
        filename="smoke_test.wav",
        progress_cb=cb,
    )
    print(f"采样率 {sr}, 时长 {waveform.shape[0]/sr:.1f}s, seed {seed}")
    print(f"保存于 {saved}")
    print(f"总耗时 {(time.time()-t0)/60:.1f} 分钟")


if __name__ == "__main__":
    main()
