from pathlib import Path
from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import SuccessFailureNode
from griptape_nodes.files.file import File, FileLoadError


class AssertFileExists(SuccessFailureNode):
    def __init__(self, name: str, metadata: dict[Any, Any] | None = None) -> None:
        super().__init__(name, metadata)

        self.add_parameter(
            Parameter(
                name="file_path",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                type="any",
                default_value="",
                tooltip="The file path to check for existence. Supports project macros (e.g. {outputs}/result.txt).",
            )
        )
        self.add_parameter(
            Parameter(
                name="message",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                type="str",
                default_value="",
                tooltip="Optional custom message to include on assertion failure.",
            )
        )
        self._create_status_parameters(
            result_details_tooltip="Details about the assertion result.",
            result_details_placeholder="Details on the assertion will appear here.",
        )

    def process(self) -> None:
        self._clear_execution_status()
        file_path = self.get_parameter_value("file_path")
        message = self.get_parameter_value("message")

        try:
            resolved_path = File(file_path).resolve()
        except FileLoadError as e:
            details = f"Assertion failed: could not resolve path {file_path!r}: {e}"
            if message:
                details = f"{message}: {details}"
            self._set_status_results(was_successful=False, result_details=details)
            self._handle_failure_exception(AssertionError(details))
            return

        if Path(resolved_path).exists():
            self._set_status_results(
                was_successful=True,
                result_details=f"Assertion passed: file exists at {resolved_path!r}",
            )
        else:
            details = f"Assertion failed: no file found at {resolved_path!r}"
            if message:
                details = f"{message}: {details}"
            self._set_status_results(was_successful=False, result_details=details)
            self._handle_failure_exception(AssertionError(details))
