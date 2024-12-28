from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from typing import Callable, Any

from homeassistant.components.sensor import SensorEntityDescription, SensorDeviceClass, SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .entity import PetLibroEntityDescription, _DeviceT, PetLibroEntity
from ..core import PetLibroHub

_LOGGER = getLogger(__name__)

@dataclass(frozen=True)
class PetLibroSensorEntityDescription(SensorEntityDescription, PetLibroEntityDescription[_DeviceT]):
    """A class that describes device sensor entities."""

    icon_fn: Callable[[Any], str | None] = lambda _: None
    native_unit_of_measurement_fn: Callable[[_DeviceT], str | None] = lambda _: None
    device_class_fn: Callable[[_DeviceT], SensorDeviceClass | None] = lambda _: None
    should_report: Callable[[_DeviceT], bool] = lambda _: True



class PetLibroSensorEntity(PetLibroEntity[_DeviceT], SensorEntity):
    def __init__(self, device: _DeviceT, coordinator: DataUpdateCoordinator, key: str):
        super().__init__(device, coordinator, key)

        # Ensure unique_id includes the device serial, specific sensor key, and the MAC address from the device attributes
        mac_address = getattr(device, "mac", None)
        if mac_address:
            self._attr_unique_id = f"{device.serial}-{key}-{mac_address.replace(':', '')}"
        else:
            self._attr_unique_id = f"{device.serial}-{key}"

        # Dictionary to keep track of the last known state for each sensor key
        self._last_sensor_state = {}


class PetLibroDescribedSensorEntity(PetLibroSensorEntity[_DeviceT],
                                    SensorEntity):
    entity_description: PetLibroSensorEntityDescription[_DeviceT]

    def __init__(self, device: _DeviceT, coordinator: DataUpdateCoordinator, description: PetLibroSensorEntityDescription[_DeviceT]):
        super().__init__(device, coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> float | datetime | str | None:
        """Return the state."""

        sensor_key = self.entity_description.key

        # Handle feeding_plan_state as "On" or "Off"
        if sensor_key == "feeding_plan_state":
            feeding_plan_active = getattr(self.device, sensor_key, False)
            # Log only if the state has changed
            if self._last_sensor_state.get(sensor_key) != feeding_plan_active:
                _LOGGER.debug(f"Raw {sensor_key} for device {self.device.serial}: {feeding_plan_active}")
                self._last_sensor_state[sensor_key] = feeding_plan_active
            return "On" if feeding_plan_active else "Off"

        # Handle today_eating_time as raw seconds value
        elif sensor_key == "today_eating_time":
            eating_time_seconds = getattr(self.device, sensor_key, 0)
            return eating_time_seconds

        # Handle today_feeding_quantity as raw numeric value, converting to cups
        elif sensor_key == "today_feeding_quantity":
            feeding_quantity = getattr(self.device, sensor_key, 0)
            # Determine the conversion factor based on device-specific attributes or context
            conversion_factor = 1 / 12  # Default conversion factor
            if hasattr(self.device, "conversion_mode") and self.device.conversion_mode == "1/24":
                conversion_factor = 1 / 24

            cups = feeding_quantity * conversion_factor
            return f"{round(cups, 2)}"

        # Handle wifi_rssi to display only the numeric value
        elif sensor_key == "wifi_rssi":
            wifi_rssi = getattr(self.device, sensor_key, None)
            if wifi_rssi is not None:
                if self._last_sensor_state.get(sensor_key) != wifi_rssi:
                    _LOGGER.debug(f"Raw {sensor_key} for device {self.device.serial}: {wifi_rssi}")
                    self._last_sensor_state[sensor_key] = wifi_rssi
                return wifi_rssi

        # Handle weight in grams and convert to ounces
        elif sensor_key == "weight":
            weight_in_grams = getattr(self.device, sensor_key, 0.0)
            ounces = round(weight_in_grams * 0.035274, 2)
            return ounces

        # Default behavior for other sensors
        if self.entity_description.should_report(self.device):
            val = getattr(self.device, sensor_key, None)
            # Log only if the state has changed
            if self._last_sensor_state.get(sensor_key) != val:
                _LOGGER.debug(f"Raw {sensor_key} for device {self.device.serial}: {val}")
                self._last_sensor_state[sensor_key] = val
            return val
        return None

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend, if any."""
        if (icon := self.entity_description.icon_fn(self.state)) is not None:
            return icon
        return super().icon

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement to use in the frontend, if any."""
        # For temperature, display as Fahrenheit
        if self.entity_description.key == "temperature":
            return "°F"
        # For today_feeding_quantity, display as cups in the frontend
        if self.entity_description.key == "today_feeding_quantity":
            return "cups"
        # For today_eating_time, display as seconds in the frontend
        elif self.entity_description.key == "today_eating_time":
            return "s"
        # For wifi_rssi, display as dBm
        elif self.entity_description.key == "wifi_rssi":
            return "dBm"
        # For weight, display as ounces in the frontend
        elif self.entity_description.key == "weight":
            return "oz"
        # For use_water_interval and use_water_duration, display as minutes
        elif self.entity_description.key in ["use_water_interval", "use_water_duration"]:
            return "min"
        # For weight_percent, display as a percentage
        elif self.entity_description.key == "weight_percent":
            return "%"
        # For electric_quantity, display as a percentage
        elif self.entity_description.key == "electric_quantity":
            return "%"
        # Default behavior for other sensors
        return self.entity_description.native_unit_of_measurement_fn(self.device)

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class to use in the frontend, if any."""
        if (device_class := self.entity_description.device_class_fn(self.device)) is not None:
            return device_class
        return super().device_class
