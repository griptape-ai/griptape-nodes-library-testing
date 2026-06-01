"""TryCatchGroup Node - A group that catches child node failures and routes control flow."""

from __future__ import annotations

import logging
from typing import Any

from griptape_nodes.exe_types.core_types import (
    ControlParameterInput,
    ControlParameterOutput,
    Parameter,
    ParameterMode,
    ParameterTypeBuiltin,
)
from griptape_nodes.exe_types.node_groups.subflow_node_group import SubflowNodeGroup

logger = logging.getLogger("griptape_nodes")


class TryCatchGroup(SubflowNodeGroup):
    """Group node that catches exceptions from child nodes and routes to Succeeded/Failed.

    Place nodes inside this group. If any child node raises an exception during
    execution, the Failed control output fires and the error message is available
    on the error_message output. If all child nodes succeed, the Succeeded control
    output fires.

    Only RuntimeError is caught, because the engine's execute_subflow() wraps all
    child node exceptions in RuntimeError before re-raising.

    This converts any node into a SuccessFailureNode-like construct, useful for
    testing error handling in nodes that raise exceptions rather than using the
    SuccessFailureNode base class.
    """

    _execution_succeeded: bool | None

    def __init__(
        self,
        name: str,
        metadata: dict[Any, Any] | None = None,
    ) -> None:
        super().__init__(name, metadata)

        self._execution_succeeded = None

        self.control_parameter_in = ControlParameterInput()
        self.add_parameter(self.control_parameter_in)

        self.control_parameter_out = ControlParameterOutput(
            display_name="Succeeded",
            tooltip="Control path when the child nodes execute successfully",
        )
        self.add_parameter(self.control_parameter_out)

        self.failure_output = ControlParameterOutput(
            name="failure",
            display_name="Failed",
            tooltip="Control path when a child node raises an exception",
        )
        self.add_parameter(self.failure_output)

        self.error_message = Parameter(
            name="error_message",
            tooltip="The error message from the caught exception (empty on success)",
            type=ParameterTypeBuiltin.STR.value,
            allowed_modes={ParameterMode.OUTPUT},
            settable=False,
            default_value="",
        )
        self.add_parameter(self.error_message)

        if "right_parameters" not in self.metadata:
            self.metadata["right_parameters"] = []
        self.metadata["right_parameters"].extend(["exec_out", "failure", "error_message"])

    def get_next_control_output(self) -> Parameter | None:
        if self._execution_succeeded is None:
            self.stop_flow = True
            return None
        if self._execution_succeeded:
            return self.control_parameter_out
        return self.failure_output

    async def aprocess(self) -> None:
        self._execution_succeeded = None
        try:
            await self.execute_subflow()
            self._execution_succeeded = True
            self.parameter_output_values["error_message"] = ""
        except RuntimeError as e:
            self._execution_succeeded = False
            self.parameter_output_values["error_message"] = str(e)
            logger.info(
                "TryCatchGroup '%s': caught error from child nodes: %s",
                self.name,
                e,
            )

    def process(self) -> Any:
        pass
