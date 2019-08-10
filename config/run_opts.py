from dataclasses import dataclass

@dataclass
class RunOpts:
    input: str
    output: str
    output_depth: int
    config: str
    samples: int

