import sys
from grammar_parser import GrammarParser
from lr_parser import LR1Parser


def main():
    try:
        grammar, words = GrammarParser.parse_from_stdin()

        parser = LR1Parser()

        try:
            parser.fit(grammar)
        except ValueError as e:
            print(f"Grammar is not LR(1): {e}", file=sys.stderr)
            sys.exit(1)

        for word in words:
            try:
                if parser.predict(word):
                    print("Yes")
                else:
                    print("No")
            except Exception:
                print("No")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()