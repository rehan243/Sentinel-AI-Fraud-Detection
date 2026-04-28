-- Core fraud storage — partition by month in prod, this is the polite version
CREATE TABLE IF NOT EXISTS customers (
    customer_id UUID PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    risk_tier TEXT NOT NULL DEFAULT 'standard'
);

CREATE TABLE IF NOT EXISTS transactions (
    txn_id UUID PRIMARY KEY,
    customer_id UUID NOT NULL REFERENCES customers (customer_id),
    amount NUMERIC(18, 4) NOT NULL,
    currency CHAR(3) NOT NULL,
    merchant_id TEXT NOT NULL,
    mcc CHAR(4) NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    device_fp_hash TEXT,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION
) PARTITION BY RANGE (occurred_at);

CREATE INDEX IF NOT EXISTS idx_txn_customer_time ON transactions (customer_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_txn_merchant ON transactions (merchant_id);

CREATE TABLE IF NOT EXISTS model_versions (
    version_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    artifact_uri TEXT NOT NULL,
    deployed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_active BOOLEAN NOT NULL DEFAULT false
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_model_active ON model_versions (name) WHERE is_active;

CREATE TABLE IF NOT EXISTS fraud_scores (
    score_id BIGSERIAL PRIMARY KEY,
    txn_id UUID NOT NULL REFERENCES transactions (txn_id),
    model_version_id INT REFERENCES model_versions (version_id),
    score REAL NOT NULL,
    features JSONB NOT NULL,
    scored_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_scores_txn ON fraud_scores (txn_id);
CREATE INDEX IF NOT EXISTS idx_scores_time ON fraud_scores (scored_at DESC);

CREATE TABLE IF NOT EXISTS rules (
    rule_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    expression TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    priority INT NOT NULL DEFAULT 100
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    txn_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    outcome TEXT NOT NULL,
    reasons TEXT[] NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);
CREATE INDEX IF NOT EXISTS idx_alerts_customer ON alerts (customer_id, created_at DESC);

CREATE TABLE IF NOT EXISTS feature_store (
    entity_id UUID NOT NULL,
    feature_set TEXT NOT NULL,
    values JSONB NOT NULL,
    as_of TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (entity_id, feature_set, as_of)
);
CREATE INDEX IF NOT EXISTS idx_feature_store_asof ON feature_store (as_of DESC);
