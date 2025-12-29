"""Unit tests for InputHandler."""

import pytest
from unittest.mock import patch
from cli.input_handler import InputHandler


class TestGetMenuChoice:
    """Tests for get_menu_choice method."""

    @patch('builtins.input', return_value='1')
    def test_returns_one_for_valid_input(self, mock_input):
        """Should return 1 for valid input."""
        handler = InputHandler()
        result = handler.get_menu_choice()
        assert result == 1

    @patch('builtins.input', return_value='7')
    def test_returns_seven_for_valid_input(self, mock_input):
        """Should return 7 for valid input."""
        handler = InputHandler()
        result = handler.get_menu_choice()
        assert result == 7

    @patch('builtins.input', return_value='0')
    def test_returns_none_for_out_of_range_low(self, mock_input):
        """Should return None for input below range."""
        handler = InputHandler()
        result = handler.get_menu_choice()
        assert result is None

    @patch('builtins.input', return_value='8')
    def test_returns_none_for_out_of_range_high(self, mock_input):
        """Should return None for input above range."""
        handler = InputHandler()
        result = handler.get_menu_choice()
        assert result is None

    @patch('builtins.input', return_value='abc')
    def test_returns_none_for_non_numeric(self, mock_input):
        """Should return None for non-numeric input."""
        handler = InputHandler()
        result = handler.get_menu_choice()
        assert result is None

    @patch('builtins.input', return_value='  3  ')
    def test_accepts_whitespace_around_number(self, mock_input):
        """Should accept numbers with surrounding whitespace."""
        handler = InputHandler()
        result = handler.get_menu_choice()
        assert result == 3


class TestGetTaskId:
    """Tests for get_task_id method."""

    @patch('builtins.input', return_value='1')
    def test_returns_positive_id(self, mock_input):
        """Should return positive integer ID."""
        handler = InputHandler()
        result = handler.get_task_id("Enter ID: ")
        assert result == 1

    @patch('builtins.input', return_value='999')
    def test_returns_large_id(self, mock_input):
        """Should return large integer ID."""
        handler = InputHandler()
        result = handler.get_task_id("Enter ID: ")
        assert result == 999

    @patch('builtins.input', return_value='0')
    def test_returns_none_for_zero(self, mock_input):
        """Should return None for zero."""
        handler = InputHandler()
        result = handler.get_task_id("Enter ID: ")
        assert result is None

    @patch('builtins.input', return_value='-1')
    def test_returns_none_for_negative(self, mock_input):
        """Should return None for negative numbers."""
        handler = InputHandler()
        result = handler.get_task_id("Enter ID: ")
        assert result is None

    @patch('builtins.input', return_value='abc')
    def test_returns_none_for_non_numeric(self, mock_input):
        """Should return None for non-numeric input."""
        handler = InputHandler()
        result = handler.get_task_id("Enter ID: ")
        assert result is None


class TestGetTaskDescription:
    """Tests for get_task_description method."""

    @patch('builtins.input', return_value='Buy groceries')
    def test_returns_valid_description(self, mock_input):
        """Should return valid description."""
        handler = InputHandler()
        result = handler.get_task_description()
        assert result == "Buy groceries"

    @patch('builtins.input', return_value='')
    def test_returns_none_for_empty(self, mock_input):
        """Should return None for empty input."""
        handler = InputHandler()
        result = handler.get_task_description()
        assert result is None

    @patch('builtins.input', return_value='   ')
    def test_returns_none_for_whitespace_only(self, mock_input):
        """Should return None for whitespace-only input."""
        handler = InputHandler()
        result = handler.get_task_description()
        assert result is None

    @patch('builtins.input', return_value='  trimmed  ')
    def test_strips_whitespace(self, mock_input):
        """Should strip surrounding whitespace."""
        handler = InputHandler()
        result = handler.get_task_description()
        assert result == "trimmed"

    @patch('builtins.input', return_value='a' * 500)
    def test_accepts_max_length(self, mock_input):
        """Should accept description at max length (500)."""
        handler = InputHandler()
        result = handler.get_task_description()
        assert len(result) == 500

    @patch('builtins.input', return_value='a' * 501)
    def test_rejects_over_max_length(self, mock_input):
        """Should reject description over max length."""
        handler = InputHandler()
        result = handler.get_task_description()
        assert result is None
