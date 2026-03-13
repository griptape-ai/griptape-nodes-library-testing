from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import SuccessFailureNode


class AssertTrue(SuccessFailureNode):
    def __init__(self, name: str, metadata: dict[Any, Any] | None = None) -> None:
        super().__init__(name, metadata)

        self.add_parameter(
            Parameter(
                name="value",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                type="any",
                default_value=None,
                tooltip="The value to assert is truthy.",
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
        value = self.get_parameter_value("value")
        message = self.get_parameter_value("message")

        if bool(value):
            self._set_status_results(
                was_successful=True,
                result_details=f"Assertion passed: {value!r} is truthy",
            )
        else:
            details = f"Assertion failed: {value!r} is not truthy"
            if message:
                details = f"{message}: {details}"
            self._set_status_results(was_successful=False, result_details=details)
            self._handle_failure_exception(AssertionError(details))
