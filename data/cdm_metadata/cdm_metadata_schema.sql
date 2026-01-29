-- ENIGMA CDM Metadata Catalog Tables
-- Generated from parquet metadata

CREATE OR REPLACE TABLE cdm_column_metadata (
  table_name VARCHAR NOT NULL,
  table_category VARCHAR NOT NULL,
  column_name VARCHAR NOT NULL,
  column_type VARCHAR,
  description TEXT,
  microtype VARCHAR,
  units VARCHAR,
  is_primary_key BOOLEAN DEFAULT FALSE,
  is_unique_key BOOLEAN DEFAULT FALSE,
  is_foreign_key BOOLEAN DEFAULT FALSE,
  fk_references VARCHAR,
  is_required BOOLEAN DEFAULT FALSE,
  is_nullable BOOLEAN DEFAULT TRUE,
  constraint_pattern VARCHAR,
  original_name VARCHAR,
  field_type VARCHAR,
  PRIMARY KEY (table_name, column_name)
);

CREATE OR REPLACE TABLE cdm_table_metadata (
  table_name VARCHAR PRIMARY KEY,
  table_category VARCHAR NOT NULL,
  total_rows BIGINT,
  num_columns INTEGER,
  num_primary_keys INTEGER,
  num_foreign_keys INTEGER,
  num_unique_keys INTEGER,
  num_required_columns INTEGER,
  description TEXT
);

CREATE OR REPLACE TABLE cdm_validation_rules (
  table_name VARCHAR NOT NULL,
  column_name VARCHAR NOT NULL,
  validation_type VARCHAR NOT NULL,
  validation_pattern VARCHAR,
  description TEXT,
  microtype VARCHAR
);

CREATE OR REPLACE TABLE cdm_microtype_catalog (
  microtype VARCHAR PRIMARY KEY,
  usage_count INTEGER,
  tables VARCHAR[],
  columns VARCHAR[],
  example_description TEXT
);

CREATE OR REPLACE TABLE cdm_relationship_catalog (
  source_table VARCHAR NOT NULL,
  source_column VARCHAR NOT NULL,
  target_table VARCHAR NOT NULL,
  target_column VARCHAR,
  relationship_type VARCHAR,
  is_required BOOLEAN,
  description TEXT
);

-- Indexes for fast searching
CREATE INDEX idx_column_description ON cdm_column_metadata(description);
CREATE INDEX idx_column_microtype ON cdm_column_metadata(microtype);
CREATE INDEX idx_validation_table ON cdm_validation_rules(table_name);
