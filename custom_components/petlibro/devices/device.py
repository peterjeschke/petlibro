from logging import getLogger
from typing import cast

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .event import Event, EVENT_UPDATE
from ..api import PetLibroAPI

_LOGGER = getLogger(__name__)


class Device(Event):
    def __init__(self, data: dict, api: PetLibroAPI):
        super().__init__()
        self._data: dict = {}
        self.api = api

        self.update_data(data)

    def update_data(self, data: dict) -> None:
        """Save the device info from a data dictionary."""
        try:
            _LOGGER.debug("Updating data with new information.")
            self._data.update(data)
            self.emit(EVENT_UPDATE)
            _LOGGER.debug("Data updated successfully.")
        except Exception as e:
            _LOGGER.error(f"Error updating data: {e}")
            _LOGGER.debug(f"Partial data: {data.get('deviceSn', 'Unknown Serial')}")

    async def refresh(self):
        """Refresh the device data from the API."""
        try:
            data = {}
            data.update(await self.api.device_base_info(self.serial))
            data.update(await self.api.device_real_info(self.serial))
            data.update(await self.api.device_attribute_settings(self.serial))
            self.update_data(data)
        except Exception as e:
            _LOGGER.error(f"Failed to refresh device data: {e}")

    def build_sensors(self, coordinator: DataUpdateCoordinator[bool]) -> list[SensorEntity]:
        _LOGGER.debug("device has no sensors")
        return []

    @property
    def serial(self) -> str:
        return cast(str, self._data.get("deviceSn"))

    @property
    def model(self) -> str:
        return cast(str, self._data.get("productIdentifier"))

    @property
    def model_name(self) -> str:
        return cast(str, self._data.get("productName"))

    @property
    def name(self) -> str:
        return cast(str, self._data.get("name"))

    @property
    def mac(self) -> str:
        return cast(str, self._data.get("mac"))

    @property
    def software_version(self) -> str:
        return cast(str, self._data.get("softwareVersion"))

    @property
    def hardware_version(self) -> str:
        return cast(str, self._data.get("hardwareVersion"))
