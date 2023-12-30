
import z3

from consistency.common import check
from consistency.model.monotonic_read import MonotonicRead
from consistency.model.read_your_writes import ReadYourWrites


def main() -> int:
    s = z3.Solver()

    MonotonicRead.constraints(s)
    ReadYourWrites.constraints(s)

    check(s)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
