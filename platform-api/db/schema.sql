CREATE TABLE deployments (
    id UUID PRIMARY KEY,
    cloud TEXT NOT NULL,
    environment TEXT NOT NULL,
    application TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE deployment_events (
    id SERIAL PRIMARY KEY,
    deployment_id UUID NOT NULL REFERENCES deployments(id) ON DELETE CASCADE,
    status TEXT NOT NULL,
    time TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_events_deployment_id
ON deployment_events(deployment_id);