import logging
from typing import Any, Iterable

from normcap.gui.constants import DEFAULT_SETTINGS
from PySide6 import QtCore

logger = logging.getLogger(__name__)


class Settings(QtCore.QSettings):
    """Customized settings."""

    default_settings = DEFAULT_SETTINGS

    def __init__(self, *args: Iterable[Any], init_settings: dict) -> None:
        super().__init__(*args)
        self.setFallbacksEnabled(False)
        self.init_settings = init_settings
        self._prepare_and_sync()

    def _prepare_and_sync(self) -> None:
        self._set_missing_to_default()
        self._update_from_init_settings()
        self.sync()

    def _set_missing_to_default(self) -> None:
        for d in self.default_settings:
            key, value = d.key, d.value
            if key not in self.allKeys() or (self.value(key) is None):
                logger.debug("Reset settings to (%s: %s)", key, value)
                self.setValue(key, value)

    def _update_from_init_settings(self) -> None:
        for key, value in self.init_settings.items():
            if self.contains(key):
                if value is not None:
                    self.setValue(key, value)
            elif key in ("reset", "verbosity"):
                continue
            else:
                logger.debug("Skip update of non existing setting (%s: %s)", key, value)

    def reset(self) -> None:
        """Remove all existing settings and values."""
        logger.info("Reset settings to defaults")
        for key in self.allKeys():
            self.remove(key)
        self._prepare_and_sync()
