import argparse

from sonar_template_python.counter import Counter
from sonar_template_python.greeting import greet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tiny demo CLI for the SonarQube template.")
    parser.add_argument("name", nargs="?", default="", help="who to greet")
    parser.add_argument("--count", type=int, default=0, help="how many times to increment")
    args = parser.parse_args(argv)

    counter = Counter()
    for _ in range(args.count):
        counter.increment()

    print(greet(args.name))
    print(f"Count: {counter.count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
