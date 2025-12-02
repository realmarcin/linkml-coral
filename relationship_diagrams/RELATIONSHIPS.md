# CORAL LinkML Schema - Relationship Documentation

## Overview

This document describes the relationships between entities in the ENIGMA Common Data Model.

- **Total relationships**: 15
- **One-to-one/Many-to-one**: 12
- **Many-to-many**: 1
- **Self-referential**: 2
- **Provenance-tracked entities**: 0

## Relationship Reference

### One-to-One and Many-to-One Relationships

| Source Entity | Slot | Target Entity | Target Field | Required |
|---------------|------|---------------|--------------|----------|
| `Assembly` | `assembly_strain` | `Strain` | `name` |  |
| `Bin` | `bin_assembly` | `Assembly` | `name` | ✓ |
| `Community` | `community_condition` | `Condition` | `name` |  |
| `Community` | `community_sample` | `Sample` | `name` |  |
| `Community` | `community_defined_strains` | `Strain` | `name` |  |
| `DubSeq_Library` | `dubseq_library_genome` | `Genome` | `name` | ✓ |
| `Gene` | `gene_genome` | `Genome` | `name` | ✓ |
| `Genome` | `genome_strain` | `Strain` | `name` |  |
| `Process` | `process_protocol` | `Protocol` | `name` |  |
| `Sample` | `sample_location` | `Location` | `name` | ✓ |
| `Strain` | `strain_genome` | `Genome` | `name` |  |
| `TnSeq_Library` | `tnseq_library_genome` | `Genome` | `name` | ✓ |

### Many-to-Many Relationships

| Source Entity | Slot | Target Entity | Target Field | Required |
|---------------|------|---------------|--------------|----------|
| `Strain` | `strain_genes_changed` | `Gene` | `gene_id` |  |

### Self-Referential Relationships

These relationships create hierarchies within a single entity type:

| Entity | Slot | Target Field | Description |
|--------|------|--------------|-------------|
| `Community` | `community_parent_community` | `name` | Hierarchical relationship |
| `Strain` | `strain_derived_from` | `name` | Derived relationship |

## Entity Relationship Graph

```
Assembly
  --> Strain [assembly_strain]
Bin
  --> Assembly [bin_assembly]
Community
  --> Sample [community_sample]
  --> Community [community_parent_community] (self-reference)
  --> Condition [community_condition]
  --> Strain [community_defined_strains]
DubSeq_Library
  --> Genome [dubseq_library_genome]
Gene
  --> Genome [gene_genome]
Genome
  --> Strain [genome_strain]
Process
  --> Protocol [process_protocol]
Sample
  --> Location [sample_location]
Strain
  --> Genome [strain_genome]
  --> Strain [strain_derived_from] (self-reference)
  ==> Gene [strain_genes_changed]
TnSeq_Library
  --> Genome [tnseq_library_genome]
```
