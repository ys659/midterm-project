import re
import pytest
from colorama import Fore, Style
from app import ui

@pytest.mark.parametrize("func,color", [
    (ui.success, Fore.GREEN),
    (ui.error,   Fore.RED),
    (ui.info,    Fore.CYAN),
    (ui.value,   Fore.YELLOW),
])
def test_ui_color_formatting(func, color):
    """Each UI function should wrap the message in the right color and reset style."""
    msg = "test message"
    result = func(msg)

    # Check that color code appears, message is included, and style reset is appended
    assert isinstance(result, str)
    assert color in result
    assert msg in result
    assert result.endswith(Style.RESET_ALL)

def test_color_codes_do_not_stack():
    """Ensure multiple calls don't accumulate color codes."""
    msg = "check"
    first = ui.success(msg)
    second = ui.success(msg)
    # Count how many times RESET appears
    assert first.count(Style.RESET_ALL) == 1
    assert second.count(Style.RESET_ALL) == 1
    # Ensure no duplicate Fore codes appear inside
    assert len(re.findall(re.escape(Fore.GREEN), first)) == 1
    assert len(re.findall(re.escape(Fore.GREEN), second)) == 1
