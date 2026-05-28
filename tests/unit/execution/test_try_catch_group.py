"""Tests for TryCatchGroup node."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from griptape_nodes.exe_types.core_types import ParameterMode, ParameterTypeBuiltin
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

from griptape_nodes_library_testing.execution.try_catch_group import TryCatchGroup


class TestTryCatchGroup:
    @pytest.fixture
    def node(self, griptape_nodes: GriptapeNodes) -> TryCatchGroup:  # noqa: ARG002
        return TryCatchGroup(name="test_try_catch")

    def test_init_has_control_input(self, node: TryCatchGroup) -> None:
        param = node.get_parameter_by_name("exec_in")
        assert param is not None
        assert param.output_type == ParameterTypeBuiltin.CONTROL_TYPE.value

    def test_init_has_succeeded_output(self, node: TryCatchGroup) -> None:
        param = node.get_parameter_by_name("exec_out")
        assert param is not None
        assert param.output_type == ParameterTypeBuiltin.CONTROL_TYPE.value

    def test_init_has_failed_output(self, node: TryCatchGroup) -> None:
        param = node.get_parameter_by_name("failure")
        assert param is not None
        assert param.output_type == ParameterTypeBuiltin.CONTROL_TYPE.value

    def test_init_has_error_message_output(self, node: TryCatchGroup) -> None:
        param = node.get_parameter_by_name("error_message")
        assert param is not None
        assert param.type == ParameterTypeBuiltin.STR.value
        assert param.allowed_modes == {ParameterMode.OUTPUT}
        assert param.default_value == ""

    def test_get_next_control_output_before_execution(self, node: TryCatchGroup) -> None:
        result = node.get_next_control_output()
        assert result is None
        assert node.stop_flow is True

    @pytest.mark.asyncio
    async def test_subflow_success_sets_succeeded(self, node: TryCatchGroup) -> None:
        with patch.object(node, "execute_subflow", new_callable=AsyncMock):
            await node.aprocess()

        assert node._execution_succeeded is True
        assert node.parameter_output_values["error_message"] == ""
        assert node.get_next_control_output() is node.control_parameter_out

    @pytest.mark.asyncio
    async def test_subflow_failure_sets_failed(self, node: TryCatchGroup) -> None:
        with patch.object(node, "execute_subflow", new_callable=AsyncMock, side_effect=RuntimeError("something broke")):
            await node.aprocess()

        assert node._execution_succeeded is False
        assert node.parameter_output_values["error_message"] == "something broke"
        assert node.get_next_control_output() is node.failure_output

    @pytest.mark.asyncio
    async def test_error_message_cleared_on_success_after_failure(self, node: TryCatchGroup) -> None:
        with patch.object(node, "execute_subflow", new_callable=AsyncMock, side_effect=RuntimeError("first error")):
            await node.aprocess()
        assert node.parameter_output_values["error_message"] == "first error"

        with patch.object(node, "execute_subflow", new_callable=AsyncMock):
            await node.aprocess()
        assert node.parameter_output_values["error_message"] == ""
        assert node._execution_succeeded is True

    def test_right_parameters_include_failure_and_error_message(self, node: TryCatchGroup) -> None:
        right_params = node.metadata.get("right_parameters", [])
        assert "exec_out" in right_params
        assert "failure" in right_params
        assert "error_message" in right_params
