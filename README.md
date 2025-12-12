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
