# Функции:
# process_bank_search(data, search) -> list[dict[str, Any]] — возвращает операции, у которых в поле description найдено регулярное выражение/строка.
# process_bank_operations(data, categories) -> dict[str, int] — считает попадания категорий на основе description (использует collections.Counter).