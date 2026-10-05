import lgpio

# Had Claude help me write a class that sets the pulse length of servos


_chip = None

def _handle():
    global _chip
    if _chip is None:
        _chip = lgpio.gpiochip_open(0)   # Pi 4 header GPIOs are on chip 0
    return _chip

class LgServo:
    """Same .angle get/set as AngularServo, but uses microsecond pulse widths."""
    def __init__(self, pin, initial_angle=90, min_angle=10, max_angle=170,
                 min_us=1000, max_us=2000):
        self.pin, self.min_angle, self.max_angle = pin, min_angle, max_angle
        self.min_us, self.max_us = min_us, max_us
        self._angle = None
        lgpio.gpio_claim_output(_handle(), pin)
        self.angle = initial_angle

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        value = max(self.min_angle, min(self.max_angle, value))
        frac = (value - self.min_angle) / (self.max_angle - self.min_angle)
        us = int(self.min_us + frac * (self.max_us - self.min_us))
        lgpio.tx_servo(_handle(), self.pin, us, 50)
        self._angle = value

    def close(self):
        lgpio.tx_servo(_handle(), self.pin, 0)   # stop pulses
    def release(self):
        lgpio.tx_servo(_handle(), self.pin, 0)   # stop pulses, servo holds in place