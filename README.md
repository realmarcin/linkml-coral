<a href="https://github.com/dalito/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# linkml-coral

linkml schema for CORAL

## Getting Started

When cloning linkml-coral:
```bash
git clone https://github.com/realmarcin/linkml-coral
cd linkml-coral
git submodule update --init --recursive
uv sync
```

To update CORAL and sync typedef.json:
```bash
git submodule update --remote CORAL
cp CORAL/back_end/python/var/typedef.json data/
```

## Documentation Website

[https://realmarcin.github.io/linkml-coral](https://realmarcin.github.io/linkml-coral)

## Quick Start: CDM Store Queries

Load and query KBase Common Data Model (CDM) parquet files using linkml-store:

```bash
# Load CDM data into queryable database (~60-90 seconds)
just load-cdm-store

# Show database statistics
just cdm-store-stats

# Find samples from a location
just cdm-find-samples EU02

# Search ontology terms
just cdm-search-oterm "soil"

# Trace provenance lineage
just cdm-lineage Assembly Assembly0000001
```

**What gets loaded:**
- 1,110,656 records across 23 collections
- 17 static entity tables (Location, Sample, Reads, Assembly, Genome, Gene, ASV, etc.)
- 6 system tables (Ontology terms, Type definitions, Process records)
- 44 MB database with full-text search and provenance tracking

See [CDM Store Quick Start Guide](docs/cdm_store_quickstart.md) for detailed examples and Python API usage.

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [src/](src/) - source files (edit these)
  * [linkml_coral](src/linkml_coral)
    * [schema/](src/linkml_coral/schema) -- LinkML schema
      (edit this)
    * [datamodel/](src/linkml_coral/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests
  * [data/](tests/data) - Example data

## Developer Tools

There are several pre-defined command-recipes available.
They are written for the command runner [just](https://github.com/casey/just/). To list all pre-defined commands, run `just` or `just --list`.

## Credits

This project uses the template [linkml-project-copier](https://github.com/dalito/linkml-project-copier) published as [doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584).
