"""Support for PETLIBRO binary sensors."""
from __future__ import annotations

from logging import getLogger

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry  # Added ConfigEntry import
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PetLibroHub
from .core import DOMAIN, Device
from .devices.feeders.air_smart_feeder import AirSmartFeeder
from .devices.feeders.feeder import Feeder
from .devices.feeders.granary_smart_camera_feeder import GranarySmartCameraFeeder
from .devices.feeders.granary_smart_feeder import GranarySmartFeeder
from .devices.feeders.one_rfid_smart_feeder import OneRFIDSmartFeeder
from .devices.feeders.polar_wet_food_feeder import PolarWetFoodFeeder
from .devices.fountains.dockstream_smart_fountain import DockstreamSmartFountain
from .devices.fountains.dockstream_smart_rfid_fountain import DockstreamSmartRFIDFountain
from .entities import PetLibroBinarySensorEntityDescription, PetLibroBinarySensorEntity
from .entities.binary_sensor import PetLibroDescribedBinarySensorEntity

_LOGGER = getLogger(__name__)

DEVICE_BINARY_SENSOR_MAP: dict[type[Device], list[PetLibroBinarySensorEntityDescription]] = {
    Feeder: [
    ],
    AirSmartFeeder: [
        PetLibroBinarySensorEntityDescription[AirSmartFeeder](
            key="food_dispenser_state",
            translation_key="food_dispenser_state",
            icon="mdi:bowl-outline",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.food_dispenser_state is not None,
            name="Food Dispenser"
        ),
        PetLibroBinarySensorEntityDescription[AirSmartFeeder](
            key="food_low",
            translation_key="food_low",
            icon="mdi:bowl-mix-outline",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.food_low is not None,
            name="Food Status"
        ),
        PetLibroBinarySensorEntityDescription[AirSmartFeeder](
            key="online",
            translation_key="online",
            icon="mdi:wifi",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            should_report=lambda device: device.online is not None,
            name="Wi-Fi"
        ),
        PetLibroBinarySensorEntityDescription[AirSmartFeeder](
            key="whether_in_sleep_mode",
            translation_key="whether_in_sleep_mode",
            icon="mdi:sleep",
            device_class=BinarySensorDeviceClass.POWER,
            should_report=lambda device: device.whether_in_sleep_mode is not None,
            name="Sleep Mode"
        ),
        PetLibroBinarySensorEntityDescription[AirSmartFeeder](
            key="enable_low_battery_notice",
            translation_key="enable_low_battery_notice",
            icon="mdi:battery-alert",
            device_class=BinarySensorDeviceClass.BATTERY,
            should_report=lambda device: device.enable_low_battery_notice is not None,
            name="Battery Status"
        ),
    ],
    GranarySmartFeeder: [
        PetLibroBinarySensorEntityDescription[GranarySmartFeeder](
            key="food_dispenser_state",
            translation_key="food_dispenser_state",
            icon="mdi:bowl-outline",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.food_dispenser_state is not None,
            name="Food Dispenser"
        ),
        PetLibroBinarySensorEntityDescription[GranarySmartFeeder](
            key="food_low",
            translation_key="food_low",
            icon="mdi:bowl-mix-outline",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.food_low is not None,
            name="Food Status"
        ),
        PetLibroBinarySensorEntityDescription[GranarySmartFeeder](
            key="online",
            translation_key="online",
            icon="mdi:wifi",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            should_report=lambda device: device.online is not None,
            name="Wi-Fi"
        ),
        PetLibroBinarySensorEntityDescription[GranarySmartFeeder](
            key="whether_in_sleep_mode",
            translation_key="whether_in_sleep_mode",
            icon="mdi:sleep",
            device_class=BinarySensorDeviceClass.POWER,
            should_report=lambda device: device.whether_in_sleep_mode is not None,
            name="Sleep Mode"
        ),
        PetLibroBinarySensorEntityDescription[GranarySmartFeeder](
            key="enable_low_battery_notice",
            translation_key="enable_low_battery_notice",
            icon="mdi:battery-alert",
            device_class=BinarySensorDeviceClass.BATTERY,
            should_report=lambda device: device.enable_low_battery_notice is not None,
            name="Battery Status"
        ),
    ],
    GranarySmartCameraFeeder: [
        PetLibroBinarySensorEntityDescription[GranarySmartCameraFeeder](
            key="food_dispenser_state",
            translation_key="food_dispenser_state",
            icon="mdi:bowl-outline",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.food_dispenser_state is not None,
            name="Food Dispenser"
        ),
        PetLibroBinarySensorEntityDescription[GranarySmartCameraFeeder](
            key="food_low",
            translation_key="food_low",
            icon="mdi:bowl-mix-outline",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.food_low is not None,
            name="Food Status"
        ),
        PetLibroBinarySensorEntityDescription[GranarySmartCameraFeeder](
            key="online",
            translation_key="online",
            icon="mdi:wifi",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            should_report=lambda device: device.online is not None,
            name="Wi-Fi"
        ),
        PetLibroBinarySensorEntityDescription[GranarySmartCameraFeeder](
            key="whether_in_sleep_mode",
            translation_key="whether_in_sleep_mode",
            icon="mdi:sleep",
            device_class=BinarySensorDeviceClass.POWER,
            should_report=lambda device: device.whether_in_sleep_mode is not None,
            name="Sleep Mode"
        ),
        PetLibroBinarySensorEntityDescription[GranarySmartCameraFeeder](
            key="enable_low_battery_notice",
            translation_key="enable_low_battery_notice",
            icon="mdi:battery-alert",
            device_class=BinarySensorDeviceClass.BATTERY,
            should_report=lambda device: device.enable_low_battery_notice is not None,
            name="Battery Status"
        ),
    ],
    OneRFIDSmartFeeder: [
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="door_state",
            translation_key="door_state",
            icon="mdi:door",
            device_class=BinarySensorDeviceClass.DOOR,
            should_report=lambda device: device.door_state is not None,
            name="Lid"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="food_dispenser_state",
            translation_key="food_dispenser_state",
            icon="mdi:bowl-outline",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.food_dispenser_state is not None,
            name="Food Dispenser"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="door_blocked",
            translation_key="door_blocked",
            icon="mdi:door",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.door_blocked is not None,
            name="Lid Status"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="food_low",
            translation_key="food_low",
            icon="mdi:bowl-mix-outline",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.food_low is not None,
            name="Food Status"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="online",
            translation_key="online",
            icon="mdi:wifi",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            should_report=lambda device: device.online is not None,
            name="Wi-Fi"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="whether_in_sleep_mode",
            translation_key="whether_in_sleep_mode",
            icon="mdi:sleep",
            device_class=BinarySensorDeviceClass.POWER,
            should_report=lambda device: device.whether_in_sleep_mode is not None,
            name="Sleep Mode"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="enable_low_battery_notice",
            translation_key="enable_low_battery_notice",
            icon="mdi:battery-alert",
            device_class=BinarySensorDeviceClass.BATTERY,
            should_report=lambda device: device.enable_low_battery_notice is not None,
            name="Battery Status"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="sound_switch",
            translation_key="sound_switch",
            icon="mdi:volume-high",
            should_report=lambda device: device.sound_switch is not None,
            name="Sound Status"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="child_lock_switch",
            translation_key="child_lock_switch",
            icon="mdi:lock",
            device_class=BinarySensorDeviceClass.LOCK,
            should_report=lambda device: device.child_lock_switch is not None,
            name="Buttons Lock"
        ),
        PetLibroBinarySensorEntityDescription[OneRFIDSmartFeeder](
            key="display_switch",
            translation_key="display_switch",
            icon="mdi:monitor-star",
            should_report=lambda device: device.display_switch is not None,
            name="Display Status"
        ),
    ],
    PolarWetFoodFeeder: [
        PetLibroBinarySensorEntityDescription[PolarWetFoodFeeder](
            key="online",
            translation_key="online",
            icon="mdi:wifi",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            should_report=lambda device: device.online is not None,
            name="Wi-Fi"
        ),
        PetLibroBinarySensorEntityDescription[PolarWetFoodFeeder](
            key="enable_low_battery_notice",
            translation_key="enable_low_battery_notice",
            icon="mdi:battery-alert",
            device_class=BinarySensorDeviceClass.BATTERY,
            should_report=lambda device: device.enable_low_battery_notice is not None,
            name="Battery Status"
        ),
        PetLibroBinarySensorEntityDescription[PolarWetFoodFeeder](
            key="door_blocked",
            translation_key="door_blocked",
            icon="mdi:door-closed-lock",
            device_class=BinarySensorDeviceClass.PROBLEM,
            should_report=lambda device: device.door_blocked is not None,
            name="Lid Status"
        ),
    ],
    DockstreamSmartFountain: [
        PetLibroBinarySensorEntityDescription[DockstreamSmartFountain](
            key="online",
            translation_key="online",
            icon="mdi:wifi",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            should_report=lambda device: device.online is not None,
            name="Wi-Fi"
        ),
    ],
    DockstreamSmartRFIDFountain: [
        PetLibroBinarySensorEntityDescription[DockstreamSmartRFIDFountain](
            key="online",
            translation_key="online",
            icon="mdi:wifi",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            should_report=lambda device: device.online is not None,
            name="Wi-Fi"
        ),
    ]
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,  # Use ConfigEntry
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PETLIBRO binary sensors using config entry."""
    # Retrieve the hub from hass.data that was set up in __init__.py
    hub: PetLibroHub = hass.data[DOMAIN].get(entry.entry_id)

    if not hub:
        _LOGGER.error("Hub not found for entry: %s", entry.entry_id)
        return

    # Ensure that the devices are loaded (if load_devices is not already called elsewhere)
    if not hub.devices:
        _LOGGER.warning("No devices found in hub during binary sensor setup.")
        return

    # Log the contents of the hub data for debugging
    _LOGGER.debug("Hub data: %s", hub)

    devices = hub.devices  # Devices should already be loaded in the hub
    _LOGGER.debug("Devices in hub: %s", devices)

    # Ask device directly if it has sensors
    entities = [
        sensor
        for device in devices
        for sensor in device.build_binary_sensors(hub.coordinator)
    ]
    if not entities:
        # Create binary sensor entities for each device based on the binary sensor map
        entities = [
            PetLibroDescribedBinarySensorEntity(device, hub.coordinator, description)
            for device in devices  # Iterate through devices from the hub
            for device_type, entity_descriptions in DEVICE_BINARY_SENSOR_MAP.items()
            if isinstance(device, device_type)
            for description in entity_descriptions
        ]

    if not entities:
        _LOGGER.warning("No binary sensors added, entities list is empty!")
    else:
        # Log the number of entities and their details
        _LOGGER.debug("Adding %d PetLibro binary sensors", len(entities))
        for entity in entities:
            _LOGGER.debug("Adding binary sensor entity: %s for device %s", entity.entity_id, entity.device.name)

        # Add binary sensor entities to Home Assistant
        async_add_entities(entities)

