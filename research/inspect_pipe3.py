import inspect
import re

import diffusers.modular_pipelines.minimax_music3.modular_pipeline as mp
import diffusers.modular_pipelines.minimax_music3.encoders as enc
import diffusers.modular_pipelines.minimax_music3.denoise as dn

for name, mod in (("PIPE", mp), ("ENC", enc), ("DEN", dn)):
    src = inspect.getsource(mod)
    print(f"===== {name} =====")
    for i, line in enumerate(src.splitlines()):
        if re.search(r'ComponentSpec\(|language_model|num_inference_steps.*=|default', line):
            print(f"{i+1}: {line.strip()}")
