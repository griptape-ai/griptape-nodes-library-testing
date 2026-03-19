"""Tests for AssertNumbers node."""

import pytest
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

from griptape_nodes_library_testing.assert_.assert_numbers import AssertNumbers


class TestAssertNumbers:
    @pytest.fixture
    def node(self, griptape_nodes: GriptapeNodes) -> AssertNumbers:  # noqa: ARG002
        return AssertNumbers(name="test_assert_numbers")

    # == operator
    def test_equal_passes(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 5
        node.parameter_values["operator"] = "=="
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_equal_fails(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 6
        node.parameter_values["operator"] = "=="
        with pytest.raises(AssertionError):
            node.process()

    # != operator
    def test_not_equal_passes(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 6
        node.parameter_values["operator"] = "!="
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_not_equal_fails(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 5
        node.parameter_values["operator"] = "!="
        with pytest.raises(AssertionError):
            node.process()

    # < operator
    def test_less_than_passes(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 3
        node.parameter_values["expected"] = 5
        node.parameter_values["operator"] = "<"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_less_than_fails(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 3
        node.parameter_values["operator"] = "<"
        with pytest.raises(AssertionError):
            node.process()

    # > operator
    def test_greater_than_passes(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 3
        node.parameter_values["operator"] = ">"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_greater_than_fails(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 3
        node.parameter_values["expected"] = 5
        node.parameter_values["operator"] = ">"
        with pytest.raises(AssertionError):
            node.process()

    # <= operator
    def test_less_than_or_equal_passes(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 5
        node.parameter_values["operator"] = "<="
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_less_than_or_equal_fails(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 6
        node.parameter_values["expected"] = 5
        node.parameter_values["operator"] = "<="
        with pytest.raises(AssertionError):
            node.process()

    # >= operator
    def test_greater_than_or_equal_passes(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 5
        node.parameter_values["operator"] = ">="
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_greater_than_or_equal_fails(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 4
        node.parameter_values["expected"] = 5
        node.parameter_values["operator"] = ">="
        with pytest.raises(AssertionError):
            node.process()

    def test_int_float_interop(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 5
        node.parameter_values["expected"] = 5.0
        node.parameter_values["operator"] = "=="
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_custom_message_on_failure(self, node: AssertNumbers) -> None:
        node.parameter_values["actual"] = 1
        node.parameter_values["expected"] = 2
        node.parameter_values["operator"] = "=="
        node.parameter_values["message"] = "numbers must match"
        with pytest.raises(AssertionError, match="numbers must match"):
            node.process()
