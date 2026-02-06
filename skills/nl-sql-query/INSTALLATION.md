# Installation Guide: nl-sql-query Skill

## Quick Start

The `nl-sql-query` skill is already installed in this project and ready to use!

### Prerequisites

1. **Anthropic API Key**: Set your API key
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-your-key-here"
   ```

2. **Dependencies**: Install Python packages
   ```bash
   uv sync
   ```

3. **Database**: Load CDM data into DuckDB
   ```bash
   just load-cdm-store-bricks-64gb
   ```

## Using the Skill

### Method 1: Claude Code Skill (Recommended)

When using Claude Code in this project, simply invoke:
```
/nl-sql-query
```

Then ask your question in natural language.

### Method 2: Just Commands

```bash
# Basic query
just cdm-nl-query "How many samples are there?"

# JSON output
just cdm-nl-query-json "Show top 10 locations"

# Verbose (see SQL)
just cdm-nl-query-verbose "Find samples with depth > 100"
```

### Method 3: Direct Python Script

```bash
uv run python scripts/cdm_analysis/nl_sql_query.py \
  --db cdm_store.db \
  "your natural language question"
```

## Global Installation (Optional)

To make this skill available across all Claude Code projects:

```bash
# Create global skills directory
mkdir -p ~/.claude/skills

# Symlink the skill
ln -s "$(pwd)/skills/nl-sql-query" ~/.claude/skills/nl-sql-query
```

## Verifying Installation

### Check Prerequisites

```bash
# 1. Check API key
echo $ANTHROPIC_API_KEY | grep -q "sk-ant" && echo "✓ API key set" || echo "✗ API key missing"

# 2. Check dependencies
uv run python -c "import anthropic; print('✓ anthropic package installed')" 2>/dev/null || echo "✗ Run: uv sync"

# 3. Check database
ls -lh cdm_store.db || ls -lh cdm_store_bricks_full.db || echo "✗ Load database with: just load-cdm-store-bricks-64gb"

# 4. Check script
test -x scripts/cdm_analysis/nl_sql_query.py && echo "✓ Script executable" || echo "✗ Script not found"
```

### Test Query

```bash
# Quick test
just cdm-nl-query "SELECT 1 as test"
```

Expected output:
```
Natural Query: SELECT 1 as test

Generated SQL:
SELECT 1 as test

Results (1 rows):
test
----
1
```

## Troubleshooting

### Issue: "anthropic package not installed"

**Solution:**
```bash
uv sync
```

### Issue: "ANTHROPIC_API_KEY not set"

**Solution:**
```bash
export ANTHROPIC_API_KEY="your-key-here"

# Or permanently in your shell profile:
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc
```

### Issue: "Database not found"

**Solution:**
```bash
# Option 1: Quick sample (2 minutes, 8 GB RAM)
just load-cdm-store-sample

# Option 2: Full dataset (45 minutes, 64 GB RAM)
just load-cdm-store-bricks-64gb
```

### Issue: "Query fails with SQL error"

**Solution:**
Try with verbose mode to see the generated SQL:
```bash
just cdm-nl-query-verbose "your question"
```

Then check if:
- Table names are correct (use `just cdm-store-stats` to see available tables)
- Column names match the schema
- The question is specific enough

## Updating the Skill

If the skill is updated, simply pull the latest changes:

```bash
git pull
uv sync  # In case dependencies changed
```

## Uninstalling

To remove the skill:

```bash
# Remove global symlink (if created)
rm ~/.claude/skills/nl-sql-query

# Remove from project (not recommended)
rm -rf skills/nl-sql-query
```

## Support

For issues or questions:
1. Check `skills/nl-sql-query/EXAMPLES.md` for query examples
2. See `skills/nl-sql-query/SKILL.md` for complete documentation
3. Review `docs/CDM_PARQUET_STORE_GUIDE.md` for database details
4. Open an issue on GitHub
