import re


class FormulaEngine:

    CELL_REF = re.compile(r"[A-Z]+[0-9]+")

    def __init__(self, sheet_data):
        self.sheet = sheet_data

    # ----------------------------
    # Public API
    # ----------------------------

    def evaluate(self, value):

        if not isinstance(value, str):
            return value

        if not value.startswith("="):
            return value

        expression = value[1:]

        if expression.startswith("SUM"):
            return self._sum(expression)

        if expression.startswith("IF"):
            return self._if(expression)

        return self._evaluate_math(expression)

    # ----------------------------
    # SUM
    # ----------------------------

    def _sum(self, expr):

        inside = expr[4:-1]

        parts = inside.split(",")

        total = 0

        for part in parts:

            if ":" in part:
                total += self._sum_range(part)
            else:
                total += self._get_cell_value(part)

        return total

    def _sum_range(self, range_expr):

        start, end = range_expr.split(":")

        r1, c1 = self._cell_to_index(start)
        r2, c2 = self._cell_to_index(end)

        total = 0

        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):

                try:
                    total += float(self.sheet[r][c])
                except:
                    pass

        return total

    # ----------------------------
    # IF
    # ----------------------------

    def _if(self, expr):

        inside = expr[3:-1]

        condition, true_val, false_val = inside.split(",")

        result = self._evaluate_math(condition)

        if result:
            return true_val.strip('"')
        else:
            return false_val.strip('"')

    # ----------------------------
    # math expressions
    # ----------------------------

    def _evaluate_math(self, expr):

        refs = self.CELL_REF.findall(expr)

        for ref in refs:
            value = self._get_cell_value(ref)
            expr = expr.replace(ref, str(value))

        try:
            return eval(expr)
        except:
            return "ERR"

    # ----------------------------
    # cell helpers
    # ----------------------------

    def _get_cell_value(self, ref):

        r, c = self._cell_to_index(ref)

        try:
            return float(self.sheet[r][c])
        except:
            return 0

    def _cell_to_index(self, ref):

        col = 0
        row = ""

        for ch in ref:

            if ch.isalpha():
                col = col * 26 + (ord(ch) - 64)
            else:
                row += ch

        return int(row) - 1, col - 1