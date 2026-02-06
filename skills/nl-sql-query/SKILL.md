---
name: nl-sql-query
description: Query the CDM DuckDB database using natural language. Use this skill when the user wants to query the linkml-coral CDM database with questions in plain English instead of writing SQL. The skill translates natural language to SQL using Claude API and returns formatted results.
---

# Natural Language SQL Query for CDM Database

Query the KBase CDM DuckDB database using natural language questions. This skill translates your questions to SQL and executes them against the database.

## When to Use This Skill

Use this skill when:
- User asks to query the CDM database with natural language
- User wants to explore data without writing SQL
- User asks questions like "How many samples are there?" or "Show me reads with high counts"
- User wants to invoke `/nl-sql-query` command

## Prerequisites

Before using this skill:
1. **CDM Database**: Must exist at `cdm_store.db` (or specify custom path)
2. **API Key**: `ANTHROPIC_API_KEY` environment variable must be set
3. **Load Data**: Run `just load-cdm-store-bricks-64gb` if database doesn't exist

## How It Works

1. **Schema Inspection**: Reads database schema (tables, columns, types, counts)
2. **AI Translation**: Sends question + schema to Claude API
3. **SQL Generation**: Claude generates optimized DuckDB SQL
4. **Execution**: Runs query and formats results
5. **Display**: Returns results in clean table format or JSON

## Usage

### Basic Query

```bash
just cdm-nl-query "How many samples are there?"
```

### JSON Output

```bash
just cdm-nl-query-json "List all locations with sample counts"
```

### Verbose (See Generated SQL)

```bash
just cdm-nl-query-verbose "Find reads with read_count over 50000"
```

### Direct Python Usage

```bash
uv run python scripts/cdm_analysis/nl_sql_query.py \
  --db cdm_store.db \
  "Show me the top 10 samples by depth"
```

## Example Queries

**Quick Examples:**
- "How many samples are in the database?"
- "Find samples with depth greater than 100"
- "Show me the top 10 locations by sample count"
- "List reads with read_count over 50000"

**For complete examples**: See EXAMPLES.md for 50+ example queries covering:
- Basic statistics and counts
- Filtered queries (numeric, string, date)
- Aggregations and grouping
- Joins and relationships
- Complex queries with subqueries
- Domain-specific analysis (sequencing, taxonomy, geography)
- Data quality and validation queries

## Database Schema Overview

The CDM database contains these main table types:

### Static Entity Tables (sdt_*)
- `sdt_location`: Geographic locations
- `sdt_sample`: Sample metadata
- `sdt_reads`: Sequencing reads data
- `sdt_assembly`: Genome assemblies
- `sdt_genome`: Genome annotations
- `sdt_gene`: Gene predictions
- `sdt_otu` (ASV): 16S amplicon sequence variants

### System Tables (sys_*)
- `sys_oterm`: Ontology terms
- `sys_type_def`: Type definitions
- `sys_process`: Processing records

### Dynamic Tables (ddt_*)
- `ddt_brick*`: Measurement array data (21 brick tables)

## Common Foreign Keys

- `sample_id`: Links to samples
- `location_id`: Links to locations
- `reads_id`: Links to reads
- `assembly_id`: Links to assemblies
- `genome_id`: Links to genomes

## Output Formats

### Text Format (Default)
```
Natural Query: How many samples are there?

Generated SQL:
SELECT COUNT(*) as total_samples FROM sdt_sample

Results (1 rows):
total_samples
-------------
1523
```

### JSON Format
```json
{
  "natural_query": "How many samples are there?",
  "sql_query": "SELECT COUNT(*) as total_samples FROM sdt_sample",
  "result_count": 1,
  "results": [
    {"total_samples": 1523}
  ]
}
```

## Implementation Steps

When user invokes this skill:

1. **Check Prerequisites**
   ```bash
   # Verify database exists
   ls -l cdm_store.db || ls -l cdm_store_bricks_full.db

   # Check API key
   echo $ANTHROPIC_API_KEY | grep -q "sk-" && echo "✓ API key set" || echo "✗ Set ANTHROPIC_API_KEY"
   ```

2. **Execute Query**
   ```bash
   just cdm-nl-query "USER_QUESTION_HERE"
   ```

3. **Handle Results**
   - Display results to user
   - If query fails, show generated SQL and error
   - Suggest fixes if SQL is invalid

## Error Handling

**Database Not Found:**
```bash
# Load the database first
just load-cdm-store-bricks-64gb
```

**API Key Missing:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Invalid SQL Generated:**
- Run with `--verbose` to see generated SQL
- Check if table/column names are correct
- Rephrase the question more specifically

## Advanced Options

### Custom Database Path
```bash
uv run python scripts/cdm_analysis/nl_sql_query.py \
  --db /path/to/custom.db \
  "your question"
```

### Custom API Key
```bash
uv run python scripts/cdm_analysis/nl_sql_query.py \
  --api-key "sk-ant-..." \
  "your question"
```

### Save Results to File
```bash
just cdm-nl-query-json "your question" > results.json
```

## Tips for Better Results

1. **Be Specific**: "Show me samples with depth > 100" instead of "Show me deep samples"
2. **Use Table Names**: Reference actual table names when known (sdt_sample, sdt_reads)
3. **Specify Limits**: "Top 10 locations" instead of "Show locations"
4. **Use Field Names**: "samples with read_count > 50000" uses actual column names
5. **Ask for Context**: "Show samples with their locations" triggers JOINs automatically

## Troubleshooting

**Issue**: Query returns no results
- Check if data actually exists: `just cdm-store-stats`
- Verify table/column names with verbose mode

**Issue**: SQL syntax error
- Run with `--verbose` to see generated SQL
- Check DuckDB documentation for syntax
- Rephrase question using simpler terms

**Issue**: Query too slow
- Add LIMIT clauses: "Show first 100 samples..."
- Use indexed columns when possible
- Consider using brick tables with caution (large datasets)

## Related Commands

```bash
# Show database statistics
just cdm-store-stats

# Pre-defined queries
just cdm-find-samples Location0000001
just cdm-search-oterm "soil"
just cdm-lineage Assembly Assembly0000001

# View documentation
cat docs/CDM_PARQUET_STORE_GUIDE.md
```

## Technical Details

**Script Location**: `scripts/cdm_analysis/nl_sql_query.py`

**Dependencies**:
- `anthropic>=0.39.0` - Claude API client
- `duckdb` - Database engine
- `linkml-store>=0.2.0` - Data management

**Model**: Claude Sonnet 4 (claude-sonnet-4-20250514)

**Token Limits**:
- Schema description: ~1-2K tokens
- Query translation: ~1K tokens max
- Results returned up to 100 rows by default
