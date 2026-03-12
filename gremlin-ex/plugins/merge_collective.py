import gremlin
from gremlin.user_plugin import *

main_axis = PhysicalInputVariable(
    "Main collective (Throttle Z)",
    "Pick your throttle Z axis here",
    [gremlin.common.InputType.JoystickAxis]
)

corr_axis = PhysicalInputVariable(
    "Correction (mini-stick Y)",
    "Pick your mini-stick Y axis here",
    [gremlin.common.InputType.JoystickAxis]
)

VJOY_ID = 1
VJOY_AXIS_ID = 5

invert_correction = BoolVariable("Invert correction", "Flip the correction axis direction", True)
gain = FloatVariable("Correction gain", "How strong correction is (0.05–0.20)", 0.12)
deadzone = FloatVariable("Correction deadzone", "Ignore drift (0.03–0.10)", 0.06)

_state_main = 0.0
_state_corr = 0.0

def clamp(x: float) -> float:
    return max(-1.0, min(1.0, x))

def write_out():
    global _state_main, _state_corr

    corr = _state_corr
    if abs(corr) < deadzone.value:
        corr = 0.0
    if invert_correction.value:
        corr = -corr

    out = clamp(_state_main + corr * gain.value)
    gremlin.joystick_handling.VJoyProxy()[VJOY_ID].axis(VJOY_AXIS_ID).value = out

def register_for_mode(mode_name: str):
    d1 = main_axis.create_decorator(mode_name)
    @d1.axis(main_axis.input_id)
    def on_main(event):
        global _state_main
        _state_main = event.value
        write_out()

    d2 = corr_axis.create_decorator(mode_name)
    @d2.axis(corr_axis.input_id)
    def on_corr(event):
        global _state_corr
        _state_corr = event.value
        write_out()

# Add whatever modes you actually have in your profile:
for m in ("Driving", "Flight", "UI"):
    register_for_mode(m)
