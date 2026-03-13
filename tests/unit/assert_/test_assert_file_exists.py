"""Tests for AssertFileExists node."""

from pathlib import Path
from unittest.mock import patch

import pytest
from griptape_nodes_library_testing.assert_.assert_file_exists import AssertFileExists

from griptape_nodes.files.file import File, FileLoadError
from griptape_nodes.retained_mode.events.os_events import FileIOFailureReason
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes


class TestAssertFileExists:
    @pytest.fixture
    def node(self, griptape_nodes: GriptapeNodes) -> AssertFileExists:  # noqa: ARG002
        return AssertFileExists(name="test_assert_file_exists")

    def test_existing_file_passes(self, node: AssertFileExists) -> None:
        node.parameter_values["file_path"] = "/some/file.txt"
        with patch.object(File, "resolve", return_value="/some/file.txt"):
            with patch.object(Path, "exists", return_value=True):
                node.process()
        assert node.parameter_output_values["was_successful"] is True

    def test_missing_file_fails(self, node: AssertFileExists) -> None:
        node.parameter_values["file_path"] = "/missing/file.txt"
        with patch.object(File, "resolve", return_value="/missing/file.txt"):
            with patch.object(Path, "exists", return_value=False):
                with pytest.raises(AssertionError):
                    node.process()
        assert node.parameter_output_values["was_successful"] is False

    def test_macro_resolution_failure_fails(self, node: AssertFileExists) -> None:
        node.parameter_values["file_path"] = "{outputs}/file.txt"
        with patch.object(
            File,
            "resolve",
            side_effect=FileLoadError(FileIOFailureReason.INVALID_PATH, "no project loaded"),
        ):
            with pytest.raises(AssertionError):
                node.process()
        assert node.parameter_output_values["was_successful"] is False

    def test_custom_message_on_failure(self, node: AssertFileExists) -> None:
        node.parameter_values["file_path"] = "/missing/file.txt"
        node.parameter_values["message"] = "output file must exist"
        with patch.object(File, "resolve", return_value="/missing/file.txt"):
            with patch.object(Path, "exists", return_value=False):
                with pytest.raises(AssertionError, match="output file must exist"):
                    node.process()
