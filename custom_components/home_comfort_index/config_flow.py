"""Config flow for Home Comfort Index."""

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import CONF_HUMIDITY_ENTITY, CONF_TEMPERATURE_ENTITY, DOMAIN


class HomeComfortIndexConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure the source temperature and humidity sensors."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial setup step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Home Comfort Index", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_TEMPERATURE_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        filter=[{"domain": "sensor", "device_class": "temperature"}]
                    )
                ),
                vol.Required(CONF_HUMIDITY_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        filter=[{"domain": "sensor", "device_class": "humidity"}]
                    )
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)
