"""Sensors created by Home Comfort Index."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN


@dataclass(frozen=True, kw_only=True)
class ComfortSensorDescription(SensorEntityDescription):
    """Describe a calculated comfort sensor."""

    value_fn: Callable[[dict], int | str]


SENSORS = (
    ComfortSensorDescription(
        key="score",
        translation_key="comfort_score",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["score"],
    ),
    ComfortSensorDescription(
        key="status",
        translation_key="comfort_status",
        value_fn=lambda data: data["label"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up calculated sensors for one config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ComfortSensor(coordinator, entry, description) for description in SENSORS
    )


class ComfortSensor(CoordinatorEntity, SensorEntity):
    """Expose one value from the shared coordinator."""

    entity_description: ComfortSensorDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        description: ComfortSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_has_entity_name = True

    @property
    def native_value(self) -> int | str:
        """Return the current score or translated status key."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, float]:
        """Include the source readings to make the score explainable."""
        return {
            "temperature_c": self.coordinator.data["temperature"],
            "relative_humidity": self.coordinator.data["humidity"],
        }
