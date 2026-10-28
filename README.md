# Эмулятор оболочки ОС (Вариант 24)

## 1. Общее описание

Проект представляет собой эмулятор командной строки UNIX-подобной операционной системы, реализованный на языке Python 3. Эмулятор работает с виртуальной файловой системой (VFS), загружаемой из JSON-файла, и поддерживает выполнение команд как в интерактивном режиме (REPL), так и пакетно через стартовые скрипты.

**Ключевые особенности:**

- Консольный интерфейс (CLI) с приглашением, содержащим имя текущей VFS.
- Поддержка раскрытия переменных окружения реальной ОС (`$VAR`, `${VAR}`).
- Виртуальная файловая система хранится в памяти, источник — JSON-файл.
- Двоичные файлы кодируются в формате base64.
- Обработка ошибок загрузки VFS и выполнения скриптов.
- Имитация диалога пользователя с системой при запуске скриптов.

**Реализованные этапы:**

| Этап | Название | Описание |
|------|----------|----------|
| 1 | REPL | CLI, приглашение с именем VFS, парсер с раскрытием переменных окружения, заглушки `ls` и `cd`, команда `exit`, обработка ошибок |
| 2 | Конфигурация | Параметры `--vfs` и `--script`, выполнение стартовых скриптов с комментариями, имитация диалога, обработка ошибочных строк |
| 3 | VFS | Загрузка дерева VFS из JSON, текстовое и base64-содержимое, обработка ошибок загрузки, тестовые сценарии |

---

## 2. Описание функций и настроек

### Параметры командной строки

| Параметр | Тип | Значение по умолчанию | Назначение |
|----------|-----|------------------------|------------|
| `--vfs` | строка | пустая VFS в памяти | Путь к JSON-файлу виртуальной ФС |
| `--script` | строка | интерактивный режим | Путь к стартовому скрипту |

### Поддерживаемые команды эмулятора

| Команда | Описание |
|---------|----------|
| `ls` | Заглушка: выводит имя команды и переданные аргументы |
| `cd` | Заглушка: выводит имя команды и переданные аргументы |
| `echo` | Выводит аргументы с раскрытыми переменными окружения |
| `exit` | Завершает работу эмулятора |
| Неизвестная команда | Выводит сообщение об ошибке `[ERROR] Unknown command: <имя>` |

### Поведение парсера

- Разделяет ввод на команду и аргументы по пробелам.
- Корректно обрабатывает аргументы в одинарных и двойных кавычках.
- Раскрывает переменные окружения реальной ОС: `$VAR` и `${VAR}`.
- Неизвестная переменная окружения оставляется в строке без изменений.
- Сообщает о неверных аргументах команд.

### Формат VFS (JSON)

Виртуальная файловая система описывается в JSON-файле со следующей структурой:

```json
{
  "name": "root",
  "is_dir": true,
  "children": [
    {
      "name": "file.txt",
      "is_dir": false,
      "is_binary": false,
      "content": "Текстовое содержимое файла"
    },
    {
      "name": "image.bin",
      "is_dir": false,
      "is_binary": true,
      "content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAA..."
    },
    {
      "name": "subdir",
      "is_dir": true,
      "children": []
    }
  ]
}
```

**Поля узлов:**

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | строка | Имя файла или директории |
| `is_dir` | bool | `true` — директория, `false` — файл |
| `content` | строка | Содержимое файла (текст или base64 для бинарных) |
| `is_binary` | bool | `true`, если `content` закодирован в base64 |
| `children` | массив | Список дочерних узлов (только для директорий) |

### Стартовый скрипт

- Поддерживает комментарии (синтаксис `#`).
- При выполнении на экран выводится и ввод, и вывод (имитация диалога).
- Ошибочные строки пропускаются с выводом сообщения об ошибке.
- Выполнение продолжается до конца файла или команды `exit`.

### Обработка ошибок

| Ситуация | Реакция |
|----------|---------|
| Файл VFS не существует | `[ERROR] VFS file not found: <путь>`, выход с кодом 1 |
| Некорректный JSON | `[ERROR] Invalid JSON format in VFS: <путь>`, выход с кодом 1 |
| Файл скрипта не найден | `[ERROR] Script file not found: <путь>` |
| Неизвестная команда | `[ERROR] Unknown command: <имя>` |
| Неверные аргументы `cd` | `[ERROR] cd: invalid arguments. Usage: cd <path>` |
| Ctrl+C или EOF в REPL | Корректное завершение работы |

---

## 3. Команды для сборки и запуска тестов

### Требования

- Python 3.6 или выше.
- Bash и Git.
- Сторонние Python-пакеты не требуются.

### Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<username>/os-shell-emulator.git
cd os-shell-emulator

# 2. Сделать скрипты исполняемыми
chmod +x run.sh tests/run_tests.sh

# 3. Запуск в интерактивном режиме
./run.sh

# 4. Запуск с VFS и стартовым скриптом
./run.sh --vfs tests/test_vfs_complex.json --script tests/test_all.sh

# 5. Запуск всех тестов
./tests/run_tests.sh
```

### Структура репозитория

```text
.
├── .gitignore
├── README.md
├── run.sh
├── src/
│   └── emulator.py
└── tests/
    ├── run_tests.sh
    ├── test_all.sh
    ├── test_script1.sh
    ├── test_script2.sh
    ├── test_vfs_minimal.json
    └── test_vfs_complex.json
```

### Состав тестов

| Файл | Назначение |
|------|------------|
| `test_vfs_minimal.json` | Минимальная VFS: пустой корень |
| `test_vfs_complex.json` | Вложенность более двух уровней и base64-файл |
| `test_script1.sh` | Заглушки, комментарии, неизвестная команда, `exit` |
| `test_script2.sh` | Переходы по вложенным путям VFS |
| `test_all.sh` | Все режимы: переменные, аргументы, ошибки, VFS |
| `run_tests.sh` | Прогон всех сценариев, включая ошибки загрузки VFS |

### История коммитов (Conventional Commits)

```bash
# Этап 1: REPL
git commit -m "feat(repl): add cli interface, env var expansion and command stubs"

# Этап 2: Конфигурация
git commit -m "feat(config): add argparse for vfs/script paths and script execution"

# Этап 3: VFS
git commit -m "feat(vfs): implement json vfs loading with base64 support and test suites"
```

---

## 4. Примеры использования

### Пример 1: Интерактивный режим

```text
$ ./run.sh
Emulator started. VFS: default_vfs
[default_vfs /]$ echo $HOME
/home/user
[default_vfs /]$ echo "User: ${USER}"
User: student
[default_vfs /]$ ls -l
Executing stub: ls with args ['-l']
[default_vfs /]$ cd /home
Executing stub: cd with args ['/home']
[default_vfs /]$ cd
[ERROR] cd: invalid arguments. Usage: cd <path>
[default_vfs /]$ unknown_cmd
[ERROR] Unknown command: unknown_cmd
[default_vfs /]$ exit
Exiting emulator.
```

### Пример 2: Запуск со скриптом и VFS

```text
$ ./run.sh --vfs tests/test_vfs_complex.json --script tests/test_all.sh
[DEBUG] VFS loaded from tests/test_vfs_complex.json
[test_vfs_complex.json]$ echo $HOME
/home/user
[test_vfs_complex.json]$ ls -la /
Executing stub: ls with args ['-la', '/']
[test_vfs_complex.json]$ cd /dir1
Executing stub: cd with args ['/dir1']
[test_vfs_complex.json]$ invalid_command --flag
[ERROR] Unknown command: invalid_command
Exiting emulator.
```

### Пример 3: Обработка ошибок загрузки VFS

**Файл не найден:**

```text
$ ./run.sh --vfs nonexistent.json
[ERROR] Failed to load VFS: VFS file not found: nonexistent.json
```

**Неверный формат JSON:**

```text
$ ./run.sh --vfs tests/invalid.json
[ERROR] Failed to load VFS: Invalid JSON format in VFS: tests/invalid.json
```

### Пример 4: Выполнение стартового скрипта с комментариями

Содержимое `tests/test_script1.sh`:

```bash
# Test script 1: Basic commands and comments
ls -l /
cd /home
# Another comment testing
unknown_command arg1 arg2
exit
```

Результат выполнения:

```text
$ ./run.sh --script tests/test_script1.sh
[test_script1.sh]$ ls -l /
Executing stub: ls with args ['-l', '/']
[test_script1.sh]$ cd /home
Executing stub: cd with args ['/home']
[test_script1.sh]$ unknown_command arg1 arg2
[ERROR] Unknown command: unknown_command
Exiting emulator.
```

### Пример 5: Прогон всех тестов

```text
$ ./tests/run_tests.sh
=== Test 1: Minimal VFS ===
[DEBUG] VFS loaded from tests/test_vfs_minimal.json
...
=== Test 2: Complex VFS (3 levels) ===
[DEBUG] VFS loaded from tests/test_vfs_complex.json
...
=== Test 3: VFS Load Error (File not found) ===
[ERROR] Failed to load VFS: VFS file not found: tests/nonexistent.json
...
=== Test 4: VFS Load Error (Invalid format) ===
[ERROR] Failed to load VFS: Invalid JSON format in VFS: tests/invalid.json
...
=== All tests completed ===
```
