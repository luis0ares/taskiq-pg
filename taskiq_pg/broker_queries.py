CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS {} (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR NOT NULL,
    task_name VARCHAR NOT NULL,
    message TEXT NOT NULL,
    labels JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    locked BOOLEAN DEFAULT FALSE
);
"""

INSERT_MESSAGE_QUERY = """
INSERT INTO {} (task_id, task_name, message, labels)
VALUES ($1, $2, $3, $4)
RETURNING id
"""

SELECT_MESSAGE_QUERY = """
UPDATE {0}
SET locked = TRUE
WHERE id = (
    SELECT id
    FROM {0}
    WHERE locked = FALSE AND id = $1
    FOR UPDATE SKIP LOCKED
    LIMIT 1
)
RETURNING *;
"""

DELETE_MESSAGE_QUERY = "DELETE FROM {} WHERE id = $1"

UPDATE_MESSAGE_QUERY = """
UPDATE {} SET locked = FALSE WHERE id = $1
"""

NOTIFY_STORED_MESSAGES = """
DO $$
DECLARE
    msg RECORD;
BEGIN
    FOR msg IN
        SELECT id FROM {table} WHERE locked = FALSE
    LOOP
        PERFORM pg_notify({channel}, msg.id::text);
    END LOOP;
END $$;
"""