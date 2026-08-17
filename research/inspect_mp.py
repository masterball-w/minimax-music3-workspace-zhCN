import inspect

from diffusers.modular_pipelines.modular_pipeline import ModularPipeline

for name, member in inspect.getmembers(ModularPipeline):
    if name.startswith("_") or inspect.isclass(member):
        continue
    if inspect.isfunction(member) or isinstance(member, property):
        try:
            sig = inspect.signature(member) if inspect.isfunction(member) else ""
            print(f"{name}{sig}")
        except (ValueError, TypeError):
            print(name)
