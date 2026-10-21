"""Read source entities and calculate the local comfort indicator."""

from __future__ import annotations

from typing import Any

from homeassistant.const import ATTR_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed


def _read_number(hass: HomeAssistant, entity_id: str, label: str) -> tuple[float, str]:
    """Return a finite numeric state and its unit or raise a useful update error."""
    state = hass.states.get(entity_id)
    if state is None or state.state in ("unknown", "unavailable"):
        raise UpdateFailed(f"The selected {label} sensor is unavailable")
    try:
        value = float(state.state)
    except (TypeError, ValueError) as err:
        raise UpdateFailed(f"The selected {label} sensor has a non-numeric value") from err
    if not (-1e6 < value < 1e6):
        raise UpdateFailed(f"The selected {label} sensor has an invalid value")
    return value, state.attributes.get(ATTR_UNIT_OF_MEASUREMENT, "")


async def async_fetch_readings(
    hass: HomeAssistant, temperature_entity: str, humidity_entity: str
) -> dict[str, Any]:
    """Read the selected entities and calculate score and label."""
    temperature, temperature_unit = _read_number(hass, temperature_entity, "temperature")
    humidity, humidity_unit = _read_number(hass, humidity_entity, "humidity")

    if temperature_unit in ("°F", "F"):
        temperature = (temperature - 32) * 5 / 9
    elif temperature_unit not in ("°C", "C"):
        raise UpdateFailed("Temperature must be reported in °C or °F")
    if humidity_unit not in ("%", "%RH"):
        raise UpdateFailed("Humidity must be reported as a percentage")
    if not 0 <= humidity <= 100:
        raise UpdateFailed("Humidity must be between 0 and 100 percent")

    score = max(
        0,
        min(
            100,
            100
            - abs(temperature - 21) * 3
            - max(0, 40 - humidity, humidity - 60) * 1.5,
        ),
    )
    rounded_score = round(score)
    if rounded_score >= 85:
        label = "very_comfortable"
    elif rounded_score >= 70:
        label = "comfortable"
    elif rounded_score >= 50:
        label = "slightly_uncomfortable"
    else:
        label = "uncomfortable"

    return {
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1),
        "score": rounded_score,
        "label": label,
    }
