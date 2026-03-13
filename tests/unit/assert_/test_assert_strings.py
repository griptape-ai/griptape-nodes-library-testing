"""Tests for AssertStrings node."""

import pytest
from griptape_nodes_library_testing.assert_.assert_strings import AssertStrings

from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes


class TestAssertStrings:
    @pytest.fixture
    def node(self, griptape_nodes: GriptapeNodes) -> AssertStrings:  # noqa: ARG002
        return AssertStrings(name="test_assert_strings")

    # == operator
    def test_equal_passes(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = "hello"
        node.parameter_values["operator"] = "=="
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_equal_fails(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = "world"
        node.parameter_values["operator"] = "=="
        with pytest.raises(AssertionError):
            node.process()

    # != operator
    def test_not_equal_passes(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = "world"
        node.parameter_values["operator"] = "!="
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_not_equal_fails(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = "hello"
        node.parameter_values["operator"] = "!="
        with pytest.raises(AssertionError):
            node.process()

    # contains operator
    def test_contains_passes(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello world"
        node.parameter_values["expected"] = "world"
        node.parameter_values["operator"] = "contains"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_contains_fails(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = "world"
        node.parameter_values["operator"] = "contains"
        with pytest.raises(AssertionError):
            node.process()

    # not contains operator
    def test_not_contains_passes(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = "world"
        node.parameter_values["operator"] = "not contains"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_not_contains_fails(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello world"
        node.parameter_values["expected"] = "world"
        node.parameter_values["operator"] = "not contains"
        with pytest.raises(AssertionError):
            node.process()

    # starts_with operator
    def test_starts_with_passes(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello world"
        node.parameter_values["expected"] = "hello"
        node.parameter_values["operator"] = "starts_with"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_starts_with_fails(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello world"
        node.parameter_values["expected"] = "world"
        node.parameter_values["operator"] = "starts_with"
        with pytest.raises(AssertionError):
            node.process()

    # ends_with operator
    def test_ends_with_passes(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello world"
        node.parameter_values["expected"] = "world"
        node.parameter_values["operator"] = "ends_with"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_ends_with_fails(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello world"
        node.parameter_values["expected"] = "hello"
        node.parameter_values["operator"] = "ends_with"
        with pytest.raises(AssertionError):
            node.process()

    # regex operator
    def test_regex_passes(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello123"
        node.parameter_values["expected"] = r"\d+"
        node.parameter_values["operator"] = "regex"
        node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_regex_fails(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "hello"
        node.parameter_values["expected"] = r"^\d+$"
        node.parameter_values["operator"] = "regex"
        with pytest.raises(AssertionError):
            node.process()

    def test_custom_message_on_failure(self, node: AssertStrings) -> None:
        node.parameter_values["actual"] = "foo"
        node.parameter_values["expected"] = "bar"
        node.parameter_values["operator"] = "=="
        node.parameter_values["message"] = "strings must match"
        with pytest.raises(AssertionError, match="strings must match"):
            node.process()
