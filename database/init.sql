-- Initialize pgvector and required schema extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Log initialization
COMMENT ON DATABASE datacentre_epc IS 'AI Intelligence Platform for Data Centre EPC Project Delivery';
