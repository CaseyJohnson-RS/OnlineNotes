# Последовательность настройки базы данных

1. Подключаемся к базе данных на провах супер пользователя

2. Запускаем скрипт `CREATION.sql`

```bash
\i /path/to/file/CREATION.sql
```

3. Запускаем скрипт `CREATE_USER_FOR_BACKEND.sql`. Его нет в репозитории, но его вид таков:

```sql
CREATE USER username WITH PASSWORD 'password';

GRANT SELECT, INSERT, UPDATE, DELETE ON "Users", "Error_messages","Reviews","User_note_labels","Notes","Note_assigned_labels" TO username;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO username;
```

4. Запускаем скрипт `INSERT_APP_ADMIN.sql`. Его нет в репозитории, но его вид таков:

```sql
INSERT INTO "Users" (email, nickname, password_hash, active, role_id)
VALUES ('admin@admin.admin', 'Admin', 'password_hash', TRUE, 2);

-- Password: password_hash
```
