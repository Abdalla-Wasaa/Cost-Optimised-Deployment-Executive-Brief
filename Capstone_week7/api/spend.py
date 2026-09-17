"""Single-process fixed-window reservation guard; simulated USD, no billing claim."""
import time
from decimal import Decimal

class SpendExceeded(RuntimeError):
    pass

class SpendGuard:
    def __init__(self, ceiling, window, clock=time.monotonic):
        self.ceiling = Decimal(str(ceiling))
        if self.ceiling < 0 or window <= 0:
            raise ValueError('invalid spend configuration')
        self.window, self.clock = window, clock
        self.started = clock()
        self.used = Decimal('0')
        self.rejections = 0

    def reserve(self, amount):
        # No await: reservation is atomic on this service's single asyncio loop.
        amount = Decimal(str(amount))
        if not amount.is_finite() or amount < 0:
            raise ValueError('invalid reservation')
        now = self.clock()
        if now-self.started >= self.window:
            self.started, self.used = now, Decimal('0')
        if self.used+amount > self.ceiling:
            self.rejections += 1
            raise SpendExceeded('spend window exhausted')
        self.used += amount  # Keep reservation on failure: provider might have billed.
