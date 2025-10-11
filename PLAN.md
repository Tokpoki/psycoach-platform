# План работ по MVP

Работа ведётся в ветке `feature/mvp`. Коммиты в `main` не выполняем.

## Дорожная карта (12 шагов)

1. **Сбор уточнённых требований и согласование архитектуры**  
   - Цель: на основе `TECHNICAL_SPECIFICATION.md` и README зафиксировать пользовательские роли, сценарии и минимальные потоки (регистрация, выбор роли, прохождение сценария, подсчёт очков).  
   - Файлы: `README.md`, `docs/TECHNICAL_SPECIFICATION.md` (создать при необходимости), `docs/architecture.md`.  
   - Риски: неполные входные данные от психологов и продуктовой команды; возможная корректировка MVP после интервью.

2. **Структурирование монорепозитория и базовой автоматизации**  
   - Цель: создать каталоги `backend/` и `android/`, настроить общие pre-commit хуки, линтеры и GitHub Actions.  
   - Файлы: `.pre-commit-config.yaml`, `.github/workflows/backend.yml`, `.github/workflows/android.yml`, `backend/pyproject.toml`, `android/build.gradle`.  
   - Риски: конфликты зависимостей Python/Kotlin, время на отладку CI.

3. **Проектирование схемы данных PostgreSQL**  
   - Цель: определить таблицы пользователей, ролей, сценариев, вариантов ответов, прогресса и курсов, соответствующие MVP.  
   - Файлы: `backend/app/db/models.py`, `backend/app/db/schemas.py`, `backend/migrations/versions/*.py`, `docs/db_schema.md`.  
   - Риски: упущенные связи (например, достижения, мини-игры), необходимость пересоздания миграций.

4. **Настройка FastAPI-приложения и инфраструктуры БД**  
   - Цель: развернуть каркас приложения, конфигурацию окружения, Alembic, Docker Compose для локальной разработки.  
   - Файлы: `backend/app/main.py`, `backend/app/config.py`, `backend/alembic.ini`, `docker-compose.yml`.  
   - Риски: сложности с согласованием окружений разработчиков, ошибки подключения к БД.

5. **Регистрация, выбор роли и аутентификация**  
   - Цель: реализовать API регистрации с выбором роли (спортсмен, тренер, родитель), вход и выдачу JWT-токенов.  
   - Файлы: `backend/app/api/v1/auth.py`, `backend/app/services/auth.py`, `backend/app/core/security.py`.  
   - Риски: безопасность (хеширование паролей, refresh-токены), корректное хранение ролей.

6. **Сценарии и расчёт прогресса**  
   - Цель: создать эндпоинты выдачи сценариев, приёма ответов, расчёта очков и уровней с учётом эмоциональных навыков.  
   - Файлы: `backend/app/api/v1/scenarios.py`, `backend/app/services/scenarios.py`, `backend/app/services/progress.py`.  
   - Риски: сложная бизнес-логика (баланс очков, объяснения), расширяемость для будущих мини-игр.

7. **API курсов и демо-контента**  
   - Цель: реализовать выдачу тестового курса «Как справиться с волнением перед стартом» и связать его со сценариями.  
   - Файлы: `backend/app/api/v1/courses.py`, `backend/app/services/courses.py`, `backend/app/db/models.py`.  
   - Риски: изменение структуры курсов, необходимость дополнительного контента.

8. **Seed-данные и скрипты наполнения**  
   - Цель: подготовить JSON/YAML с 1–2 сценариями, эмоциями и курсом; реализовать скрипт импорта в БД.  
   - Файлы: `backend/app/seed/__init__.py`, `backend/app/seed/data/*.json`, `backend/scripts/load_seed.py`.  
   - Риски: несогласованность с психологами, поддержка версионности данных.

9. **Тестирование backend**  
   - Цель: покрыть юнит- и интеграционные тесты (pytest, FastAPI TestClient, PostgreSQL в контейнере) для auth, сценариев, курсов и seed.  
   - Файлы: `backend/tests/test_auth.py`, `backend/tests/test_scenarios.py`, `backend/tests/test_courses.py`, `backend/tests/conftest.py`.  
   - Риски: медленные интеграционные тесты, необходимость моков для внешних сервисов.

10. **Инициализация Android-проекта на Kotlin**  
    - Цель: настроить модуль `app`, зависимости (Jetpack Compose/Views, Retrofit/Ktor, Hilt/Koin), навигацию и модели данных.  
    - Файлы: `android/app/build.gradle.kts`, `android/app/src/main/AndroidManifest.xml`, `android/app/src/main/java/.../App.kt`.  
    - Риски: несовместимость версий Android Gradle Plugin, сложность CI для Gradle.

11. **Ключевые экраны Android-клиента**  
    - Цель: реализовать UI и взаимодействие с API для регистрации/выбора роли, списка сценариев, прохождения сценария, экрана прогресса и курса.  
    - Файлы: `android/app/src/main/java/.../ui/auth/*`, `.../ui/scenarios/*`, `.../ui/progress/*`, `android/app/src/main/res/*`.  
    - Риски: UX на разных устройствах, офлайн-кэш, обработка сетевых ошибок.

12. **Тесты Android и подготовка демо**  
    - Цель: настроить unit-тесты (JUnit), UI-тесты (Espresso/Compose Testing), интеграцию с backend на стенде; подготовить сценарий демонстрации с тестовыми аккаунтами.  
    - Файлы: `android/app/src/test/java/...`, `android/app/src/androidTest/java/...`, `docs/demo_instructions.md`, `docs/test_report.md`.  
    - Риски: нестабильные эмуляторы, необходимость мок-сервера для автотестов, ограничение времени на полировку демо.

