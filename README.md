# Home Comfort Index

**Turn the temperature and humidity sensors you already own into a simple, local indoor comfort indicator for Home Assistant.**

Home Comfort Index is a custom Home Assistant integration. It creates a score from 0 to 100 and a plain-language status from one temperature sensor and one relative-humidity sensor. It makes no internet requests and stores no measurements outside Home Assistant.

> The score is a lightweight household heuristic, not a medical, ventilation, or building-safety assessment. It does not measure air quality, CO₂, mold, or health risk.

## What it adds

- A comfort score sensor (0–100%).
- A status sensor: `Very comfortable`, `Comfortable`, `A little uncomfortable`, or `Uncomfortable`.
- Automatic updates when Home Assistant refreshes the selected sensor values (every 30 seconds).
- A guided setup flow to select existing sensors.
- English and Dutch setup translations.

## Install

### Manual

1. Copy `custom_components/home_comfort_index` into the `custom_components` folder in your Home Assistant configuration directory.
2. Restart Home Assistant.
3. Open **Settings → Devices & services → Add integration** and search for **Home Comfort Index**.
4. Select one temperature sensor and one relative-humidity sensor.

### HACS (custom repository)

Until this integration is accepted into a HACS default list, add this GitHub repository in **HACS → Integrations → ⋮ → Custom repositories**, select **Integration**, install it, restart Home Assistant, and add the integration from **Devices & services**.

## How the score works

The score starts at 100. It subtracts 3 points for each °C away from 21 °C, then subtracts 1.5 points for each percentage point that relative humidity falls outside the 40–60% band. The result is clamped to 0–100 and rounded to a whole number. The status is based on score bands: 85–100, 70–84, 50–69, and 0–49.

These deliberately simple thresholds make the result explainable. They are not a universal definition of comfort and may not suit every person, room, season, or building.

## Privacy and security

- Reads only the two Home Assistant sensor states selected during setup.
- Makes no network requests and requires no account or API key.
- Keeps calculated values in Home Assistant's in-memory coordinator; it does not create a separate database.
- Does not control devices or change automations.

## Requirements and limitations

- Home Assistant Core 2025.1 or newer.
- Temperature sensor with a numeric value in °C or °F.
- Relative-humidity sensor with a numeric percentage value.
- Sensor state becomes unavailable if either source is missing, unavailable, non-numeric, or has an unsupported unit.
- One integration entry is supported in this initial version.

## Development

The integration code is under `custom_components/home_comfort_index/`. No third-party Python package is required. This repository has not yet been run inside a Home Assistant instance; compatibility and entity behavior should be confirmed in a test instance before relying on it.

## Roadmap

- Add a configurable comfort profile after gathering user feedback.
- Support multiple rooms through separate entries.
- Consider a Home Assistant quality-scale review before applying for core inclusion.

## Nederlands

Home Comfort Index maakt van één bestaande temperatuursensor en één luchtvochtigheidssensor een lokale comfortscore van 0 tot 100 en een leesbare status. De integratie verstuurt geen gegevens naar internet. De score is een eenvoudige indicatie voor thuisgebruik, geen medische of bouwkundige meting.

Installatie: kopieer `custom_components/home_comfort_index` naar de map `custom_components` van Home Assistant, herstart Home Assistant en voeg **Home Comfort Index** toe via **Instellingen → Apparaten & diensten → Integratie toevoegen**. Kies daarna een temperatuursensor en een relatieve-luchtvochtigheidssensor.

## License

No license has been selected yet. Until one is added, reuse rights are not granted by this repository alone.
