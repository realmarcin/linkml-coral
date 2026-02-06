---
name: schema-query
description: Query the CDM DuckDB database using LinkML schema awareness. Use this skill when the user wants to query the database with understanding of the data model, relationships, and semantics defined in the LinkML schema. This provides richer, more intelligent queries than basic SQL.
---

# Schema-Aware Query for CDM Database

Query the KBase CDM DuckDB database with full understanding of the LinkML schema, including class definitions, relationships, constraints, and semantic annotations.

## When to Use This Skill

Use this skill when:
- User wants to query with understanding of the data model
- User asks about relationships between entities
- User wants schema-aware query suggestions
- User needs to explore the data model structure
- User wants queries that leverage semantic annotations
- Complex joins across multiple entities are needed

## Advantages Over Simple SQL Queries

**Schema Awareness:**
- Understands class descriptions and purposes
- Knows foreign key relationships automatically
- Recognizes required vs optional fields
- Understands multivalued attributes
- Leverages semantic annotations (ontology terms)

**Intelligent Query Generation:**
- Automatically generates proper JOINs based on schema relationships
- Uses descriptive aliases based on schema descriptions
- Validates queries against data model constraints
- Suggests related queries based on schema structure

## Prerequisites

Same as nl-sql-query skill:
1. **CDM Database**: Must exist (e.g., `cdm_store.db`)
2. **API Key**: `ANTHROPIC_API_KEY` environment variable
3. **LinkML Schema**: `src/linkml_coral/schema/linkml_coral.yaml` (already present)

## Usage

### Basic Query

```bash
just cdm-schema-query "Find samples from Location0000001"
```

### JSON Output

```bash
just cdm-schema-query-json "Show assemblies with their sample information"
```

### Verbose (See Schema Context)

```bash
just cdm-schema-query-verbose "List reads with high counts and their samples"
```

### Direct Python Usage

```bash
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --db cdm_store.db \
  "Find samples from specific location"
```

## Schema Exploration Commands

### Show Entire Schema

```bash
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --db cdm_store.db \
  --show-schema
```

Output includes:
- All classes and their descriptions
- Attributes per class
- Relationship counts

### Explore Specific Class

```bash
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --db cdm_store.db \
  --explore-class Sample
```

Output includes:
- Class description
- All attributes with types and requirements
- Relationships to other classes

### Get Query Suggestions

```bash
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --db cdm_store.db \
  --suggest-queries
```

Output includes:
- Basic count queries for each class
- Relationship-based query suggestions
- Common analysis patterns

## Example Queries

### Basic Entity Queries

**Simple lookups:**
- "Find all samples"
- "Show me Location records"
- "List assemblies"

**With filters:**
- "Find samples with depth greater than 100"
- "Show reads from sample Sample0000001"
- "List assemblies from 2021"

### Relationship Queries

**Two-entity joins:**
- "Find samples with their location information"
- "Show reads with their corresponding samples"
- "List assemblies with read data"

**Multi-entity queries:**
- "Show the complete pipeline: sample → reads → assembly"
- "Find locations with their samples and read counts"
- "Trace assemblies back to their source locations"

### Schema-Driven Queries

**Using schema knowledge:**
- "Show all required fields for Sample class"
- "Find samples with missing required attributes"
- "List all foreign key relationships from Sample"

**Semantic queries:**
- "Find samples from soil environments" (uses ontology knowledge)
- "Show sequencing reads by technology type" (uses enum knowledge)
- "List assemblies with provenance information" (uses annotations)

## How It Works

1. **Load LinkML Schema**: Reads `linkml_coral.yaml` using SchemaView
2. **Extract Context**: Builds comprehensive data model context
   - Classes and descriptions
   - Slots (attributes) with types and constraints
   - Foreign key relationships
   - Enums and valid values
   - Semantic annotations
3. **Query Translation**: Sends schema context + user query to Claude API
4. **SQL Generation**: Claude generates schema-aware SQL with proper JOINs
5. **Execution**: Runs query and returns formatted results

## Schema Information Used

### Classes (Entities)
- Process, Location, Sample, Taxon, Community
- Reads, Assembly, Genome, Gene
- OTU (ASV), Protein

### Key Relationships
- Sample → Location (sample_location FK)
- Reads → Sample (reads_sample FK)
- Assembly → Reads (assembly_reads FK)
- Genome → Assembly (genome_assembly FK)
- Gene → Genome (gene_genome FK)

### Semantic Annotations
- **Ontology terms**: DA (Data Acquisition), ME (Measurement), ENVO (Environment)
- **Process types**: Provenance workflow annotations
- **Microtypes**: ME: terms for semantic typing (298 types)

## Output Formats

### Text Format (Default)
```
Query: Find samples from Location0000001

Generated SQL:
SELECT s.*
FROM sdt_sample s
WHERE s.sample_location = 'Location0000001'
LIMIT 100

Results (5 rows):
sample_id         | sample_name | sample_location    | ...
------------------|-------------|--------------------|-----
Sample0000001     | Site A      | Location0000001    | ...
```

### JSON Format
```json
{
  "natural_query": "Find samples from Location0000001",
  "sql_query": "SELECT s.* FROM sdt_sample s WHERE ...",
  "result_count": 5,
  "results": [
    {"sample_id": "Sample0000001", ...}
  ]
}
```

## Implementation Steps

When user invokes this skill:

1. **Check Prerequisites**
   ```bash
   # Database exists
   ls -l cdm_store.db

   # Schema exists
   ls -l src/linkml_coral/schema/linkml_coral.yaml

   # API key set
   echo $ANTHROPIC_API_KEY | grep -q "sk-"
   ```

2. **Execute Query**
   ```bash
   just cdm-schema-query "USER_QUESTION_HERE"
   ```

3. **Handle Results**
   - Display results with schema context
   - If query fails, show schema info that might help
   - Suggest related queries based on schema

## Comparison: schema-query vs nl-sql-query

| Feature | nl-sql-query | schema-query |
|---------|--------------|--------------|
| **Database schema** | ✓ (inspects tables) | ✓ (inspects tables) |
| **LinkML schema** | ✗ | ✓ (full understanding) |
| **Relationships** | Basic (from DB) | Rich (from LinkML) |
| **Descriptions** | ✗ | ✓ (from schema) |
| **Constraints** | ✗ | ✓ (required, multivalued) |
| **Semantics** | ✗ | ✓ (ontology, annotations) |
| **Query suggestions** | ✗ | ✓ (schema-based) |
| **Speed** | Fast | Slightly slower (more context) |

**Use nl-sql-query when:**
- Simple, fast queries needed
- No relationship complexity
- Quick ad-hoc analysis

**Use schema-query when:**
- Complex joins required
- Need to understand data model
- Want schema-aware suggestions
- Exploring relationships
- Need semantic understanding

## Advanced Features

### Schema Exploration

**List all classes:**
```bash
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --show-schema \
  --db cdm_store.db
```

**Explore Sample class:**
```bash
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --explore-class Sample \
  --db cdm_store.db
```

**Get query ideas:**
```bash
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --suggest-queries \
  --db cdm_store.db
```

### Custom Schema Path

```bash
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --schema /path/to/custom_schema.yaml \
  --db cdm_store.db \
  "your query"
```

## Tips for Better Results

1. **Use Class Names**: Mention actual class names (Sample, Location, Reads)
2. **Ask About Relationships**: "Show samples WITH their locations"
3. **Request Schema Info**: "What fields does Sample have?"
4. **Use Schema Terms**: Use terminology from the data model
5. **Complex Queries**: Schema understands multi-hop relationships

## Troubleshooting

**Issue**: Schema file not found
```bash
# Verify schema exists
ls -l src/linkml_coral/schema/linkml_coral.yaml
```

**Issue**: Query doesn't understand relationship
```bash
# Explore the classes first
uv run python scripts/cdm_analysis/schema_aware_query.py \
  --explore-class Sample \
  --db cdm_store.db
```

**Issue**: Want to see what queries are possible
```bash
# Get suggestions
just cdm-schema-suggest
```

## Related Commands

```bash
# Show schema info
just cdm-schema-info

# Explore specific class
just cdm-schema-explore Sample

# Get query suggestions
just cdm-schema-suggest

# Regular database stats
just cdm-store-stats
```

## Technical Details

**Script**: `scripts/cdm_analysis/schema_aware_query.py`

**Dependencies**:
- `linkml-runtime>=1.9.4` - Schema loading and inspection
- `anthropic>=0.39.0` - Claude API client
- `duckdb` - Database queries

**Model**: Claude Sonnet 4 (claude-sonnet-4-20250514)

**Schema Used**: `src/linkml_coral/schema/linkml_coral.yaml`
- 12 classes (entities)
- 105 slots (attributes)
- 23 enums (controlled vocabularies)
- 69 microtype annotations (ME: terms)
- Complete relationship graph
