from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import SuccessFailureNode
from griptape_nodes.traits.options import Options


class AssertNumbers(SuccessFailureNode):
    OPERATORS = ["==", "!=", "<", ">", "<=", ">="]

    def __init__(self, name: str, metadata: dict[Any, Any] | None = None) -> None:
        super().__init__(name, metadata)

        self.add_parameter(
            Parameter(
                name="actual",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                type="float",
                default_value=0,
                tooltip="The actual numeric value.",
            )
        )
        self.add_parameter(
            Parameter(
                name="expected",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                type="float",
                default_value=0,
                tooltip="The expected numeric value.",
            )
        )
        self.add_parameter(
            Parameter(
                name="operator",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                type="str",
                default_value="==",
                tooltip="The comparison operator to apply.",
                traits={Options(choices=self.OPERATORS)},
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

    def _evaluate(self, actual: float, expected: float, operator: str) -> bool:
        match operator:
            case "==":
                return actual == expected
            case "!=":
                return actual != expected
            case "<":
                return actual < expected
            case ">":
                return actual > expected
            case "<=":
                return actual <= expected
            case ">=":
                return actual >= expected
            case _:
                msg = f"Unknown operator: {operator!r}"
                raise ValueError(msg)

    def process(self) -> None:
        self._clear_execution_status()
        actual = self.get_parameter_value("actual")
        expected = self.get_parameter_value("expected")
        operator = self.get_parameter_value("operator")
        message = self.get_parameter_value("message")

        if self._evaluate(actual, expected, operator):
            self._set_status_results(
                was_successful=True,
                result_details=f"Assertion passed: {actual} {operator} {expected}",
            )
        else:
            details = f"Assertion failed: {actual} {operator} {expected}"
            if message:
                details = f"{message}: {details}"
            self._set_status_results(was_successful=False, result_details=details)
            self._handle_failure_exception(AssertionError(details))
