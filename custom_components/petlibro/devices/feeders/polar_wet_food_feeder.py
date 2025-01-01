from datetime import datetime
from logging import getLogger
from typing import Any
from zoneinfo import ZoneInfo

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from typing_extensions import override

from ...core import PetLibroAPIError, Device
from ...entities import WetFeedingPlanPlateSensorEntity, PetLibroSensorEntityDescription, PetLibroSensorEntity, \
    PetLibroDescribedSensorEntity

_LOGGER = getLogger(__name__)


class PolarWetFoodFeeder(Device):
    @override
    async def refresh(self):
        """Refresh the device data from the API."""
        try:
            await super().refresh()

            grain_status = await self.api.device_grain_status(self.serial)
            real_info = await self.api.device_real_info(self.serial)
            feeding_plan_templates = await self.api.device_feeding_plan_templates(self.serial)
            wet_feeding_plan = await self.api.device_wet_feeding_plan(self.serial)

            self.update_data({
                "grainStatus": grain_status or {},
                "realInfo": real_info or {},
                "feedingPlanTemplates": feeding_plan_templates or {},
                "wetFeedingPlan": wet_feeding_plan or {},
            })
        except PetLibroAPIError as err:
            _LOGGER.error("Error refreshing data for PolarWetFoodFeeder", err)

    @override
    def build_sensors(self, coordinator: DataUpdateCoordinator) -> list[PetLibroSensorEntity]:
        return [
            *(
                PetLibroDescribedSensorEntity(self, coordinator, description)
                for description in [
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="device_sn",
                    translation_key="device_sn",
                    icon="mdi:identifier",
                    name="Device SN"
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="mac",
                    translation_key="mac_address",
                    icon="mdi:network",
                    name="MAC Address"
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="wifi_rssi",
                    translation_key="wifi_rssi",
                    icon="mdi:wifi",
                    native_unit_of_measurement="dBm",
                    name="Wi-Fi Signal Strength",
                    device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                    state_class=SensorStateClass.MEASUREMENT
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="wifi_ssid",
                    translation_key="wifi_ssid",
                    icon="mdi:wifi",
                    name="Wi-Fi SSID"
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="battery_state",
                    translation_key="battery_state",
                    icon="mdi:battery",
                    name="Battery Level"
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="electric_quantity",
                    translation_key="electric_quantity",
                    icon="mdi:battery",
                    native_unit_of_measurement="%",
                    device_class=SensorDeviceClass.BATTERY,
                    state_class=SensorStateClass.MEASUREMENT,
                    name="Battery / AC %"
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="feeding_plan_state",
                    translation_key="feeding_plan",
                    icon="mdi:calendar-check",
                    name="Feeding Plan",
                    should_report=lambda device: device.feeding_plan_state is not None,
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="next_feeding_time",
                    translation_key="next_feeding_time",
                    icon="mdi:clock-outline",
                    name="Feeding Begins",
                    device_class=SensorDeviceClass.TIMESTAMP
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="next_feeding_end_time",
                    translation_key="next_feeding_end_time",
                    icon="mdi:clock-end",
                    name="Feeding Ends",
                    device_class=SensorDeviceClass.TIMESTAMP
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="plate_position",
                    translation_key="plate_position",
                    icon="mdi:rotate-3d-variant",
                    name="Plate Position",
                    should_report=lambda device: device.plate_position is not None,
                ),
                PetLibroSensorEntityDescription[PolarWetFoodFeeder](
                    key="active_feeding_plan_name",
                    translation_key="active_feeding_plan_name",
                    icon="mdi:notebook",
                    name="Active feeding plan"
                )
            ]
            ),
        ]

    @override
    def build_binary_sensors(self, coordinator: DataUpdateCoordinator) -> list[BinarySensorEntity]:
        _LOGGER.debug("Polar: Building binary sensors")
        result = []
        for plate_index in range(1, 4):
            _LOGGER.debug("Polar: Building plate sensor %", plate_index)
            plate = self._get_feeding_plan_plate(plate_index)
            result.append(WetFeedingPlanPlateSensorEntity(self, coordinator, plate_index, plate))
        _LOGGER.debug("Polar: Built sensors %", result)
        return result

    def _get_feeding_plan_plate(self, plate_index: int) -> dict[str, Any] | None:
        result = None
        _LOGGER.debug("Checking plans: %", self._data.get("wetFeedingPlan", {}).get("plan", []))
        for plate in self._data.get("wetFeedingPlan", {}).get("plan", []):
            if plate.get("plate") == str(plate_index):
                result = plate
        _LOGGER.debug("Plan for plate %: %", plate_index, result)
        return result

    @property
    def battery_state(self) -> str | None:
        return self._data.get("batteryState")

    @property
    def device_sn(self) -> str:
        """Returns the serial number of the device."""
        return self._data.get("deviceSn", "unknown")

    @property
    def door_blocked(self) -> bool | None:
        return self._data.get("realInfo", {}).get("barnDoorError")

    @property
    def electric_quantity(self) -> int | None:
        """Electric quantity (battery percentage or power state)."""
        return self._data.get("electricQuantity")

    @property
    def feeding_plan_state(self) -> bool | None:
        """Return the state of the feeding plan."""
        return self._data.get("enableFeedingPlan")

    @property
    def active_feeding_plan_name(self) -> str | None:
        """Returns the name of the currently active feeding plan"""
        return self._data.get("wetFeedingPlan", {}).get("templateName")

    @property
    def next_feeding_time(self) -> datetime | None:
        """Returns the next feeding start date/time as native datetime object. Will return None, if the date/time is
        not parsable."""
        raw_time = self._data.get("nextFeedingTime")
        raw_date = self._data.get("nextFeedingDay")
        raw_timezone = self._data.get("timezone")
        if None in (raw_time, raw_date, raw_timezone):
            _LOGGER.error("One of the time values is not available: raw_time=%s raw_date=%s raw_timezone=%s", raw_time,
                          raw_date, raw_timezone)
            return None
        raw_combined = f"{raw_date} {raw_time}"
        try:
            time_obj = datetime.strptime(raw_combined, "%Y-%m-%d %H:%M").astimezone(ZoneInfo(raw_timezone))
            return time_obj
        except ValueError:
            _LOGGER.error("Error converting time from %s in timezone %s", raw_combined, raw_timezone)
            return None

    @property
    def next_feeding_end_time(self) -> datetime | None:
        """Returns the next feeding start date/time as native datetime object. Will return None, if the date/time is
        not parsable. Assumes that the end time occurs on the same date as the start time, because the API does not
        support feeding times beyond midnight."""
        raw_time = self._data.get("nextFeedingEndTime")
        raw_date = self._data.get("nextFeedingDay")
        raw_timezone = self._data.get("timezone")
        if None in (raw_time, raw_date, raw_timezone):
            _LOGGER.error("One of the time values is not available: raw_time=%s raw_date=%s raw_timezone=%s", raw_time,
                          raw_date, raw_timezone)
            return None
        raw_combined = f"{raw_date} {raw_time}"
        try:
            time_obj = datetime.strptime(raw_combined, "%Y-%m-%d %H:%M").astimezone(ZoneInfo(raw_timezone))
            return time_obj
        except ValueError:
            _LOGGER.error("Error converting time from %s in timezone %s", raw_combined, raw_timezone)
            return None

    @property
    def online(self) -> bool | None:
        """Returns the online status of the device."""
        return self._data.get("online")

    @property
    def online_list(self) -> list:
        """Returns a list of online status records with timestamps."""
        return self._data.get("realInfo", {}).get("onlineList", [])

    @property
    def plate_position(self) -> int | None:
        """Returns the current position of the plate, if applicable."""
        return self._data.get("realInfo", {}).get("platePosition")

    @property
    def unit_type(self) -> int | None:
        return self._data.get("realInfo", {}).get("unitType")

    @property
    def enable_low_battery_notice(self) -> bool | None:
        return self._data.get("realInfo", {}).get("enableLowBatteryNotice")

    @property
    def wifi_rssi(self) -> int | None:
        """Returns the Wi-Fi's RSSI, also known as signal strength"""
        return self._data.get("wifiRssi")

    @property
    def wifi_ssid(self) -> str | None:
        """Returns the Wi-Fi's SSID, also known as the name"""
        return self._data.get("realInfo", {}).get("wifiSsid")
