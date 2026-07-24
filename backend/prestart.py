"""Подготовка базы данных перед запуском приложения.

Скрипт делает применение миграций Alembic безопасным независимо от того, как
раньше управлялась база:

1. База уже под управлением Alembic (есть таблица alembic_version)
   -> просто `alembic upgrade head`.

2. Таблицы есть, но истории Alembic нет (базу раньше строил только create_all)
   -> помечаем базу предыдущей ревизией (stamp) и затем `upgrade head`,
      чтобы Alembic не пытался заново создавать уже существующие объекты.

3. База пустая (первый запуск)
   -> создаём все таблицы из моделей и помечаем базу как head.

Запускается из entrypoint.sh до старта uvicorn.
"""

import os

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect
from sqlmodel import SQLModel

# Регистрируем все модели в метаданных SQLModel.
import notes.models  # noqa: F401
import tags.models  # noqa: F401
import tasks.models  # noqa: F401
import users.models  # noqa: F401


# Ревизия, соответствующая схеме до появления title/тегов у задач.
# Это последняя миграция, которую даёт «старый» create_all-снимок базы.
BASELINE_REVISION = "dac6eb355023"


def main() -> None:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    engine = create_engine(database_url)

    tables = set(inspect(engine).get_table_names())
    has_alembic_history = "alembic_version" in tables
    has_app_tables = "task" in tables

    alembic_cfg = Config("alembic.ini")

    if has_alembic_history:
        print("prestart: база под управлением Alembic — применяем миграции.")
        command.upgrade(alembic_cfg, "head")
    elif has_app_tables:
        print(
            "prestart: таблицы есть, но истории Alembic нет — "
            f"помечаем базу как {BASELINE_REVISION} и обновляем до head."
        )
        command.stamp(alembic_cfg, BASELINE_REVISION)
        command.upgrade(alembic_cfg, "head")
    else:
        print("prestart: пустая база — создаём таблицы и помечаем как head.")
        SQLModel.metadata.create_all(engine)
        command.stamp(alembic_cfg, "head")

    print("prestart: база готова.")


if __name__ == "__main__":
    main()
