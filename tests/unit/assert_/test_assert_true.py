"""Tests for AssertTrue node."""

import pytest
from griptape_nodes_library_testing.assert_.assert_true import AssertTrue

from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes


class TestAssertTrue:
    @pytest.fixture
    def node(self, griptape_nodes: GriptapeNodes) -> AssertTrue:  # noqa: ARG002
        return AssertTrue(name="test_assert_true")

    def test_true_value_succeeds(self, node: AssertTrue) -> None:
        node.parameter_values["value"] = True
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_truthy_string_succeeds(self, node: AssertTrue) -> None:
        node.parameter_values["value"] = "non-empty"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_truthy_number_succeeds(self, node: AssertTrue) -> None:
        node.parameter_values["value"] = 1
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_false_value_fails(self, node: AssertTrue) -> None:
        node.parameter_values["value"] = False
        with pytest.raises(AssertionError):
            node.process()
        assert node.parameter_output_values["was_successful"] is False

    def test_none_value_fails(self, node: AssertTrue) -> None:
        node.parameter_values["value"] = None
        with pytest.raises(AssertionError):
            node.process()

    def test_empty_string_fails(self, node: AssertTrue) -> None:
        node.parameter_values["value"] = ""
        with pytest.raises(AssertionError):
            node.process()

    def test_zero_fails(self, node: AssertTrue) -> None:
        node.parameter_values["value"] = 0
        with pytest.raises(AssertionError):
            node.process()

    def test_custom_message_on_failure(self, node: AssertTrue) -> None:
        node.parameter_values["value"] = False
        node.parameter_values["message"] = "expected truthy"
        with pytest.raises(AssertionError, match="expected truthy"):
            node.process()
