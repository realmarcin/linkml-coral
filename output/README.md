# Output Directory

This directory contains all report files, analysis documents, test databases, and other generated outputs from development work.

## Contents

### Analysis and Report Documents
- `*_ANALYSIS.md` - Analysis reports from various development phases
- `*_GUIDE.md` - Implementation guides and documentation
- `*_SUMMARY.md` - Summary documents for completed tasks
- `*_STATUS.md` - Status reports and progress tracking

### Database Files
- `*.db` - Test and development database files
- `*.db.wal` - SQLite write-ahead log files
- `brick_*.db` - Brick table loading test databases
- `cdm_store_*.db` - CDM store database variations
- `enigma_*.db` - ENIGMA data test databases

### Generated Files
- `generated_schema*.sql` - Generated SQL DDL files
- `schema_base.sql` - Base schema definitions
- `*.json` - Metadata and report JSON files
- `brick_index.json` - Brick table index
- `*_metadata.json` - Metadata extraction outputs
- `*.out` - Command execution logs

### Scripts
- `*.py` - Ad-hoc analysis and test scripts

## Note

Files in this directory are:
- **Not tracked in git** (excluded via `.gitignore`)
- Generated during development and testing
- Safe to delete if you need to clean up disk space
- Regenerable by running the appropriate commands

To clean up this directory:
```bash
rm -rf output/*
```

To regenerate databases and reports, see the main README.md for appropriate `just` commands.
