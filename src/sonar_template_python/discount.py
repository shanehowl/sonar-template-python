"""Deliberate quality-gate failures (remove after testing the gate)."""

# Vulnerability: hard-coded credentials (python:S6418 / S2068)
PROMO_API_PASSWORD = "P@ssw0rd-super-secret-123"
PROMO_API_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"


def loyalty_bonus(points, is_member):
    # Bug: self-comparison (S1764) and identical branches (S3923)
    if points != points:
        return 0
    return points * 2 if is_member else points * 2


def run_expression(expression):
    # Vulnerability: eval on arbitrary input (S5334)
    return eval(expression)


def seasonal_discount(total, season, unused_flag=None):
    # Code smell: duplicated blocks, high complexity, unused parameter, never tested
    if season == "summer":
        if total > 500:
            return total * 0.3
        elif total > 100:
            return total * 0.2
        elif total > 50:
            return total * 0.1
        return 0
    if season == "winter":
        if total > 500:
            return total * 0.3
        elif total > 100:
            return total * 0.2
        elif total > 50:
            return total * 0.1
        return 0
    if season == "spring":
        if total > 500:
            return total * 0.3
        elif total > 100:
            return total * 0.2
        elif total > 50:
            return total * 0.1
        return 0
    # TODO: handle autumn
    return 0
