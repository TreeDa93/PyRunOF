# PyRunOF

PyRunOF — Python-библиотека для подготовки, копирования и запуска расчётных
кейсов OpenFOAM, а также проведения параметрических исследований.

> Проект не устанавливает OpenFOAM. Команды `pimpleFoam`, `mpirun`, Elmer и
> другие внешние программы должны быть доступны в окружении пользователя.

## Требования

- Python 3.12 или новее;
- [uv](https://docs.astral.sh/uv/);
- установленный OpenFOAM для реальных расчётов;
- Git для совместной разработки.

## Быстрый старт

```bash
git clone git@github.com:TreeDa93/PyRunOF.git
cd PyRunOF
uv sync --locked --extra dev
uv run pytest
```

`uv sync` создаёт локальное окружение `.venv` и устанавливает проект в
редактируемом виде. Активировать окружение вручную не обязательно: команды
можно запускать через `uv run`.

Минимальный пример полного перебора параметров:

```python
from pyRunOF.sweep import ParametricSweep, SweepPoint


def calculate(point: SweepPoint) -> float:
    print(point.index, point.name, point.parameters)
    return point.parameters["velocity"] * 2


sweep = ParametricSweep(
    {"velocity": [1, 2], "turbulence_model": ["kEpsilon", "kOmegaSST"]},
    mode="product",
)
results = sweep.run(calculate, progress=True)
```

Параметры можно сопоставлять попарно. В режиме `zip` длины списков должны
совпадать, поэтому случайная потеря вариантов сразу обнаруживается:

```python
from pyRunOF.sweep import ParametricSweep

sweep = ParametricSweep(
    {"velocity": [1, 2], "model": ["kEpsilon", "kOmegaSST"]},
    mode="zip",
)

for point in sweep:
    print(point.index, point.parameters, point.name)
```

Запуск OpenFOAM-кейса:

```python
from pyRunOF import Run

runner = Run(case_path="cases/channel", solver="pimpleFoam")
runner.set_log_flag(True)
result = runner.run(timeout=3600)
print(result.returncode)
```

Параллельный режим:

```python
runner = Run(
    case_path="cases/channel",
    solver="pimpleFoam",
    mode="parallel",
    OF_core=8,
)
runner.run()
```

Единая конфигурация и фасад кейса:

```python
from pyRunOF import CaseConfig, OpenFOAMCase, Run

config = CaseConfig(key="channel", case_path="cases/channel")
runner = Run(config=config, solver="pimpleFoam")

case = OpenFOAMCase("cases/channel")
case.runner.set_solver_name("pimpleFoam")
case.mesh.run_blockMesh()
case.runner.run()
```

Экспорт всех словарей кейса в один JSON-файл:

```python
from pyRunOF import OpenFOAMCase

case = OpenFOAMCase("cases/channel")
settings = case.parser.parse()
json_path = case.parser.save("case-config.json")
```

Полученный словарь или JSON можно изменить и применить к другому кейсу:

```python
settings["system"]["controlDict"]["endTime"] = 500
settings["constant"]["transportProperties"]["nu"] = 2e-5
settings["initial_conditions"]["U"]["boundaryField"]["inlet"]["value"] = (
    "uniform (2 0 0)"
)

report = case.parser.apply(settings)
print(report["updated"])

# Или непосредственно из файла:
case.parser.apply("case-config.json")
```

При записи каждый конечный параметр преобразуется в команду вида
`foamDictionary -entry <путь> -set <значение> <файл>`. Изменять разрешено
только существующие файлы внутри `0`, `constant` и `system`; запись в
`constant/polyMesh` и выход за пределы кейса блокируются.

Парсер читает через `foamDictionary`:

- все поля из папки `0`, включая `internalField`, названия границ и их
  граничные условия из `boundaryField`;
- все словари из `constant`, кроме содержимого `polyMesh`;
- все словари из `system`, включая словари во вложенных каталогах.

По умолчанию ошибка разбора любого файла останавливает экспорт. Для старых или
нестандартных словарей можно использовать `parse(strict=False)` — тогда ошибка
будет записана около соответствующего файла в поле `_parse_error`.

`CaseConfig` рекомендуется для нового кода. Исторический аргумент `info` и
импорты из `pyRunOF.modules` пока поддерживаются для обратной совместимости.

## Где что редактировать

```text
PyRunOF/
├── pyRunOF/
│   ├── modules/          # публичные операции с кейсами и расчётами
│   ├── case/             # единая конфигурация CaseConfig
│   ├── openfoam/         # OpenFOAM API и фасад OpenFOAMCase
│   ├── elmer/            # Elmer API
│   ├── sweep/            # параметрические исследования
│   ├── postprocessing/   # обработка результатов
│   ├── _internal/        # непубличные команды, пути и файловые операции
│   ├── modules/          # переходные исторические импорты
│   ├── additional_fun/   # переходные вспомогательные импорты
│   ├── files/            # поставляемые шаблоны OpenFOAM
│   ├── exceptions.py     # публичные исключения
│   └── __init__.py       # публичный API и версия
├── tests/
│   ├── unit/             # быстрые автоматические тесты
│   └── ...               # примеры и тяжёлые OpenFOAM-кейсы
├── .github/workflows/    # проверки GitHub Actions
├── pyproject.toml        # зависимости, сборка и настройки инструментов
└── uv.lock               # точные версии зависимостей
```

Основные точки расширения:

- `modules/model_config.py` — создание, копирование и удаление каталогов кейсов;
- `modules/run.py` — формирование и безопасный запуск внешних команд;
- `modules/parametric_sweep.py` — комбинации параметров и callback расчёта;
- `modules/constant.py`, `initial_values.py`, `set_system.py` — изменение
  OpenFOAM-словарей;
- `modules/meshes.py` и `post_process.py` — сетки и обработка результатов.

Имя дистрибутива в PyPI/uv — `pyrunof`, а исторический Python-импорт пока
сохранён как `pyRunOF` для совместимости со старыми скриптами.

## Рабочий процесс разработчика

После получения изменений коллеги:

```bash
git pull --rebase
uv sync --locked --extra dev
```

Перед коммитом:

```bash
uv run ruff format pyRunOF tests/unit
uv run ruff check pyRunOF tests/unit
uv run pytest --cov=pyRunOF --cov-report=term-missing
uv build
```

Добавление обычной зависимости:

```bash
uv add package-name
```

Добавление инструмента разработки:

```bash
uv add --optional dev package-name
```

После изменения зависимостей коммитьте одновременно `pyproject.toml` и
`uv.lock`. Каталог `.venv` в Git не добавляется.

## Безопасность файловых операций

- Существующие каталоги никогда не перезаписываются по умолчанию.
- Для явной замены требуется `rewrite=True`.
- Рекурсивное удаление разрешено только внутри переданного рабочего каталога.
- Символические ссылки рекурсивно не удаляются.
- Имя solver проверяется и не передаётся через shell.

Перед запуском на ценных расчётах рекомендуется хранить исходный кейс под Git
или иметь резервную копию результатов.

## Тесты и CI

Быстрые unit-тесты не требуют OpenFOAM:

```bash
uv run pytest
```

Каталоги с полноценными CFD-кейсами сохранены как примеры и будущие
интеграционные тесты. Они не запускаются автоматически, потому что требуют
отдельно установленного OpenFOAM. GitHub Actions проверяет линтер, unit-тесты и
сборку пакета при каждом pull request.

## Сборка

```bash
uv build
```

Артефакты wheel и sdist появятся в `dist/`. Публикация выполняется отдельно и
не требуется для установки проекта из Git.
