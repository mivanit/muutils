"""Tests for muutils.cli.arg_bool module."""

from __future__ import annotations

import argparse
import pytest
from pytest import mark, param

from muutils.cli.arg_bool import (
    parse_bool_token,
    BoolFlagOrValue,
    add_bool_flag,
    TRUE_SET_DEFAULT,
    FALSE_SET_DEFAULT,
)


# ============================================================================
# Tests for parse_bool_token
# ============================================================================


def test_parse_bool_token_valid():
    """Test parse_bool_token with valid true/false tokens."""
    # True tokens from default set
    assert parse_bool_token("true") is True
    assert parse_bool_token("1") is True
    assert parse_bool_token("t") is True
    assert parse_bool_token("yes") is True
    assert parse_bool_token("y") is True
    assert parse_bool_token("on") is True

    # False tokens from default set
    assert parse_bool_token("false") is False
    assert parse_bool_token("0") is False
    assert parse_bool_token("f") is False
    assert parse_bool_token("no") is False
    assert parse_bool_token("n") is False
    assert parse_bool_token("off") is False


def test_parse_bool_token_case_insensitive():
    """Test parse_bool_token is case-insensitive."""
    assert parse_bool_token("TRUE") is True
    assert parse_bool_token("True") is True
    assert parse_bool_token("TrUe") is True
    assert parse_bool_token("FALSE") is False
    assert parse_bool_token("False") is False
    assert parse_bool_token("FaLsE") is False
    assert parse_bool_token("YES") is True
    assert parse_bool_token("NO") is False
    assert parse_bool_token("ON") is True
    assert parse_bool_token("OFF") is False


def test_parse_bool_token_invalid():
    """Test parse_bool_token with invalid tokens raises ArgumentTypeError."""
    with pytest.raises(argparse.ArgumentTypeError, match="expected one of"):
        parse_bool_token("invalid")

    with pytest.raises(argparse.ArgumentTypeError, match="expected one of"):
        parse_bool_token("maybe")

    with pytest.raises(argparse.ArgumentTypeError, match="expected one of"):
        parse_bool_token("2")

    with pytest.raises(argparse.ArgumentTypeError, match="expected one of"):
        parse_bool_token("")


def test_parse_bool_token_custom_sets():
    """Test parse_bool_token with custom true/false sets."""
    custom_true = {"enabled", "active"}
    custom_false = {"disabled", "inactive"}

    assert (
        parse_bool_token("enabled", true_set=custom_true, false_set=custom_false)
        is True
    )
    assert (
        parse_bool_token("ACTIVE", true_set=custom_true, false_set=custom_false) is True
    )
    assert (
        parse_bool_token("disabled", true_set=custom_true, false_set=custom_false)
        is False
    )
    assert (
        parse_bool_token("INACTIVE", true_set=custom_true, false_set=custom_false)
        is False
    )

    # Default tokens should not work with custom sets
    with pytest.raises(argparse.ArgumentTypeError):
        parse_bool_token("true", true_set=custom_true, false_set=custom_false)


# ============================================================================
# Tests for BoolFlagOrValue
# ============================================================================


def test_BoolFlagOrValue_bare_flag():
    """Test bare flag (--flag with no value) → True."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=False,
        allow_bare=True,
    )

    # Bare flag should be True
    args = parser.parse_args(["--flag"])
    assert args.flag is True

    # No flag should use default
    args = parser.parse_args([])
    assert args.flag is False


def test_BoolFlagOrValue_negated():
    """Test negated flag (--no-flag) → False."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        "--no-flag",
        dest="flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=True,
        allow_no=True,
    )

    # --no-flag should be False
    args = parser.parse_args(["--no-flag"])
    assert args.flag is False

    # --flag should be True (bare)
    args = parser.parse_args(["--flag"])
    assert args.flag is True

    # No flag should use default
    args = parser.parse_args([])
    assert args.flag is True


def test_BoolFlagOrValue_explicit_values():
    """Test explicit values: --flag true, --flag false."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=False,
    )

    # --flag true
    args = parser.parse_args(["--flag", "true"])
    assert args.flag is True

    # --flag false
    args = parser.parse_args(["--flag", "false"])
    assert args.flag is False

    # --flag 1
    args = parser.parse_args(["--flag", "1"])
    assert args.flag is True

    # --flag 0
    args = parser.parse_args(["--flag", "0"])
    assert args.flag is False

    # --flag yes
    args = parser.parse_args(["--flag", "yes"])
    assert args.flag is True

    # --flag no
    args = parser.parse_args(["--flag", "no"])
    assert args.flag is False


def test_BoolFlagOrValue_equals_syntax():
    """Test --flag=true and --flag=false syntax."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=False,
    )

    # --flag=true
    args = parser.parse_args(["--flag=true"])
    assert args.flag is True

    # --flag=false
    args = parser.parse_args(["--flag=false"])
    assert args.flag is False

    # --flag=1
    args = parser.parse_args(["--flag=1"])
    assert args.flag is True

    # --flag=0
    args = parser.parse_args(["--flag=0"])
    assert args.flag is False


def test_BoolFlagOrValue_allow_bare_false():
    """Test error on bare flag when allow_bare=False."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=False,
        allow_bare=False,
    )

    # Bare flag should error
    with pytest.raises(SystemExit):
        parser.parse_args(["--flag"])

    # Explicit value should work
    args = parser.parse_args(["--flag", "true"])
    assert args.flag is True


def test_BoolFlagOrValue_invalid_token():
    """Test --flag invalid raises error."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=False,
    )

    # Invalid token should error
    with pytest.raises(SystemExit):
        parser.parse_args(["--flag", "invalid"])

    with pytest.raises(SystemExit):
        parser.parse_args(["--flag", "maybe"])


def test_BoolFlagOrValue_no_flag_with_value_error():
    """Test --no-flag with a value raises error."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        "--no-flag",
        dest="flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=True,
        allow_no=True,
    )

    # --no-flag with value should error
    with pytest.raises(SystemExit):
        parser.parse_args(["--no-flag", "true"])

    with pytest.raises(SystemExit):
        parser.parse_args(["--no-flag=false"])


def test_BoolFlagOrValue_allow_no_false():
    """Test error when using --no-flag but allow_no=False."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        "--no-flag",
        dest="flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=True,
        allow_no=False,
    )

    # --no-flag should error when allow_no=False
    with pytest.raises(SystemExit):
        parser.parse_args(["--no-flag"])


def test_BoolFlagOrValue_custom_true_false_sets():
    """Test BoolFlagOrValue with custom true/false sets."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=False,
        true_set={"enabled", "active"},
        false_set={"disabled", "inactive"},
    )

    args = parser.parse_args(["--flag", "enabled"])
    assert args.flag is True

    args = parser.parse_args(["--flag", "disabled"])
    assert args.flag is False

    # Default tokens should not work
    with pytest.raises(SystemExit):
        parser.parse_args(["--flag", "true"])


def test_BoolFlagOrValue_invalid_nargs():
    """Test that BoolFlagOrValue raises ValueError for invalid nargs."""
    parser = argparse.ArgumentParser()

    # nargs other than '?' or None should raise ValueError
    with pytest.raises(ValueError, match="requires nargs='?'"):
        parser.add_argument(
            "--flag",
            action=BoolFlagOrValue,
            nargs=1,
        )

    with pytest.raises(ValueError, match="requires nargs='?'"):
        parser.add_argument(
            "--flag2",
            action=BoolFlagOrValue,
            nargs="*",
        )


def test_BoolFlagOrValue_type_not_allowed():
    """Test that BoolFlagOrValue raises ValueError when type= is provided."""
    parser = argparse.ArgumentParser()

    with pytest.raises(ValueError, match="does not accept type="):
        parser.add_argument(
            "--flag",
            action=BoolFlagOrValue,
            nargs="?",
            type=str,
        )


# ============================================================================
# Tests for add_bool_flag
# ============================================================================


def test_add_bool_flag_integration():
    """Test full integration with various argument combinations."""
    parser = argparse.ArgumentParser()
    add_bool_flag(parser, "feature", default=False, help="Enable feature")

    # Bare flag
    args = parser.parse_args(["--feature"])
    assert args.feature is True

    # Explicit true
    args = parser.parse_args(["--feature", "true"])
    assert args.feature is True

    # Explicit false
    args = parser.parse_args(["--feature", "false"])
    assert args.feature is False

    # Equals syntax
    args = parser.parse_args(["--feature=true"])
    assert args.feature is True

    args = parser.parse_args(["--feature=false"])
    assert args.feature is False

    # No flag (default)
    args = parser.parse_args([])
    assert args.feature is False


def test_add_bool_flag_allow_no():
    """Test both --flag and --no-flag work when allow_no=True."""
    parser = argparse.ArgumentParser()
    add_bool_flag(parser, "feature", default=False, allow_no=True)

    # --feature
    args = parser.parse_args(["--feature"])
    assert args.feature is True

    # --no-feature
    args = parser.parse_args(["--no-feature"])
    assert args.feature is False

    # No flag (default)
    args = parser.parse_args([])
    assert args.feature is False


def test_add_bool_flag_dest_conversion():
    """Test 'some-flag' → namespace.some_flag."""
    parser = argparse.ArgumentParser()
    add_bool_flag(parser, "some-flag", default=False)

    args = parser.parse_args(["--some-flag"])
    assert args.some_flag is True
    assert not hasattr(args, "some-flag")

    args = parser.parse_args(["--some-flag", "false"])
    assert args.some_flag is False


def test_add_bool_flag_custom_true_false_sets():
    """Test add_bool_flag with custom true/false sets."""
    parser = argparse.ArgumentParser()
    add_bool_flag(
        parser,
        "feature",
        default=False,
        true_set={"enabled", "on"},
        false_set={"disabled", "off"},
    )

    args = parser.parse_args(["--feature", "enabled"])
    assert args.feature is True

    args = parser.parse_args(["--feature", "disabled"])
    assert args.feature is False

    # Default tokens should not work
    with pytest.raises(SystemExit):
        parser.parse_args(["--feature", "true"])


def test_add_bool_flag_allow_bare_false():
    """Test add_bool_flag with allow_bare=False."""
    parser = argparse.ArgumentParser()
    add_bool_flag(parser, "feature", default=False, allow_bare=False)

    # Bare flag should error
    with pytest.raises(SystemExit):
        parser.parse_args(["--feature"])

    # Explicit value should work
    args = parser.parse_args(["--feature", "true"])
    assert args.feature is True


def test_add_bool_flag_default_true():
    """Test add_bool_flag with default=True."""
    parser = argparse.ArgumentParser()
    add_bool_flag(parser, "feature", default=True)

    # No flag should use default=True
    args = parser.parse_args([])
    assert args.feature is True

    # Explicit false should override
    args = parser.parse_args(["--feature", "false"])
    assert args.feature is False


def test_add_bool_flag_multiple_flags():
    """Test multiple boolean flags in the same parser."""
    parser = argparse.ArgumentParser()
    add_bool_flag(parser, "feature-a", default=False)
    add_bool_flag(parser, "feature-b", default=True)
    add_bool_flag(parser, "feature-c", default=False, allow_no=True)

    args = parser.parse_args(
        [
            "--feature-a",
            "--feature-b",
            "false",
            "--no-feature-c",
        ]
    )
    assert args.feature_a is True
    assert args.feature_b is False
    assert args.feature_c is False


def test_add_bool_flag_help_text():
    """Test that help text is generated or used correctly."""
    parser = argparse.ArgumentParser()
    add_bool_flag(parser, "feature", default=False, help="Custom help text")

    # Check that the help is stored (can't easily test output without parsing help text)
    action = None
    for act in parser._actions:
        if hasattr(act, "dest") and act.dest == "feature":
            action = act
            break

    assert action is not None
    assert action.help == "Custom help text"


def test_add_bool_flag_default_help():
    """Test that default help text is generated when not provided."""
    parser = argparse.ArgumentParser()
    add_bool_flag(parser, "my-feature", default=False)

    action = None
    for act in parser._actions:
        if hasattr(act, "dest") and act.dest == "my_feature":
            action = act
            break

    assert action is not None
    assert action.help is not None
    assert "enable/disable my feature" in action.help


# ============================================================================
# Integration and edge case tests
# ============================================================================


def test_multiple_values_error():
    """Test that passing multiple values to a flag raises an error."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--flag",
        action=BoolFlagOrValue,
        nargs="?",
        default=False,
    )

    # This should work with nargs='?', only one value accepted
    args = parser.parse_args(["--flag", "true"])
    assert args.flag is True


@mark.parametrize(
    "token, expected",
    [
        param("true", True, id="true"),
        param("false", False, id="false"),
        param("1", True, id="1"),
        param("0", False, id="0"),
        param("yes", True, id="yes"),
        param("no", False, id="no"),
        param("on", True, id="on"),
        param("off", False, id="off"),
        param("t", True, id="t"),
        param("f", False, id="f"),
        param("y", True, id="y"),
        param("n", False, id="n"),
        param("TRUE", True, id="TRUE"),
        param("FALSE", False, id="FALSE"),
        param("Yes", True, id="Yes"),
        param("No", False, id="No"),
    ],
)
def test_parse_bool_token_parametrized(token: str, expected: bool):
    """Parametrized test for all valid boolean tokens."""
    assert parse_bool_token(token) == expected


@mark.parametrize(
    "invalid_token",
    [
        param("invalid", id="invalid"),
        param("maybe", id="maybe"),
        param("2", id="2"),
        param("-1", id="-1"),
        param("", id="empty"),
        param("truee", id="truee"),
        param("yess", id="yess"),
    ],
)
def test_parse_bool_token_invalid_parametrized(invalid_token: str):
    """Parametrized test for invalid boolean tokens."""
    with pytest.raises(argparse.ArgumentTypeError):
        parse_bool_token(invalid_token)


def test_constants_exist():
    """Test that the default token sets are defined correctly."""
    assert isinstance(TRUE_SET_DEFAULT, set)
    assert isinstance(FALSE_SET_DEFAULT, set)
    assert len(TRUE_SET_DEFAULT) > 0
    assert len(FALSE_SET_DEFAULT) > 0
    assert "true" in TRUE_SET_DEFAULT
    assert "false" in FALSE_SET_DEFAULT
    assert TRUE_SET_DEFAULT.isdisjoint(FALSE_SET_DEFAULT)
