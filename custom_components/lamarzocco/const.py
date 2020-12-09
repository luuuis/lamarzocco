"""Constants for the La Marzocco integration."""

DOMAIN = "lamarzocco"

CONF_SERIAL_NUMBER = "serial_number"
CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"

DEFAULT_NAME = "Espresso Machine"

ATTR_ENABLE_PREBREWING = "ENABLE_PREBREWING"
ATTR_STBY_TIMER = "STBY_TIMER"
ATTR_TON_PREBREWING_K1 = "TON_PREBREWING_K1"
ATTR_TON_PREBREWING_K2 = "TON_PREBREWING_K2"
ATTR_TON_PREBREWING_K3 = "TON_PREBREWING_K3"
ATTR_TON_PREBREWING_K4 = "TON_PREBREWING_K4"
ATTR_TOFF_PREBREWING_K1 = "TOFF_PREBREWING_K1"
ATTR_TOFF_PREBREWING_K2 = "TOFF_PREBREWING_K2"
ATTR_TOFF_PREBREWING_K3 = "TOFF_PREBREWING_K3"
ATTR_TOFF_PREBREWING_K4 = "TOFF_PREBREWING_K4"
ATTR_TSET_STEAM = "TSET_STEAM"
ATTR_TSET_COFFEE = "TSET_COFFEE"
ATTR_DOSE_K1 = "DOSE_K1"
ATTR_DOSE_K2 = "DOSE_K2"
ATTR_DOSE_K3 = "DOSE_K3"
ATTR_DOSE_K4 = "DOSE_K4"
ATTR_DOSE_K5 = "DOSE_K5"
ATTR_DOSE_TEA = "DOSE_TEA"
STATE_STATUS = "status"
DATA_TAG = "data"
STATUS_ON = "ON"
STATUS_STANDBY = "STANDBY"
MACHINE_STATUS = "MACHINE_STATUS"

STATUS_MAP = {STATUS_ON: "On", STATUS_STANDBY: "Standby"}

COMMAND_ON = {"status": "ON"}
COMMAND_STANDBY = {"status": "STANDBY"}

GW_URL = "https://gw.lamarzocco.io/v1/home/machines"

ATTR_MAP = {
    STATE_STATUS: "status",
    ATTR_ENABLE_PREBREWING: "prebrewing_enabled",
    ATTR_STBY_TIMER: "standby_timer",
    ATTR_TON_PREBREWING_K1: "prebrewing_ton_k1",
    ATTR_TON_PREBREWING_K2: "prebrewing_ton_k2",
    ATTR_TON_PREBREWING_K3: "prebrewing_ton_k3",
    ATTR_TON_PREBREWING_K4: "prebrewing_ton_k4",
    ATTR_TOFF_PREBREWING_K1: "prebrewing_toff_k1",
    ATTR_TOFF_PREBREWING_K2: "prebrewing_toff_k2",
    ATTR_TOFF_PREBREWING_K3: "prebrewing_toff_k3",
    ATTR_TOFF_PREBREWING_K4: "prebrewing_toff_k4",
    ATTR_TSET_STEAM: "steam_temperature",
    ATTR_TSET_COFFEE: "coffee_temperature",
    ATTR_DOSE_K1: "dose_k1",
    ATTR_DOSE_K2: "dose_k2",
    ATTR_DOSE_K3: "dose_k3",
    ATTR_DOSE_K4: "dose_k4",
    ATTR_DOSE_K5: "dose_k5",
    ATTR_DOSE_TEA: "dose_tea",
}