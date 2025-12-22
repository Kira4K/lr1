'''code
tests/test_grammar.py::TestGrammar::test_epsilon_rule PASSED                                                                                               [  9%]
tests/test_grammar.py::TestGrammar::test_get_rules_for PASSED                                                                                              [ 18%]
tests/test_grammar.py::TestGrammar::test_grammar_creation PASSED                                                                                           [ 27%]
tests/test_grammar.py::TestGrammar::test_grammar_validation PASSED                                                                                         [ 36%]
tests/test_grammar_parser.py::TestGrammarParser::test_invalid_input_raises_exception PASSED                                                                [ 45%]
tests/test_grammar_parser.py::TestGrammarParser::test_parse_simple_grammar PASSED                                                                          [ 54%]
tests/test_lr_parser.py::TestLR1Parser::test_arithmetic_expressions_simple PASSED                                                                          [ 63%]
tests/test_lr_parser.py::TestLR1Parser::test_example_from_assignment PASSED                                                                                [ 72%]
tests/test_lr_parser.py::TestLR1Parser::test_simple_balanced_parentheses PASSED                                                                            [ 81%]
tests/test_simple.py::TestSimpleLR1::test_epsilon_grammar_simple PASSED                                                                                    [ 90%]
tests/test_simple.py::TestSimpleLR1::test_simplest_grammar PASSED                                                                                          [100%]

======================================================================= 11 passed in 0.09s =======================================================================



rootdir: /Users/user/PycharmProjects/lr(1)
plugins: cov-5.0.0
collected 11 items                                                                                                                                               

tests/test_grammar.py ....                                                                                                                                 [ 36%]
tests/test_grammar_parser.py ..                                                                                                                            [ 54%]
tests/test_lr_parser.py ...                                                                                                                                [ 81%]
tests/test_simple.py ..                                                                                                                                    [100%]

---------- coverage: platform darwin, python 3.8.1-final-0 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
first_follow.py                  105     26    75%   40, 53-54, 61-62, 96-99, 103-104, 108, 114, 120-129, 132-137, 140
grammar.py                        35      3    91%   43, 47-48
grammar_parser.py                 41      7    83%   13, 24, 29, 36, 53-54, 61
lr_item.py                        34      7    79%   24-27, 40, 44-45
lr_parser.py                     186     22    88%   21, 107, 113-121, 176, 187-192, 195, 199, 229, 238, 250, 256
main.py                           24     24     0%   1-33
quick_test.py                      0      0   100%
tests/__init__.py                  0      0   100%
tests/test_grammar.py             47     16    66%   9-27, 104
tests/test_grammar_parser.py      23      1    96%   43
tests/test_lr_parser.py           72     32    56%   10-36, 65-67, 93-95, 119-121, 125
tests/test_simple.py              72     29    60%   10-32, 65-68, 101-104, 108-109
------------------------------------------------------------
TOTAL                            639    167    74%

'''
# LR(1) Парсер

Реализация LR(1) анализатора для проверки принадлежности слов языку, заданному контекстно-свободной грамматикой.


# Запуск тестов
```bash
python -m pytest tests/ -v
```

# Проверка примера из задания:
```bash
python main.py < input.txt
```

```code
lr_project/
├── grammar.py              Классы Grammar и Rule
├── lr_parser.py            Основной класс LR1Parser
├── lr_item.py              LRItem и LRState
├── first_follow.py         Вычисление FIRST и FOLLOW
├── grammar_parser.py       Парсер входного формата
├── main.py                 Точка входа
├── tests/                  Тесты
│   ├── __init__.py
│   ├── test_grammar.py
|   ├── test_grammar_parser.py
|   ├── test_lr_parser.py
│   └── test_simple.py
├── examples/              Примеры входных данных
│   └── example1.txt
├── input.txt              Пример из задания
└── README.md              Этот файл
```
