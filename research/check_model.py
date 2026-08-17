import json
import os

root = r"d:\program\misc\make-music\models\MiniMax-Music3"

for comp in ["language_model", "transformer", "vocoder", "condition_encoder", "rvq_depth_decoder"]:
    d = os.path.join(root, comp)
    if not os.path.isdir(d):
        print(f"{comp}: MISSING DIR")
        continue
    files = [f for f in os.listdir(d) if not f.startswith(".")]
    total = sum(os.path.getsize(os.path.join(d, f)) for f in files) / 1024**3
    idx = os.path.join(d, "model.safetensors.index.json")
    expected = []
    if os.path.exists(idx):
        with open(idx) as f:
            expected = sorted(set(json.load(f)["weight_map"].values()))
    present = [f for f in files if f.endswith(".safetensors")]
    missing = [e for e in expected if e not in present]
    print(f"{comp}: {len(present)} shards present, {len(missing)} missing, {total:.2f} GB")
    for m in missing[:5]:
        print(f"   - {m}")
