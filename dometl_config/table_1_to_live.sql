INSERT INTO table_1 (
    "id", "col_1"
    )
SELECT
    id,
    col_1
FROM table_1_st
ON CONFLICT (id) DO NOTHING;
