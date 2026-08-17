import inspect

from diffusers.modular_pipelines import modular_pipeline as mp_mod

src = inspect.getsource(mp_mod)
lines = src.splitlines()
start = None
for i, l in enumerate(lines):
    if "def load_components" in l:
        start = i
        break
print("\n".join(f"{j+1}: {lines[j]}" for j in range(start, min(len(lines), start + 60))))
