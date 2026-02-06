# Schema-Query vs NL-SQL-Query Comparison

This document compares the two natural language query skills available for the CDM database.

## Quick Comparison

| Feature | nl-sql-query | schema-query |
|---------|--------------|--------------|
| **Speed** | ⚡ Fast | 🐢 Slightly slower |
| **Complexity** | Simple | Complex |
| **Database schema** | ✓ Reads tables/columns | ✓ Reads tables/columns |
| **LinkML schema** | ✗ Not used | ✓ Full understanding |
| **Class descriptions** | ✗ | ✓ From schema |
| **Relationships** | Basic (from DB FK) | Rich (from LinkML) |
| **Required fields** | ✗ | ✓ Knows constraints |
| **Multivalued attrs** | ✗ | ✓ Understands arrays |
| **Ontology terms** | ✗ | ✓ Uses annotations |
| **Query suggestions** | ✗ | ✓ Schema-based |
| **Schema exploration** | ✗ | ✓ Full exploration |
| **Auto JOINs** | Basic | Intelligent |

## When to Use Each Skill

### Use nl-sql-query When:

✅ **Quick, simple queries**
- "How many samples are there?"
- "Show me the first 10 locations"
- "Count assemblies"

✅ **Single table queries**
- "Find samples with depth > 100"
- "List reads with high counts"

✅ **Speed is priority**
- Ad-hoc exploration
- Quick checks
- Simple statistics

✅ **No relationships needed**
- Queries within one table
- Simple filters and counts

### Use schema-query When:

✅ **Complex joins required**
- "Find samples WITH their location information"
- "Show assemblies WITH their read data"
- "Trace sample → reads → assembly pipeline"

✅ **Need to understand relationships**
- "What fields does Sample have?"
- "How is Sample related to Location?"
- "Show me the data model for sequencing"

✅ **Want query suggestions**
- "What can I query?"
- "Give me interesting query ideas"
- "What relationships exist?"

✅ **Exploring the data model**
- "Explain the Sample class"
- "Show all foreign keys"
- "What enums are available?"

✅ **Semantic understanding needed**
- Queries using ontology terms
- Understanding microtype annotations
- Using domain knowledge from schema

## Example Comparison

### Example 1: Simple Count

**Query**: "How many samples are there?"

**nl-sql-query** (faster):
```sql
SELECT COUNT(*) as total_samples FROM sdt_sample
```
⏱️ ~2 seconds

**schema-query** (same result):
```sql
SELECT COUNT(*) as total_samples FROM sdt_sample
```
⏱️ ~3 seconds (loads schema first)

**Winner**: nl-sql-query (faster, no benefit from schema)

---

### Example 2: Simple Join

**Query**: "Find samples with their location names"

**nl-sql-query**:
```sql
SELECT s.*, l.location_name
FROM sdt_sample s
JOIN sdt_location l ON s.sample_location = l.location_id
LIMIT 100
```
⏱️ ~3 seconds

**schema-query**:
```sql
-- Same SQL, but knows from schema that:
-- - sample_location is FK to Location.location_id
-- - Location has a 'name' field called location_name
-- - This is a required relationship
SELECT s.*, l.location_name
FROM sdt_sample s
JOIN sdt_location l ON s.sample_location = l.location_id
LIMIT 100
```
⏱️ ~4 seconds

**Winner**: Tie (both work well, schema-query has more context)

---

### Example 3: Complex Multi-Hop Join

**Query**: "Show the complete sequencing pipeline from sample to genes"

**nl-sql-query**:
```sql
-- May struggle with complex multi-table joins
-- Might miss some relationships
SELECT *
FROM sdt_sample s
JOIN sdt_reads r ON ...
-- May not get all relationships correct
```

**schema-query**:
```sql
-- Understands the complete provenance chain from schema:
-- Sample → Reads → Assembly → Genome → Gene
SELECT
  s.sample_id,
  s.sample_name,
  r.reads_id,
  a.assembly_id,
  g.genome_id,
  ge.gene_id
FROM sdt_sample s
JOIN sdt_reads r ON r.reads_sample = s.sample_id
JOIN sdt_assembly a ON a.assembly_reads = r.reads_id
JOIN sdt_genome g ON g.genome_assembly = a.assembly_id
JOIN sdt_gene ge ON ge.gene_genome = g.genome_id
LIMIT 100
```

**Winner**: schema-query (understands full pipeline from schema)

---

### Example 4: Schema Exploration

**Query**: "What fields does Sample have?"

**nl-sql-query**:
```
-- Can only show columns from database:
sample_id, sample_name, sample_location, sample_depth, ...
```

**schema-query**:
```
Class: Sample
Description: Sample entity in the ENIGMA data model

Attributes:
  - sample_id: string (REQUIRED) - Primary identifier
  - sample_name: string - Sample name
  - sample_location: Location (REQUIRED) → FK to Location
    References the sampling location
  - sample_depth: Depth - Sampling depth (ME:0000015)
    Depth in meters, range constraints apply
  - sample_material: string - Material type
    Enum: soil, sediment, water, ...
  ...

Relationships:
  - sample_location → Location (required FK)
  - Used by: Reads, Community
```

**Winner**: schema-query (rich schema information)

## Performance Comparison

### Response Times (Approximate)

| Query Type | nl-sql-query | schema-query | Difference |
|------------|--------------|--------------|------------|
| Simple count | 2s | 3s | +1s |
| Single table filter | 2.5s | 3.5s | +1s |
| Simple join (2 tables) | 3s | 4s | +1s |
| Complex join (3+ tables) | 4s | 5s | +1s |
| Schema exploration | N/A | 3s | - |

**Note**: schema-query is ~1 second slower due to loading and processing the LinkML schema.

## Context Size Comparison

### nl-sql-query Context:
- Database tables and columns (~1KB)
- Row counts per table (~100 bytes)
- **Total**: ~1-2KB

### schema-query Context:
- Database tables and columns (~1KB)
- LinkML class definitions (~5KB)
- Slot descriptions and types (~3KB)
- Relationships and FKs (~2KB)
- Semantic annotations (~1KB)
- **Total**: ~10-12KB

**Impact**: schema-query uses more tokens but provides richer understanding.

## Recommendations

### Default Choice
**Start with nl-sql-query** for:
- Initial exploration
- Simple queries
- Quick checks
- Single table operations

**Switch to schema-query** when you need:
- Complex joins
- Relationship understanding
- Query suggestions
- Schema exploration
- Domain knowledge

### Best Practice

1. **Use nl-sql-query by default** for speed
2. **Use schema-query when queries fail** or relationships are unclear
3. **Use schema-query for exploration** (`--show-schema`, `--explore-class`)
4. **Use schema-query for learning** the data model

## Future Enhancements

Potential improvements:

**nl-sql-query**:
- Cache database schema for faster queries
- Add query history and suggestions
- Support for query templates

**schema-query**:
- Cache compiled schema context
- Add validation against schema constraints
- Generate example data based on schema
- Semantic search using ontology terms
- Automatic query optimization based on schema

## Related Documentation

- `skills/nl-sql-query/SKILL.md` - Basic natural language SQL queries
- `skills/schema-query/SKILL.md` - Schema-aware queries
- `skills/nl-sql-query/EXAMPLES.md` - 50+ example queries
- `docs/CDM_PARQUET_STORE_GUIDE.md` - Database structure
- `src/linkml_coral/schema/linkml_coral.yaml` - LinkML schema definition
