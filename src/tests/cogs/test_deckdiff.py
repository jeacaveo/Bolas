""" Testing module for src.cogs.deckdiff. """
import unittest

from collections import defaultdict

from mock import (
    call,
    patch,
    )

from discord import Embed

from src.cogs.deckdiff import Diff


class TestDiff(unittest.TestCase):
    """ Non method specific tests for src.cogs.deckdiff.Diff. """

    @patch("src.cogs.deckdiff.re.compile")
    def test_init(self, re_mock):
        """ Test initial attributes. """
        # Given
        bot = "a bot"
        expected_angle_exp = "angle regexp"
        expected_line_exp = "line regexp"
        expected_skip_exp = "skip regexp"

        re_mock.side_effect = [
            expected_angle_exp,
            expected_line_exp,
            expected_skip_exp,
            ]

        # When
        obj = Diff(bot)

        # Then
        self.assertEqual(obj.bot, bot)
        self.assertEqual(len(obj.valid_urls), 2)
        self.assertEqual(
            obj.valid_urls["deckstats.net"]["query"],
            [("export_dec", "1")],
            )
        self.assertEqual(
            obj.valid_urls["tappedout.net"]["query"],
            [("fmt", "txt")],
            )
        self.assertEqual(obj.re_stripangle, expected_angle_exp)
        self.assertEqual(obj.re_line, expected_line_exp)
        self.assertEqual(obj.re_skip, expected_skip_exp)
        self.assertEqual(len(obj.name_replacements), 1)
        re_mock.assert_has_calls([
            call(r"^<(.*)>$"),
            call(
                r"^\s*(?:(?P<sb>SB:)\s)?\s*"
                r"(?P<count>[0-9]+)x?\s+(?P<name>.*?)\s*"
                r"(?:<[^>]*>\s*)*(?:#.*)?$"),
            call(r"^\s*(?:$|//)"),
            ])

    def test_message_error(self):
        """ Test MessageError sub class. """
        # Given
        expected_message = "error message"

        # When
        result = Diff.MessageError(expected_message)

        # Then
        self.assertEqual(result.message, expected_message)


class TestGetDiff(unittest.TestCase):
    """ Tests for src.cogs.deckdiff.Diff.get_diff. """

    def test_no_diff(self):
        """ Test when data provided has no difference. """
        # Given
        bot = "a bot"
        left = {"key1": 1}
        right = {"key1": 1}
        expected_result = ([], [], [], [])

        # When
        result = Diff(bot).get_diff(left, right)

        # Then
        self.assertEqual(result, expected_result)

    def test_all_diff(self):
        """ Test a scenario with all cases. """
        # Given
        bot = "a bot"
        left = {"key1": 1, "key2": 1, "key3": 3}
        right = {"key1": 1, "key2": 4, "key3": 1}
        expected_result = ([2], ["key3"], [3], ["key2"])

        # When
        result = Diff(bot).get_diff(left, right)

        # Then
        self.assertEqual(result, expected_result)
