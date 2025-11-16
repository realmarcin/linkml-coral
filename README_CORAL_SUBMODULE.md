# CORAL Submodule

This directory contains the CORAL repository as a git submodule.

## Purpose

The CORAL repository provides the source `typedef.json` file located at:
```
CORAL/back_end/python/var/typedef.json
```

This file is the authoritative source for ENIGMA Common Data Model type definitions that are converted to LinkML schemas.

## Setup

When cloning linkml-coral for the first time:
```bash
git clone https://github.com/realmarcin/linkml-coral
cd linkml-coral
git submodule update --init --recursive
```

## Updating

To pull the latest changes from CORAL:
```bash
git submodule update --remote CORAL
```

To sync the typedef.json to the convenience copy in `data/`:
```bash
cp CORAL/back_end/python/var/typedef.json data/
```

## Repository

- **URL**: https://github.com/jmchandonia/CORAL
- **Purpose**: CORAL (Common Ontology for Research and Analysis of Live systems)
- **Key File**: `back_end/python/var/typedef.json` - ENIGMA data model type definitions
