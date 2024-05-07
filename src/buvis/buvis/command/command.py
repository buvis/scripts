import yaml

from pathlib import Path
from buvis.adapters import ConfigAdapter, console

FILENAME_COMMAND_INPUT_SPECIFICATION = "command_input_spec.yaml"

class BuvisCommand:
    def _setattr_from_config(self, cfg: ConfigAdapter, child_module_path: str):
        input_spec_file = Path(child_module_path).parent.joinpath(FILENAME_COMMAND_INPUT_SPECIFICATION)

        with open(input_spec_file, "r") as input_spec_file:
            input_spec = yaml.safe_load(input_spec_file)

        for key, spec in input_spec.items():
            res = cfg.get_key_value(key)

            if res.is_ok():
                self.__setattr__(key, res.payload)
            else:
                if spec.get("panic"):
                    console.panic(key["panic"])
                elif spec.get("default"):
                    self.__setattr__(key, spec["default"])
