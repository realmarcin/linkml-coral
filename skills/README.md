# Claude Code Skills for linkml-coral

This directory contains Claude Code skills that extend Claude's capabilities for working with the linkml-coral CDM database.

## Available Skills

### 1. nl-sql-query (Fast, Simple Queries)

Query the CDM DuckDB database using natural language questions instead of writing SQL.

**Usage**: `/nl-sql-query`

**Best for:**
- Quick, simple queries
- Basic counts and filters
- Fast ad-hoc analysis
- When schema understanding is not needed

**Example**: "How many samples are there?"

### 2. schema-query (Intelligent, Complex Queries)

Query using full LinkML schema awareness for intelligent, relationship-aware queries.

**Usage**: `/schema-query`

**Best for:**
- Complex joins across multiple tables
- Queries requiring relationship understanding
- Exploring the data model
- Schema-aware query suggestions
- Semantic understanding (ontology terms)

**Example**: "Find samples with their location information"

**Additional features:**
- `just cdm-schema-info` - Show schema structure
- `just cdm-schema-explore Sample` - Explore specific class
- `just cdm-schema-suggest` - Get query ideas

## Choosing the Right Skill

| Feature | nl-sql-query | schema-query |
|---------|--------------|--------------|
| Speed | ⚡ Fast | 🐢 Slightly slower |
| Database schema | ✓ | ✓ |
| LinkML schema | ✗ | ✓ |
| Relationships | Basic | Rich |
| Query suggestions | ✗ | ✓ |
| Schema exploration | ✗ | ✓ |
| Best for | Simple queries | Complex queries |

## Installation

### Option 1: Project-Local Skills (Recommended)

Skills in this directory are automatically available when working in this project. Claude Code will discover them automatically.

### Option 2: Global Skills

To make these skills available globally across all projects:

```bash
# Create global skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy or symlink the skill
ln -s "$(pwd)/skills/nl-sql-query" ~/.claude/skills/nl-sql-query

# Or copy it
cp -r skills/nl-sql-query ~/.claude/skills/
```

## Using Skills

Once installed, you can invoke skills in two ways:

1. **Slash Command**: `/nl-sql-query`
2. **Natural Request**: "Use the nl-sql-query skill to find samples with high depth"

## Prerequisites

Before using skills, ensure:

1. **Database**: CDM database is loaded (`just load-cdm-store-bricks-64gb`)
2. **API Key**: Set `ANTHROPIC_API_KEY` environment variable
3. **Dependencies**: Run `uv sync` to install required packages

## Creating New Skills

To create a new skill for this project:

```bash
# Create skill directory
mkdir -p skills/my-new-skill

# Create SKILL.md with YAML frontmatter
cat > skills/my-new-skill/SKILL.md << 'EOF'
---
name: my-new-skill
description: Brief description of when to use this skill
---

# My New Skill

Instructions for Claude on how to use this skill...
EOF
```

See [Anthropic Skills Repository](https://github.com/anthropics/skills) for examples and best practices.

## Skill Development Resources

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Skill Creation Guide](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [Best Practices](https://mikhail.io/2025/10/claude-code-skills/)
- [Example Skills](https://github.com/anthropics/skills)
