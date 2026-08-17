import inspect
import re

import diffusers.modular_pipelines.minimax_music3.denoise as dn
import diffusers.modular_pipelines.minimax_music3.decoders as dc
from diffusers import ModularPipeline

pat = re.compile(r'InputParam\(\s*\n?\s*"[^"]+"|audio_duration[^\n,)]*|num_frames[^\n,)]*|max_frames[^\n,)]*|generator[^\n,)]*|output[^\n,)]*')

for name, mod in (("DENOISE", dn), ("DECODER", dc)):
    src = inspect.getsource(mod)
    print(f"===== {name} =====")
    for m in pat.findall(src)[:25]:
        print(m.strip())

print("===== ModularPipeline.__call__ =====")
sig = inspect.signature(ModularPipeline.__call__)
print(sig)
