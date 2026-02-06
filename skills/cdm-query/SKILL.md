---
name: cdm-query
description: Unified intelligent query interface for the CDM DuckDB database. Use this skill when the user wants to query the linkml-coral CDM database. Automatically chooses between fast SQL translation and schema-aware intelligent queries based on complexity. Supports natural language questions, schema exploration, and data analysis.
---

# CDM Query - Unified Database Query Interface

Intelligent query interface that automatically selects the optimal approach for querying the KBase CDM DuckDB database.

## When to Use This Skill

Use this skill for **any** CDM database query needs:
- Natural language questions about the data
- Schema exploration and documentation
- Simple counts and statistics
- Complex joins and relationships
- Data analysis and exploration

**This is the recommended default skill** for all CDM database interactions.

## How It Works

The skill automatically chooses the best approach:

### Fast Path (Simple Queries)
For straightforward queries, uses direct SQL translation:
- Single table queries
- Basic counts and statistics
- Simple filters
- Quick lookups

### Schema-Aware Path (Complex Queries)
For sophisticated queries, uses LinkML schema context:
- Multi-table joins
- Relationship navigation
- Schema exploration
- Complex aggregations
- Queries requiring data model understanding

### Auto-Detection
The skill analyzes your question and automatically picks the optimal approach. You don't need to think about it!

## Prerequisites

**Option 1: With API Key (Full Features)**
- Database loaded: `cdm_store_sample.db` or similar
- API Key: `ANTHROPIC_API_KEY` environment variable set
- Enables natural language query translation

**Option 2: Without API Key (Claude Code Only)**
- Database loaded: `cdm_store_sample.db` or similar
- Use this skill in Claude Code conversations
- Claude directly translates and executes queries

## Usage

### In Claude Code (Recommended)

Simply invoke the skill:
```
/cdm-query
```

Then ask your question:
- "How many samples are there?"
- "Show me samples with their location information"
- "What fields does the Sample table have?"
- "Find assemblies with read data"

### Using Just Commands

```bash
# Simple query (fast path)
just cdm-query "How many samples are there?"

# Complex query (schema-aware path)
just cdm-query "Find samples with their locations and read counts"

# Schema exploration
just cdm-query-schema Sample
just cdm-query-info

# JSON output
just cdm-query-json "Count samples by location"
```

### Direct Python

```bash
uv run python scripts/cdm_analysis/cdm_unified_query.py \
  --db cdm_store_sample.db \
  "your question"
```

## Query Examples

### Simple Queries (Fast Path Used)

**Counts and Statistics:**
- "How many samples are in the database?"
- "Count all reads"
- "Show total assemblies"

**Single Table Filters:**
- "Find samples with depth > 100"
- "List reads with read_count > 50000"
- "Show assemblies from 2021"

**Basic Lookups:**
- "Get sample Sample0000001"
- "Show location Location0000001"
- "Display the first 10 samples"

### Complex Queries (Schema-Aware Path Used)

**Joins and Relationships:**
- "Find samples WITH their location information"
- "Show reads WITH their corresponding samples"
- "List assemblies WITH their read data"

**Multi-Hop Relationships:**
- "Trace the pipeline: sample → reads → assembly"
- "Find locations with their samples and read counts"
- "Show genomes with their source samples"

**Aggregations Across Tables:**
- "Count samples per location with location names"
- "Show average read count per sample material"
- "List assemblies grouped by source location"

### Schema Exploration

**Class Information:**
- "What is the Sample class?"
- "Explain the Reads entity"
- "Show me all classes in the schema"

**Relationship Discovery:**
- "How is Sample related to Location?"
- "What tables link to Reads?"
- "Show the provenance chain for assemblies"

**Query Suggestions:**
- "What can I query?"
- "Give me interesting query ideas"
- "What relationships exist?"

## Command Reference

### Query Commands

```bash
# Basic query (auto-detects complexity)
just cdm-query "your question"

# Force fast path
just cdm-query-fast "simple question"

# Force schema-aware path
just cdm-query-schema-aware "complex question"

# JSON output
just cdm-query-json "your question"

# Verbose (show SQL and strategy)
just cdm-query-verbose "your question"
```

### Schema Exploration

```bash
# Show schema overview
just cdm-query-info

# Explore specific class
just cdm-query-explore Sample

# Get query suggestions
just cdm-query-suggest

# Show relationships
just cdm-query-relationships
```

## Smart Auto-Detection

The skill analyzes your query for:

**Indicators of Simple Query (Fast Path):**
- Keywords: "count", "how many", "total"
- Single entity mentioned
- No relationship words ("with", "and their")
- Basic filters (>, <, =)
- No JOINs implied

**Indicators of Complex Query (Schema-Aware Path):**
- Multiple entities mentioned
- Relationship words: "with", "and their", "related to"
- Cross-table aggregations
- Provenance terms: "pipeline", "lineage", "trace"
- Schema questions: "what is", "explain", "how is...related"

**Example Auto-Detection:**

| Query | Path Used | Why |
|-------|-----------|-----|
| "How many samples?" | Fast | Single table count |
| "Find samples with depth > 100" | Fast | Single table filter |
| "Samples WITH locations" | Schema-aware | JOIN implied |
| "What is Sample class?" | Schema-aware | Schema exploration |
| "Trace sample → assembly" | Schema-aware | Multi-hop relationship |

## Implementation Strategy

When you invoke this skill, Claude will:

1. **Analyze the Question**
   - Identify entities mentioned
   - Detect relationship keywords
   - Check for schema questions

2. **Choose Strategy**
   ```
   IF simple_query:
       Use fast SQL translation
       Execute with minimal context
   ELSE IF complex_query:
       Load LinkML schema
       Use schema-aware translation
       Generate intelligent JOINs
   ELSE IF schema_question:
       Use schema exploration tools
       Return documentation
   ```

3. **Execute Query**
   - Generate appropriate SQL
   - Run against DuckDB
   - Format results

4. **Return Results**
   - Display data in clean format
   - Show SQL if verbose mode
   - Suggest related queries

## Error Handling

**If Fast Path Fails:**
- Automatically retry with schema-aware path
- Schema context may resolve ambiguities

**If Query is Ambiguous:**
- Ask clarifying questions
- Suggest similar valid queries

**If Results are Empty:**
- Verify data exists
- Suggest alternative queries
- Check for typos in entity names

## Performance Notes

**Fast Path:**
- ⚡ ~2-3 seconds
- Minimal context (~1-2KB)
- Best for simple queries

**Schema-Aware Path:**
- 🐢 ~3-5 seconds
- Rich context (~10-12KB)
- Best for complex queries

**The skill optimizes for speed** by using the fast path when possible, but switches to schema-aware when needed for accuracy.

## Comparison with Individual Skills

| Feature | /cdm-query (unified) | /nl-sql-query | /schema-query |
|---------|---------------------|---------------|---------------|
| **Auto-optimization** | ✓ Yes | ✗ No | ✗ No |
| **Fast simple queries** | ✓ Yes | ✓ Yes | ✗ Slower |
| **Complex joins** | ✓ Yes | ~ Basic | ✓ Yes |
| **Schema awareness** | ✓ Auto | ✗ No | ✓ Yes |
| **Schema exploration** | ✓ Yes | ✗ No | ✓ Yes |
| **User choice needed** | ✗ No | ✓ Yes | ✓ Yes |

**Recommendation**: Use `/cdm-query` as your default. It combines the best of both approaches.

## Tips for Best Results

1. **Be Specific**
   - Good: "Find samples with depth > 100"
   - Better: "Find samples where depth_meter > 100"

2. **Use Relationship Words for Joins**
   - Use "WITH" for joins: "samples WITH their locations"
   - Use "AND" for multiple tables: "samples AND their reads"

3. **Ask for Schema Help**
   - "What fields does Sample have?"
   - "How do I query locations?"
   - "Show me the data model"

4. **Start Simple, Then Refine**
   - First: "How many samples?"
   - Then: "Show me those samples"
   - Finally: "Add their location information"

## Advanced Features

### Query History
Maintains context of previous queries in conversation for follow-up questions.

### Smart Suggestions
After each query, suggests related queries you might want to run.

### Automatic Optimization
Learns from failed queries and adjusts strategy automatically.

### Multi-Format Output
- Text tables (default)
- JSON (--json flag)
- CSV (--csv flag)
- Markdown (--markdown flag)

## Troubleshooting

**Issue**: "Table not found"
- Run: `just cdm-store-stats` to see available tables
- Check table naming: sdt_sample not Sample

**Issue**: Query too slow
- The skill will automatically use fast path for simple queries
- For complex queries, consider adding filters to limit results

**Issue**: Unexpected results
- Use `--verbose` to see generated SQL
- Check if the right strategy was chosen
- Try rephrasing your question

## Related Commands

```bash
# Database management
just cdm-store-stats              # Show what's in database
just load-cdm-store-sample        # Load sample database

# Direct query interfaces (if you want manual control)
just cdm-nl-query "question"      # Force fast path
just cdm-schema-query "question"  # Force schema-aware path

# Data exploration
just cdm-find-samples Location0000001
just cdm-search-oterm "soil"
just cdm-lineage Assembly Assembly0000001
```

## Technical Details

**Backend**:
- Python DuckDB 1.4.1
- LinkML Runtime 1.9.4+
- Anthropic Claude API (optional)

**Database**:
- DuckDB format
- CDM naming convention (sdt_*, sys_*, ddt_*)
- Full LinkML schema awareness

**Strategies**:
1. Fast SQL: Direct translation, minimal context
2. Schema-aware: LinkML schema context, intelligent JOINs
3. Hybrid: Uses both as needed

**Scripts**:
- `scripts/cdm_analysis/nl_sql_query.py` (fast path)
- `scripts/cdm_analysis/schema_aware_query.py` (schema-aware path)
- `scripts/cdm_analysis/cdm_unified_query.py` (unified interface)

## Future Enhancements

Planned features:
- Query result caching
- Automatic query optimization suggestions
- Visual query builder integration
- Export to multiple formats
- Saved query templates
- Query performance analysis
