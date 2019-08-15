from marshmallow_dataclass import dataclass

@dataclass
class RunOpts:
    input: str
    output: str
    output_depth: int
    config: str
    samples: int
    show: bool
    skip_cache: bool

