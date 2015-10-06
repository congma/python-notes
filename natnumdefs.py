"""
Set-theory definition of natural numbers.

Examples:
>>> one == succ(zero)
True
>>> two = succ(one)
>>> three = succ(two)
>>> three == prod(three, one)   # identity of multiplication
True
>>> three == add(zero, three)   # identity of addition
True
>>> four = succ(three)
>>> four == prod(two, two) == pow_(two, two)
True
>>> sub(four, two) == two
True
>>> five = succ(four)
>>> five == add(two, three) == add(three, two)  # commutativity
True
>>> six = succ(five)
>>> six == add(two, four) == prod(two, three)
True
>>> # associativity
>>> add(three, add(four, two)) == add(add(three, four), two)
True
>>> (two, one) == divmod_(five, two)
True
>>> (zero, two) == divmod_(two, five)
True
>>> to_int_fast(six)
6
>>> from_int(7) == succ(six)
True
>>> cmp_(three, five) < 0
True
"""


# Definition of natural numbers and their arithmetics.
# Uses only Python builtins.
# Zero is a natural number.
zero = frozenset()


# Successor function defines next number.
def succ(n):
    """Successor function."""
    return n | frozenset((n,))


# Unique predecessor.
def pred(n):
    """Predecessor function.  Raises ArithmeticError when input is zero."""
    try:
        return max(n)
    except ValueError:
        raise ArithmeticError("No predecessor to zero.")


# Idioms to ease programming and reduce typing.
def tobinary(unary):
    """Convert unary function to binary that ignores the right argument."""
    return lambda x, y: unary(x)


# Binary version of common unary operators.
# _s: successor (Python int); s: successor; p: predecessor.
_s, s, p = map(tobinary, (lambda x: x + 1, succ, pred))


# Idiomatic generators useful in a wide range of constructs.
def xrange_(n):
    """Emulate Python's xrange(n)."""
    p = zero
    while p < n:
        yield p
        p = succ(p)


def repeat(m, n):
    """Repeat m for n times."""
    for i in xrange_(n):
        yield m


# Total order.
def cmp_(m, n):
    """Compare two natural numbers.  Compatible with Python cmp().
    Allowed to return native Python integers.
    """
    if m < n:
        return -1
    elif m == n:
        return 0
    elif m > n:
        return 1


# Arithmetic
def add_r(m, n):
    """Addition function (recursive).
    Can reach recursion limit imposed by Python or the hosting OS, raising
    RuntimeError.  For demo only.
    """
    if n == zero:
        return m
    return add_r(succ(m), pred(n))


def add(m, n):
    """Addition function (without recursion)."""
    return reduce(s, xrange_(n), m)


def sub_r(m, n):
    """Subtraction function (recursive).
    Raises ArithmeticError when m is less than n.
    Can reach recursion limit imposed by Python or the hosting OS, raising
    RuntimeError.  For demo only.
    """
    if n == zero:
        return m
    return sub_r(pred(m), pred(n))


def sub(m, n):
    """Subtraction function (without recursion).
    Raises ArithmeticError when m is less than n.
    """
    return reduce(p, xrange_(n), m)


def prod_r(m, n):
    """Multiplication function (recursive).
    Can reach recursion limit imposed by Python or the hosting OS, raising
    RuntimeError.  For demo only.
    """
    if n == zero:
        return zero
    return add(m, prod_r(m, pred(n)))


def prod(m, n):
    """Multiplication function (without recursion)."""
    return reduce(add, repeat(m, n), zero)


def pow_(m, n):
    """Power function."""
    return reduce(prod, repeat(m, n), one)


def divmod_(m, n):
    """Integer division function.  Emulates Python divmod().
    Returns tuple (quotient, remainder).  Raises ZeroDivisionError when
    dividing by zero.
    """
    if n == zero:
        raise ZeroDivisionError("Division by zero.")
    rem = m
    quot = zero
    # Can be implemented without looping, by suitably wrapping reduce()
    # so that it handles exceptions.
    while True:
        try:
            rem = sub(rem, n)
        except ArithmeticError:
            return quot, rem
        quot = succ(quot)


# Conversion to and from Python native integers.
def to_int_fast(n):
    """Convert to Python integer in O(1), using implementation-specific
    details.
    """
    return len(n)


def to_int(n):
    """Convert to Python integer in O(n), using generic definition."""
    return reduce(_s, n, 0)


def from_int(n):
    """Create from Python integer."""
    if n < 0:
        raise ValueError("Input number less than zero.")
    return reduce(s, xrange(int(n)), zero)


# Handy small number.
one = succ(zero)


if __name__ == "__main__":
    import sys
    import doctest
    doctest.testmod(verbose="-v" in sys.argv[1:])
