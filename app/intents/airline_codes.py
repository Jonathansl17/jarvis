"""IATA carrier and airport codes, for Gemini's flight_delay_regression rules.

Kept as plain data, separate from the inference-rule text that renders them,
mirroring `intents/rules/extractors/flight_delay_regression.py`'s own small
lookup tables for the keyword-based fallback parser.
"""

CARRIER_CODES: dict[str, str] = {
    "American": "AA", "Delta": "DL", "United": "UA", "Southwest": "WN",
    "JetBlue": "B6", "Alaska": "AS", "US Airways": "US", "Continental": "CO",
    "Northwest": "NW", "Frontier": "F9", "AirTran": "FL", "Hawaiian": "HA",
    "Skywest": "OO", "ExpressJet": "XE", "Mesa": "YV", "Pinnacle": "9E",
    "Comair": "OH", "Atlantic Southeast": "EV", "American Eagle": "MQ",
    "Aloha": "AQ",
}

AIRPORT_CODES: dict[str, str] = {
    "Atlanta": "ATL", "Chicago": "ORD", "Los Ángeles": "LAX",
    "Nueva York": "JFK", "Dallas": "DFW", "Denver": "DEN", "Miami": "MIA",
    "San Francisco": "SFO", "Houston": "IAH", "Las Vegas": "LAS",
    "Seattle": "SEA", "Boston": "BOS", "Orlando": "MCO",
}
