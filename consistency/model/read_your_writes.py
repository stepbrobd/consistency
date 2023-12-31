import z3

from consistency.abstract_execution import AbstractExecution
from consistency.constraint import Constraint


class ReadYourWrites:
    """
    Read-Your-Writes are defined as:
    for all write operations $a$ in history, a set of operations denoted by $H$, and,
    for all read operations $b$ in history $H$,
    if operation $a$ returns before $b$ starts, and $a,b$ are in the same session,
    then operation $a$ is visible to operation $b$.
    """
    @staticmethod
    def constraints(s: z3.Solver) -> None:
        """
        Add read-your-writes constraints.
        """
        _, (rd, wr) = Constraint.declare_operation_type()
        op = Constraint.declare_operation()
        a, b = z3.Consts("a b", op)

        ss = Constraint.same_session(s)
        so = Constraint.session_order(s)
        vis = Constraint.visibility(s)

        s.add([
            # all operations and themselves are in the same session
            ss(a, a),
            ss(b, b),
            # read-your-writes
            z3.ForAll([a, b],
                z3.Implies(
                    z3.And(so(a, b), op.type(a) == wr, op.type(b) == rd),
                    vis(a, b)
                )
            ),
        ])


    @staticmethod
    def check(ae: AbstractExecution) -> bool:
        ...
