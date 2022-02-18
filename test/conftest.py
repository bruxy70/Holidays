"""Fixtures for trsting."""
from datetime import datetime
from unittest.mock import patch

import pytest

TEST_PLUGINS = "pytest_homeassistant_custom_component"  # pylint: disable=invalid-name
FUNCTION_PATH = "custom_components.holidays.calendar.now"

# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


@pytest.fixture(name="fixed-date")
def mock_now():
    with patch(FUNCTION_PATH, return_value=datetime(2017, 3, 12, 0, 0, 0)):
        yield


# This fixture is used to prevent HomeAssistant from attempting
# to create and dismiss persistent notifications.
# These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield
