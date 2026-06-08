CREATE_CHAT_MAPPING_DATA_TABLE_SQL_QUERY = """
CREATE TABLE IF NOT EXISTS chat_web_mapping (
    web_chat_id INTEGER,
    telegram_thread_id INTEGER,
    PRIMARY KEY (web_chat_id, telegram_thread_id)
);
"""

ADD_NEW_CHAT_MAPPING_DATA_SQL_QUERY = """
INSERT INTO chat_web_mapping (web_chat_id, telegram_thread_id) VALUES (
    ?, ?
);
"""

GET_CHAT_MAPPING_DATA_BY_TELEGRAM_THREAD_ID_SQL_QUERY = """
SELECT web_chat_id, telegram_thread_id FROM chat_web_mapping WHERE
telegram_thread_id = ?
LIMIT 1
"""

GET_CHAT_MAPPING_DATA_BY_WEB_ID_SQL_QUERY = """
SELECT web_chat_id, telegram_thread_id FROM chat_web_mapping
WHERE web_chat_id = ?
LIMIT 1
"""

GET_CHAT_MAPPING_DATA_COUNT_SQL_QUERY = """
SELECT COUNT(*) FROM chat_web_mapping
WHERE web_chat_id = ? OR telegram_thread_id = ?
"""

DELETE_CHAT_MAPPING_DATA_BY_TELEGRAM_THREAD_ID_SQL_QUERY = """
DELETE FROM chat_web_mapping
WHERE telegram_thread_id = ?
"""

DELETE_CHAT_MAPPING_DATA_BY_WEB_CHAT_ID_SQL_QUERY = """
DELETE FROM chat_web_mapping
WHERE web_chat_id = ?
"""
