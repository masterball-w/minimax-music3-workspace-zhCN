import inspect

from diffusers import ComponentsManager

src = inspect.getsource(ComponentsManager)
lines = src.splitlines()
for i, l in enumerate(lines):
    if "def " in l or "lazy" in l.lower():
        print(f"{i+1}: {l}")
