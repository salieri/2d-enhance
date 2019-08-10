from dataclasses import field
from marshmallow_dataclass import dataclass

import marshmallow.validate

from typing import List, Optional

# https://pypi.org/project/marshmallow-dataclass/

@dataclass
class ConfigEffectReduceColorsColor:
    count: int = field(metadata={'validate': marshmallow.validate.Range(min=1, max=256)})
    chance: float = field(metadata={'validate': marshmallow.validate.Range(min=0.00000000001)}, default=1)

@dataclass
class ConfigEffectAngle:
    min: float = field(metadata={'validate': marshmallow.validate.Range(min=-360, max=360)})
    max: float = field(metadata={'validate': marshmallow.validate.Range(min=-360, max=360)})


@dataclass
class ConfigEffectAlpha:
    min: float = field(metadata={'validate': marshmallow.validate.Range(min=0, max=1)}, default=0.1)
    max: float = field(metadata={'validate': marshmallow.validate.Range(min=0, max=1)}, default=0.9)


@dataclass
class ConfigEffect:
    type: str = field(metadata={'validate': marshmallow.validate.OneOf(['grayscale', 'reduce_colors', 'rotate', 'translucency', 'outline'])})
    colors: Optional[List[ConfigEffectReduceColorsColor]] # reduce_colors
    angle: Optional[ConfigEffectAngle] # rotate
    alpha: Optional[ConfigEffectAlpha] # translucency
    chance: float = field(metadata={'validate': marshmallow.validate.Range(min=0.00000000001)}, default=1)


# @dataclass
# class ConfigEffectGrayscale(ConfigEffect):
#     type: str = field(metadata={'required': True, 'validate': marshmallow.validate.Equal('grayscale')})
#
#
# @dataclass
# class ConfigEffectReduceColors(ConfigEffect):
#     colors: List[ConfigEffectReduceColorsColor] = field(default_factory=lambda: [])
#     type: str = field(metadata={'validate': marshmallow.validate.Equal('reduce_colors')})


@dataclass
class ConfigEffectTranslucency(ConfigEffect):
    type: str = field(metadata={'required': True, 'validate': marshmallow.validate.Equal('translucency')})
    alpha: ConfigEffectAlpha = field(default_factory=lambda: {'min': 0.1, 'max': 0.9})


@dataclass
class ConfigSize:
    width: int = field(metadata={'validate': marshmallow.validate.Range(min=1)})
    height: int = field(metadata={'validate': marshmallow.validate.Range(min=1)})


@dataclass
class ConfigProcessorNativeSize:
    width: int = field(metadata={'validate': marshmallow.validate.Range(min=1)}, default=256)
    height: int = field(metadata={'validate': marshmallow.validate.Range(min=1)}, default=256)


@dataclass
class ConfigProcessorNative:
    size: ConfigProcessorNativeSize = field(default_factory=lambda: {})


@dataclass
class ConfigProcessor:
    native: ConfigProcessorNative = field(default_factory=lambda: {})


@dataclass
class ConfigOutputTarget:
    name: str = field(metadata={'validate': marshmallow.validate.Regexp('^[a-zA-Z0-9]+$')})
    format: str = field(metadata={'validate': marshmallow.validate.OneOf(['png', 'jpg'])}, default='png')
    mode: str = field(metadata={'validate': marshmallow.validate.OneOf(['RGBA', 'RGB', 'L'])}, default='RGBA')
    style: str = field(metadata={'validate': marshmallow.validate.OneOf(['cover', 'contain', 'clip'])}, default='cover')
    size: ConfigSize = field(default_factory=lambda: {'width': 256, 'height': 256})
    effects: List[ConfigEffect] = field(default_factory=lambda: [])


@dataclass
class ConfigOutput:
    targets: List[ConfigOutputTarget] = field(default_factory=lambda: [])


@dataclass
class ConfigContentGridSize:
    max: ConfigSize = field(default_factory=lambda: {'width': 4, 'height': 4})
    min: ConfigSize = field(default_factory=lambda: {'width': 1, 'height': 1})


@dataclass
class ConfigContentTypeDrawChances:
    clipping: float = field(default=0)
    resize: float = field(default=0)


@dataclass
class ConfigContentGrid:
    size: ConfigContentGridSize = field(default_factory=lambda: {})


@dataclass
class ConfigContentTypeShape:
    type: str = field(metadata={'validate': marshmallow.validate.OneOf(['triangle', 'hexagon', 'oval', 'line'])})
    chance: float = field(metadata={'validate': marshmallow.validate.Range(min=0.00000000001)}, default=1)


@dataclass
class ConfigContentType:
    type: str = field(metadata={'validate': marshmallow.validate.OneOf(['sprite', 'shape', 'text'])})
    shapes: Optional[List[ConfigContentTypeShape]] # shape
    characters: Optional[str] # text
    draw_chances: ConfigContentTypeDrawChances = field(default_factory=lambda: {})
    effects: List[ConfigEffect] = field(default_factory=lambda: [])
    chance: float = field(metadata={'validate': marshmallow.validate.Range(min=0.00000000001)}, default=1)


@dataclass
class ConfigContent:
    types: List[ConfigContentType]
    grid: ConfigContentGrid = field(default_factory=lambda: {})


@dataclass
class ConfigBackgroundType:
    type: str = field(metadata={'validate': marshmallow.validate.OneOf(['solid', 'transparent', 'bitmap', 'gradient', 'noise'])})
    colors: Optional[List[str]] # solid, gradient
    effects: List[ConfigEffect] = field(default_factory=lambda: [])
    chance: float = field(metadata={'validate': marshmallow.validate.Range(min=0.00000000001)}, default=1)


@dataclass
class ConfigBackground:
    types: List[ConfigBackgroundType] = field(default_factory=lambda: [{'type': 'transparent'}])


@dataclass
class Config:
    output: ConfigOutput
    content: ConfigContent
    background: ConfigBackground = field(default_factory=lambda: {})
    processor: ConfigProcessor = field(default_factory=lambda: {})

