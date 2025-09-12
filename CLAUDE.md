# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## linkml-coral

LinkML schema repository for CORAL, implementing the ENIGMA Common Data Model using the LinkML (Linked Data Modeling Language) framework.

## Essential Commands

**Development workflow:**
```bash
just test          # Run all tests (schema, Python, examples)
just gen-project   # Generate project files from schema
just lint          # Lint the schema
just site          # Generate project and documentation locally
just testdoc       # Build docs and run test server
```

**Dependency management:**
```bash
uv sync            # Install/sync dependencies
uv run <command>   # Run commands in the virtual environment
```

Never use `pip` directly - this project uses `uv` for dependency management.

## Repository Structure

**Core schema files (edit these):**
- `src/linkml-coral/schema/linkml-coral.yaml` - Basic example schema
- `src/linkml-coral/schema/enigma_cdm_schema.yaml` - ENIGMA Common Data Model schema

**Generated files (do not edit):**
- `src/linkml-coral/datamodel/` - Python dataclasses and Pydantic models
- `project/` - Other generated formats (Java, TypeScript, OWL, etc.)
- `docs/` - Generated documentation
- `examples/` - Generated examples

**Test data:**
- `tests/data/valid/` - Valid example data (format: `ClassName-{name}.yaml`)
- `tests/data/invalid/` - Invalid examples for negative testing

## Architecture Overview

This is a LinkML project that:
1. Defines semantic data models in YAML format
2. Generates multiple output formats (Python, TypeScript, Java, OWL, JSON Schema)
3. Validates data against schemas
4. Auto-generates documentation

The project includes two main schemas:
- **linkml-coral.yaml**: Simple example with Person/PersonCollection entities
- **enigma_cdm_schema.yaml**: Complex ENIGMA Common Data Model with entities like Process, Location, Sample, etc.

## Testing Strategy

```bash
just test  # Runs all tests in sequence:
```
1. **Schema validation** - Ensures schema can be processed
2. **Python unit tests** - Uses pytest (functional style preferred)
3. **Example validation** - Tests valid/invalid data against schema

For specific tests:
```bash
uv run pytest tests/test_specific.py::test_name  # Run single test
uv run pytest -xvs                               # Stop on first failure, verbose
```

## LinkML Best Practices

- **Naming**: CamelCase for classes, snake_case for slots/attributes
- **Polymorphism**: Use `type` field with `type_designator: true`
- **Documentation**: Include meaningful descriptions for all elements
- **Standards**: Map to existing standards (e.g., dcterms, OBO terms)
- **Ontology terms**: Never guess IDs - use OLS MCP to look up terms

## Common Development Tasks

```bash
# After modifying schema:
just gen-project    # Regenerate all derived files
just test          # Verify changes don't break anything

# Documentation:
just testdoc       # Preview docs locally at http://localhost:8000

# Linting:
just lint          # Check schema quality
uv run ruff check  # Python linting
```

## Configuration Files

- `config.yaml` - LinkML generator configuration
- `pyproject.toml` - Python project configuration
- `.editorconfig` - 4 spaces for Python, 2 for YAML/JSON
- `mkdocs.yml` - Documentation site configuration