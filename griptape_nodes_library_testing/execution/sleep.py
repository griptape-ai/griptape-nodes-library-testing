import asyncio
from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import SuccessFailureNode


class Sleep(SuccessFailureNode):
    """Holds execution for a configurable number of seconds.

    Exists so tests can make a run take real time: concurrency and admission
    tests need one artist's run to still be in flight while another artist
    asks -- an instant node cannot demonstrate queueing.
    """

    def __init__(self, name: str, metadata: dict[Any, Any] | None = None) -> None:
        super().__init__(name, metadata)

        self.add_parameter(
            Parameter(
                name="seconds",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                type="float",
                default_value=1.0,
                tooltip="How long to sleep before completing, in seconds.",
            )
        )
        self._create_status_parameters(
            result_details_tooltip="Details about the completed sleep.",
            result_details_placeholder="Details on the sleep will appear here.",
        )

    async def aprocess(self) -> None:
        self._clear_execution_status()
        seconds = float(self.get_parameter_value("seconds") or 0.0)
        await asyncio.sleep(seconds)
        self._set_status_results(
            was_successful=True,
            result_details=f"Slept for {seconds} seconds",
        )
