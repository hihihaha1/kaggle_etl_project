DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions(
    id SERIAL PRIMARY KEY,
    step INTEGER,
    type VARCHAR(20),
    amount DECIMAL(15, 2),
    name_orig VARCHAR(50),
    old_balance_org DECIMAL(15, 2),
    new_balance_orig DECIMAL(15, 2),
    name_dest VARCHAR(50),
    old_balance_dest DECIMAL(15, 2),
    new_balance_dest DECIMAL(15, 2),
    is_fraud SMALLINT,
    is_flagged_fraud SMALLINT
)