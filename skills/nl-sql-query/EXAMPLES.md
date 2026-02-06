# Natural Language SQL Query Examples

This file contains example queries you can use with the `/nl-sql-query` skill.

## Basic Statistics

### Count Records
```
How many samples are in the database?
Count all reads
Show total number of assemblies
How many locations do we have?
```

### Simple Queries
```
List all location IDs
Show me the first 10 samples
Display all sample materials
What ontology terms are available?
```

## Filtered Queries

### Numeric Filters
```
Find samples with depth greater than 100
Show reads with read_count over 50000
List assemblies with more than 100 contigs
Find samples collected at depths between 50 and 200
```

### String Filters
```
Find samples from location "Location0000001"
Show reads with type "ME:0000113"
List samples where material contains "soil"
Find assemblies with name starting with "Assembly"
```

### Date Filters
```
Show samples collected after 2020-01-01
Find reads sequenced in 2021
List assemblies created between 2019 and 2022
```

## Aggregations

### Counts and Groups
```
Count samples by location
Show read counts grouped by sample
List assemblies per genome
Count samples by material type
```

### Top N Queries
```
Top 10 locations by sample count
Show 5 samples with highest depth values
List 10 reads with most read counts
Find top 20 most abundant OTUs
```

### Statistical Aggregations
```
Average read count per sample
Maximum depth across all samples
Minimum, maximum, and average assembly size
Sum of all read counts by location
```

## Joins and Relationships

### Two-Table Joins
```
Show samples with their location names
Find reads with their corresponding sample IDs
List assemblies with their sample information
Show genes with their genome names
```

### Multi-Table Joins
```
Show the complete pipeline: sample → reads → assembly
Find locations with their samples and read counts
List genomes with their assemblies and sample sources
Display OTUs with their sample locations
```

### Provenance Chains
```
Trace assemblies back to their source samples
Find all reads that led to specific assemblies
Show complete lineage from location to genes
Map samples to their downstream products
```

## Complex Queries

### Conditional Logic
```
Find samples with depth > 100 OR read_count > 50000
Show reads that are either Illumina or PacBio
List samples from locations in California or Oregon
Find assemblies that are either complete or high-quality
```

### Subqueries
```
Find samples with above-average depth
Show locations with more samples than the median
List reads from the top 10 most sampled locations
Find assemblies from high-quality reads
```

### Window Functions
```
Rank samples by depth within each location
Show running total of samples over time
Calculate moving average of read counts
Find percentile ranks for assembly sizes
```

## Domain-Specific Queries

### Sequencing Analysis
```
Compare read counts across sequencing technologies
Find paired-end vs single-end read statistics
List assemblies by sequencing platform
Show distribution of read lengths
```

### Taxonomic Analysis
```
Count OTUs by taxonomic rank
Find most abundant species in each sample
List unique taxonomic classifications
Show diversity metrics by location
```

### Provenance Tracking
```
Find all process records for a specific sample
Show process types and their frequencies
List inputs and outputs for assembly processes
Track sample processing workflow
```

### Geographic Analysis
```
Count samples by latitude range
Find locations with coordinates in specific region
Show sample distribution by elevation
List samples from marine vs terrestrial environments
```

## Data Quality Queries

### Missing Data
```
Find samples with NULL depth values
Show reads without assembly associations
List samples missing material information
Count records with incomplete metadata
```

### Data Validation
```
Find duplicate sample IDs
Show samples with impossible coordinate values
List reads with zero read counts
Identify assemblies without associated reads
```

### Data Coverage
```
Calculate percentage of samples with depth data
Show completeness rate for each field
Count samples with all required metadata
List fields with most missing values
```

## Performance Tips

### Good Queries (Fast)
```
✓ Find first 100 samples with depth > 50
✓ Show top 10 locations by sample count
✓ Count reads by type (with proper GROUP BY)
✓ List samples with specific IDs
```

### Queries to Avoid (Slow)
```
✗ Show all 82 million brick table rows
✗ Calculate statistics without LIMIT
✗ Join all tables without filters
✗ Wildcard searches across large text fields
```

## Troubleshooting

### Query Returns Empty Results
Try adding LIMIT to see if data exists:
```
Show first 10 records from sdt_sample
List any samples in the database
```

### Query Too Slow
Add filters and limits:
```
Find top 100 samples (not all samples) with depth > 50
Show 10 most recent assemblies
```

### SQL Syntax Error
Use more specific terms:
```
Instead of: "Show samples where it's deep"
Use: "Find samples with depth > 100"

Instead of: "Get the best assemblies"
Use: "Show assemblies with contig_count > 50"
```

## Example Session

```
User: How many samples are in the database?
Result: 15,234 samples

User: Show me the top 5 locations by sample count
Result:
  Location_ID      | Sample_Count
  -----------------|-------------
  Location0000001  | 523
  Location0000042  | 387
  Location0000089  | 251
  ...

User: Find samples from Location0000001 with depth > 100
Result: 89 samples found

User: What's the average read count for those samples?
Result: Average read_count: 127,453
```

## Additional Resources

- [DuckDB SQL Documentation](https://duckdb.org/docs/sql/introduction)
- [CDM Schema Reference](../../docs/CDM_PARQUET_STORE_GUIDE.md)
- [Query Best Practices](../../docs/QUERY_REFERENCE.md)
