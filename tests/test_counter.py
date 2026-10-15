from sonar_template_python import Counter


def test_starts_at_initial_value():
    assert Counter(5).count == 5


def test_increment_and_decrement():
    counter = Counter()
    assert counter.increment() == 1
    assert counter.increment() == 2
    assert counter.decrement() == 1


def test_reset_returns_to_initial_value():
    counter = Counter(3)
    counter.increment()
    assert counter.reset() == 3
