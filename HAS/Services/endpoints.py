from .Repositories import System

ipAddress = "192.168.1.3"

sensorEndpoints = [
    f"http://{ipAddress}/get_flyback_voltage",
    f"http://{ipAddress}/get_flyback_frequency",
    f"http://{ipAddress}/get_flyback_dutyCycle",
    f"http://{ipAddress}/get_actual_position",
    f"http://{ipAddress}/get_actual_pressure",
    f"http://{ipAddress}/get_temperature_MCP9601C_Indoor",
    f"http://{ipAddress}/get_temperature_MCP9601C_Outdoor"
]

stateEndpoints = [
    {"system":System.vacuum, "url": f"http://{ipAddress}/get_pump_switch_state", "parameter":"pumpOn"},
    {"system":System.highVoltage, "url": f"http://{ipAddress}/get_flyback_switch_state", "parameter":"hvOn"} #0 = off, 1 = manual, 2 = remote, 3 = invalid
]

loggingEndpoints = [
    {"infoMessage": "ethernet OK", "errorMessage":"ethernet not OK","url": f"http://{ipAddress}/get_report_ethernet"},
    {"infoMessage": "i2c OK", "errorMessage":"i2c not OK","url": f"http://{ipAddress}/get_report_i2c"},
    {"infoMessage": "temperature OK", "errorMessage":"temperature not OK","url": f"http://{ipAddress}/get_report_temp"},
    {"infoMessage": "pressure OK", "errorMessage":"pressure not OK","url": f"http://{ipAddress}/get_report_press"},
]

# endpoints for Highvoltage
highVoltageOn=f"http://{ipAddress}/set_flyback_ps/1"
highVoltageOff=f"http://{ipAddress}/set_flyback_ps/0"
def setFrequency(value: float) -> str:
    return f"http://{ipAddress}/set_flyback_frequency/{value}"
def setDutycycle(value: float) -> str:
    return f"http://{ipAddress}/set_flyback_dutyCycle/{value}"

# endpoints for vacuumsystem
pumpOn=f"http://{ipAddress}/set_pump/1"
pumpOff=f"http://{ipAddress}/set_pump/0"
pressureControlMode=f"http://{ipAddress}/set_control_mode/5"
def setTargetPressure(value: float) -> str:
    return f"http://{ipAddress}/set_target_pressure/{value}"
def setTargetPosition(value: float) -> str:
    return f"http://{ipAddress}/set_target_position/{value}"
