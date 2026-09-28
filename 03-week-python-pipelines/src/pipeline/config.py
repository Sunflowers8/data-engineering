from dataclasses import dataclass


@dataclass
class PipelineConfig:
    input_path: str
    output_path: str
    sample_size: int