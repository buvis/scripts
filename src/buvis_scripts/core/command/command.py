from pathlib import Path

import yaml
from buvis_scripts.core.adapters import ConfigAdapter, console

FILENAME_COMMAND_INPUT_SPECIFICATION = "command_input_spec.yaml"


class BuvisCommand:
    def _setattr_from_config(
        self: "BuvisCommand",
        cfg: ConfigAdapter,
        child_module_path: str,
    ) -> None:
        input_spec_file = Path(child_module_path).parent.joinpath(
            FILENAME_COMMAND_INPUT_SPECIFICATION,
        )

        with input_spec_file.open("r") as input_spec_file:
            input_spec = yaml.safe_load(input_spec_file)

        for key, spec in input_spec.items():
            res = cfg.get_configuration_item(key)

            if res.is_ok():
                self.__setattr__(key, res.payload)
            elif spec.get("panic"):
                console.panic(key["panic"])
            elif spec.get("default"):
                self.__setattr__(key, spec["default"])
