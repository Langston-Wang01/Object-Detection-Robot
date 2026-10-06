from rpi_hardware_pwm import HardwarePWM

class HwServo:
    def __init__(self, channel, initial_angle=90, min_angle=10, max_angle=170,
                 min_ms=1.0, max_ms=2.0):
        self.pwm = HardwarePWM(pwm_channel=channel, hz=50, chip=0)
        self.min_angle, self.max_angle = min_angle, max_angle
        self.min_ms, self.max_ms = min_ms, max_ms
        self._angle = None
        self._started = False
        self.angle = initial_angle

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        value = max(self.min_angle, min(self.max_angle, float(value)))
        frac = (value - self.min_angle) / (self.max_angle - self.min_angle)
        ms = self.min_ms + frac * (self.max_ms - self.min_ms)
        duty = ms / 20 * 100          # percent of a 20 ms frame
        if self._started:
            self.pwm.change_duty_cycle(duty)
        else:
            self.pwm.start(duty)
            self._started = True
        self._angle = value

    def release(self):
        if self._started:
            self.pwm.stop()
            self._started = False