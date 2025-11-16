## Entity Relationship Matrix

| From \ To | Assembly | Bin | Community | Condition | DubSeq_Library | Gene | Genome | Image | Location | OTU | Process | Protocol | Reads | Sample | Strain | Taxon | TnSeq_Library |
|------------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| **Assembly** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | assembly_strain | - | - |
| **Bin** | bin_assembly | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **Community** | - | - | community_parent_community | community_condition | - | - | - | - | - | - | - | - | - | community_sample | community_defined_strains | - | - |
| **Condition** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **DubSeq_Library** | - | - | - | - | - | - | dubseq_library_genome | - | - | - | - | - | - | - | - | - | - |
| **Gene** | - | - | - | - | - | - | gene_genome | - | - | - | - | - | - | - | - | - | - |
| **Genome** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | genome_strain | - | - |
| **Image** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **Location** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **OTU** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **Process** | - | - | - | - | - | - | - | - | - | - | - | process_protocol | - | - | - | - | - |
| **Protocol** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **Reads** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **Sample** | - | - | - | - | - | - | - | - | sample_location | - | - | - | - | - | - | - | - |
| **Strain** | - | - | - | - | - | strain_genes_changed | strain_genome | - | - | - | - | - | - | - | strain_derived_from | - | - |
| **Taxon** | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **TnSeq_Library** | - | - | - | - | - | - | tnseq_library_genome | - | - | - | - | - | - | - | - | - | - |
