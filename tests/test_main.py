from sonar_template_python.__main__ import main


def test_main_prints_greeting_and_count(capsys):
    assert main(["Ada", "--count", "2"]) == 0
    assert capsys.readouterr().out == "Hello, Ada!\nCount: 2\n"


def test_main_defaults(capsys):
    assert main([]) == 0
    assert capsys.readouterr().out == "Hello, world!\nCount: 0\n"
