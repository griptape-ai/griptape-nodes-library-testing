"""Tests for AssertEqual node."""

import pytest
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

from griptape_nodes_library_testing.assert_.assert_equal import AssertEqual


class TestAssertEqual:
    @pytest.fixture
    def node(self, griptape_nodes: GriptapeNodes) -> AssertEqual:  # noqa: ARG002
        return AssertEqual(name="test_assert_equal")

    def test_equal_values_succeed(self, node: AssertEqual) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = "hello"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_unequal_values_fail(self, node: AssertEqual) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = "world"
        with pytest.raises(AssertionError):
            node.process()
        assert node.parameter_output_values["was_successful"] is False

    def test_custom_message_on_failure(self, node: AssertEqual) -> None:
        node.parameter_values["actual"] = 1
        node.parameter_values["expected"] = 2
        node.parameter_values["message"] = "values must match"
        with pytest.raises(AssertionError, match="values must match"):
            node.process()

    def test_none_equality(self, node: AssertEqual) -> None:
        node.parameter_values["actual"] = None
        node.parameter_values["expected"] = None
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_none_not_equal_to_value(self, node: AssertEqual) -> None:
        node.parameter_values["actual"] = None
        node.parameter_values["expected"] = 0
        with pytest.raises(AssertionError):
            node.process()
