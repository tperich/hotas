import gremlin
from gremlin.user_plugin import *

mode_name = StringVariable("Mode name", "Exact Gremlin mode name to run in", "Driving")

right_pedal = PhysicalInputVariable(
    "Right pedal",
    "Pick Right Toe axis",
    [gremlin.common.InputType.JoystickAxis]
)

left_pedal = PhysicalInputVariable(
    "Left pedal",
    "Pick Left Toe axis",
    [gremlin.common.InputType.JoystickAxis]
)

vjoy_id = IntegerVariable("vJoy Device ID", "vJoy device number", 1, min_value=1, max_value=16)
out_axis_right = IntegerVariable("Output axis (Right toe)", "vJoy axis number (1..8)", 1, min_value=1, max_value=8)
out_axis_left  = IntegerVariable("Output axis (Left toe)",  "vJoy axis number (1..8)", 2, min_value=1, max_value=8)

deadzone = FloatVariable("Toe deadzone", "Ignore tiny movement near idle (0..0.2)", 0.02)
invert_right = BoolVariable("Invert right", "Invert right toe axis", False)
invert_left  = BoolVariable("Invert left",  "Invert left toe axis", False)

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def pedal_to_01(x: float, idle_snap: float = 0.95) -> float:
    """
    x is physical axis in [-1..+1], idle is near -1.
    idle_snap=0.95 means: if x <= -0.95 treat as idle.
    """
    if x <= -idle_snap:
        return 0.0
    # rescale [-idle_snap .. +1] -> [0 .. 1]
    return clamp01((x + idle_snap) / (1.0 + idle_snap))

def set_vjoy_axis(axis_num: int, value: float):
    gremlin.joystick_handling.VJoyProxy()[vjoy_id.value].axis(axis_num).value = value

dR = right_pedal.create_decorator(mode_name.value)
@dR.axis(right_pedal.input_id)
def on_right(e):
    x = -e.value if invert_right.value else e.value
    set_vjoy_axis(out_axis_right.value, pedal_to_01(x))

dL = left_pedal.create_decorator(mode_name.value)
@dL.axis(left_pedal.input_id)
def on_left(e):
    x = -e.value if invert_left.value else e.value
    set_vjoy_axis(out_axis_left.value, pedal_to_01(x))