import inspect
import re

import diffusers.modular_pipelines.minimax_music3.before_denoise as bd
import diffusers.modular_pipelines.minimax_music3.denoise as dn
import diffusers.modular_pipelines.minimax_music3.encoders as enc

for name, mod in (("BEFORE_DENOISE", bd), ("ENCODERS", enc), ("DENOISE", dn)):
    src = inspect.getsource(mod)
    print(f"===== {name} =====")
    for i, line in enumerate(src.splitlines()):
        if re.search(r'audio_duration|max_new_tokens|num_inference_steps|num_frames|9000|25\.0|frame_rate|duration', line):
            print(f"{i+1}: {line.strip()}")
