import pytest

from sonar_template_python import greet


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ada", "Hello, Ada!"),
        ("  Ada  ", "Hello, Ada!"),
        ("", "Hello, world!"),
        ("   ", "Hello, world!"),
    ],
)
def test_greet(name, expected):
    assert greet(name) == expected
