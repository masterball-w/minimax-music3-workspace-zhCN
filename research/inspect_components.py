import inspect

from diffusers.modular_pipelines import modular_pipeline as mp_mod

src = inspect.getsource(mp_mod)
lines = src.splitlines()
for i, l in enumerate(lines):
    if "def components" in l or "component_names" in l and "def" in l:
        print("\n".join(f"{j+1}: {lines[j]}" for j in range(max(0, i - 2), min(len(lines), i + 25))))
        print("-" * 40)
