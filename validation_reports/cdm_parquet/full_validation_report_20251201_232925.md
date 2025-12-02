# CDM Parquet Full Validation Report

**Generated:** 2025-12-01 23:31:36  
**Schema:** `src/linkml_coral/schema/cdm/linkml_coral_cdm.yaml`

## Summary

- **Tables validated:** 24
- **Total rows:** 555,348
- **Tables passed:** 3 ✅
- **Tables failed:** 21 ❌
- **Total errors:** 133,138

## Error Types

| Error Type | Count | Percentage |
|------------|-------|------------|
| Schema Mismatch | 103,114 | 77.4% |
| Other | 27,865 | 20.9% |
| Type Violation | 2,159 | 1.6% |

## Tables with Errors

### ddt_ndarray (DynamicDataArray)

- **Row count:** 20
- **Validated rows:** 20
- **Errors:** 0

### sdt_assembly (Assembly)

- **Row count:** 3,427
- **Validated rows:** 3,427
- **Errors:** 6,075

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/0] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/1] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/2] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/3] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/4] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/5] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/6] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/7] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/8] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp1b04xan_.yaml/9] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
   ... and 6065 more errors

### sdt_bin (Bin)

- **Row count:** 623
- **Validated rows:** 623
- **Errors:** 0

### sdt_community (Community)

- **Row count:** 2,209
- **Validated rows:** 2,209
- **Errors:** 0

### sdt_condition (Condition)

- **Row count:** 1,046
- **Validated rows:** 1,046
- **Errors:** 553

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/184] '30°C + aerobic + Sediment extract to 1/25 LB' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/185] '25°C + aerobic + aphotic + filter on  1/25 R2A' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/186] '30°C + aerobic + LB' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/187] '30°C + aerobic + Eugon' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/188] '30°C + aerobic + R2A' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/189] '30°C + aerobic + LB + Mn' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/190] '30°C + aerobic + TSA' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/191] '30°C + anaerobic + TSA' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/192] '30°C + aerobic + Mn + Mo + R2A' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpp4lkkh_c.yaml/193] '30°C + aerobic + Mn + TSA' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_condition_name`
   ... and 543 more errors

### sdt_dubseq_library (DubSeqLibrary)

- **Row count:** 3
- **Validated rows:** 3
- **Errors:** 6

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp4jp5m3aw.yaml/0] Additional properties are not allowed ('sdt_genome_name' was unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp4jp5m3aw.yaml/0] 'DubSeq_Library0000001' does not match '^DubSeqLibrary\\d{7}$' in /sdt_dubseq_library_id`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp4jp5m3aw.yaml/1] Additional properties are not allowed ('sdt_genome_name' was unexpected) in /`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp4jp5m3aw.yaml/1] 'DubSeq_Library0000002' does not match '^DubSeqLibrary\\d{7}$' in /sdt_dubseq_library_id`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp4jp5m3aw.yaml/2] Additional properties are not allowed ('sdt_genome_name' was unexpected) in /`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp4jp5m3aw.yaml/2] 'DubSeq_Library0000003' does not match '^DubSeqLibrary\\d{7}$' in /sdt_dubseq_library_id`

### sdt_enigma (ENIGMA)

- **Row count:** 1
- **Validated rows:** 1
- **Errors:** 1

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp3usxp9ki.yaml/0] None is not of type 'string' in /sdt_enigma_id`

### sdt_gene (Gene)

- **Row count:** 15,015
- **Validated rows:** 15,015
- **Errors:** 0

### sdt_genome (Genome)

- **Row count:** 6,688
- **Validated rows:** 6,688
- **Errors:** 10,577

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/0] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/1] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/2] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/3] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/4] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/5] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/6] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/7] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/8] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpcm_6nmuj.yaml/9] Additional properties are not allowed ('sdt_strain_name' was unexpected) in /`
   ... and 10567 more errors

### sdt_image (Image)

- **Row count:** 218
- **Validated rows:** 218
- **Errors:** 218

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/0] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/1] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/2] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/3] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/4] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/5] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/6] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/7] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/8] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpndu0_ux0.yaml/9] Additional properties are not allowed ('sdt_image_description' was unexpected) in /`
   ... and 208 more errors

### sdt_reads (Reads)

- **Row count:** 19,307
- **Validated rows:** 19,307
- **Errors:** 15,709

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1242] '51939/GW821-FHT01H10.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1243] '51939/GW821-FHT01H11.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1244] '51939/GW823-FHT04A10.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1245] '51939/GW822-FHT03B10.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1246] '51939/GW823-FHT02F01.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1247] '51939/GW823-FHT02F03.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1248] '51939/GW822-FHT04C12.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1249] '51939/GW822-FHT04C11.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1250] '51939/GW821-FHT03B11.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpq40fm9c7.yaml/1251] '51939/GW822-FHT01H04.reads' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_reads_name`
   ... and 15699 more errors

### sdt_sample (Sample)

- **Row count:** 4,330
- **Validated rows:** 4,330
- **Errors:** 9,367

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/0] Additional properties are not allowed ('sdt_location_name', 'sdt_sample_description' were unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/0] '6:59' does not match '^\\d{2}:\\d{2}(:\\d{2})?$' in /time`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/0] 'MIxS:0000017' does not match '^[A-Z_]+:\\d+$' in /env_package_sys_oterm_id`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/1] Additional properties are not allowed ('sdt_location_name', 'sdt_sample_description' were unexpected) in /`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/1] '8:09' does not match '^\\d{2}:\\d{2}(:\\d{2})?$' in /time`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/1] 'MIxS:0000017' does not match '^[A-Z_]+:\\d+$' in /env_package_sys_oterm_id`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/2] Additional properties are not allowed ('sdt_location_name', 'sdt_sample_description' were unexpected) in /`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/2] '8:58' does not match '^\\d{2}:\\d{2}(:\\d{2})?$' in /time`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/2] 'MIxS:0000017' does not match '^[A-Z_]+:\\d+$' in /env_package_sys_oterm_id`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpu6n1gd3b.yaml/3] Additional properties are not allowed ('sdt_location_name', 'sdt_sample_description' were unexpected) in /`
   ... and 9357 more errors

### sdt_strain (Strain)

- **Row count:** 3,110
- **Validated rows:** 3,110
- **Errors:** 0

### sdt_taxon (Taxon)

- **Row count:** 3,276
- **Validated rows:** 3,276
- **Errors:** 2,183

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/16] 'NCBITaxon:46123' is not of type 'integer', 'null' in /ncbi_taxid`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/17] 'Absconditabacteriales (SR1)' does not match '^[A-Za-z0-9_\\-. ]+$' in /sdt_taxon_name`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/19] 'NCBITaxon:5756' is not of type 'integer', 'null' in /ncbi_taxid`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/20] 'NCBITaxon:1427378' is not of type 'integer', 'null' in /ncbi_taxid`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/21] 'NCBITaxon:31980' is not of type 'integer', 'null' in /ncbi_taxid`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/22] 'NCBITaxon:35829' is not of type 'integer', 'null' in /ncbi_taxid`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/23] 'NCBITaxon:186831' is not of type 'integer', 'null' in /ncbi_taxid`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/24] 'NCBITaxon:433' is not of type 'integer', 'null' in /ncbi_taxid`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/27] 'NCBITaxon:33951' is not of type 'integer', 'null' in /ncbi_taxid`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpoee23pgp.yaml/28] 'NCBITaxon:1647173' is not of type 'integer', 'null' in /ncbi_taxid`
   ... and 2173 more errors

### sdt_tnseq_library (TnSeqLibrary)

- **Row count:** 1
- **Validated rows:** 1
- **Errors:** 2

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2_86xx6g.yaml/0] Additional properties are not allowed ('hit_rate_essential', 'hit_rate_other', 'n_barcodes', 'n_insertion_locations', 'n_usable_barcodes', 'sdt_genome_name' were unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2_86xx6g.yaml/0] 'TnSeq_Library0000001' does not match '^TnSeqLibrary\\d{7}$' in /sdt_tnseq_library_id`

### sys_ddt_typedef (SystemDDTTypedef)

- **Row count:** 101
- **Validated rows:** 101
- **Errors:** 101

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/0] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/1] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/2] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/3] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/4] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/5] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/6] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/7] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/8] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmpin2xk8pe.yaml/9] Additional properties are not allowed ('comment', 'fk', 'original_csv_string' were unexpected) in /`
   ... and 91 more errors

### sys_oterm (SystemOntologyTerm)

- **Row count:** 10,594
- **Validated rows:** 10,594
- **Errors:** 0

### sys_process (SystemProcess)

- **Row count:** 142,958
- **Validated rows:** 50,000
- **Errors:** 0

### sys_process_input (SystemProcessInput)

- **Row count:** 90,395
- **Validated rows:** 50,000
- **Errors:** 50,000

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/0] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/1] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/2] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/3] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/4] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/5] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/6] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/7] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/8] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2k3tusuz.yaml/9] Additional properties are not allowed ('sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_genome_id', 'sdt_location_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
   ... and 49990 more errors

### sys_process_output (SystemProcessOutput)

- **Row count:** 38,228
- **Validated rows:** 38,228
- **Errors:** 38,228

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/0] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/1] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/2] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/3] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/4] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/5] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/6] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/7] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/8] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp0rzrtlwt.yaml/9] Additional properties are not allowed ('ddt_ndarray_id', 'sdt_assembly_id', 'sdt_bin_id', 'sdt_community_id', 'sdt_dubseq_library_id', 'sdt_genome_id', 'sdt_image_id', 'sdt_reads_id', 'sdt_sample_id', 'sdt_strain_id', 'sdt_tnseq_library_id' were unexpected) in /`
   ... and 38218 more errors

### sys_typedef (SystemTypedef)

- **Row count:** 118
- **Validated rows:** 118
- **Errors:** 118

**Error samples:**

1. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/0] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
2. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/1] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
3. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/2] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
4. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/3] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
5. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/4] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
6. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/5] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
7. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/6] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
8. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/7] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
9. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/8] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
10. `[ERROR] [/var/folders/7w/ksxs106s7_sg14v6cb2y70vr0000gn/T/tmp2oitz24g.yaml/9] Additional properties are not allowed ('comment', 'required' were unexpected) in /`
   ... and 108 more errors

## Tables Passed

- ✅ **sdt_asv** (213,044 rows)
- ✅ **sdt_location** (594 rows)
- ✅ **sdt_protocol** (42 rows)

## Detailed Results

| Table | Class | Rows | Validated | Status | Errors | Time (s) |
|-------|-------|------|-----------|--------|--------|----------|
| ddt_ndarray | DynamicDataArray | 20 | 20 | ❌ FAIL | 0 | 0.37 |
| sdt_assembly | Assembly | 3,427 | 3,427 | ❌ FAIL | 6,075 | 2.27 |
| sdt_asv | ASV | 213,044 | 213,044 | ✅ PASS | 0 | 32.56 |
| sdt_bin | Bin | 623 | 623 | ❌ FAIL | 0 | 0.36 |
| sdt_community | Community | 2,209 | 2,209 | ❌ FAIL | 0 | 0.42 |
| sdt_condition | Condition | 1,046 | 1,046 | ❌ FAIL | 553 | 1.28 |
| sdt_dubseq_library | DubSeqLibrary | 3 | 3 | ❌ FAIL | 6 | 1.07 |
| sdt_enigma | ENIGMA | 1 | 1 | ❌ FAIL | 1 | 1.11 |
| sdt_gene | Gene | 15,015 | 15,015 | ❌ FAIL | 0 | 0.39 |
| sdt_genome | Genome | 6,688 | 6,688 | ❌ FAIL | 10,577 | 3.75 |
| sdt_image | Image | 218 | 218 | ❌ FAIL | 218 | 1.20 |
| sdt_location | Location | 594 | 594 | ✅ PASS | 0 | 1.95 |
| sdt_protocol | Protocol | 42 | 42 | ✅ PASS | 0 | 1.12 |
| sdt_reads | Reads | 19,307 | 19,307 | ❌ FAIL | 15,709 | 13.11 |
| sdt_sample | Sample | 4,330 | 4,330 | ❌ FAIL | 9,367 | 4.37 |
| sdt_strain | Strain | 3,110 | 3,110 | ❌ FAIL | 0 | 0.36 |
| sdt_taxon | Taxon | 3,276 | 3,276 | ❌ FAIL | 2,183 | 1.77 |
| sdt_tnseq_library | TnSeqLibrary | 1 | 1 | ❌ FAIL | 2 | 1.30 |
| sys_ddt_typedef | SystemDDTTypedef | 101 | 101 | ❌ FAIL | 101 | 1.17 |
| sys_oterm | SystemOntologyTerm | 10,594 | 10,594 | ❌ FAIL | 0 | 0.38 |
| sys_process | SystemProcess | 142,958 | 50,000 | ❌ FAIL | 0 | 0.51 |
| sys_process_input | SystemProcessInput | 90,395 | 50,000 | ❌ FAIL | 50,000 | 30.77 |
| sys_process_output | SystemProcessOutput | 38,228 | 38,228 | ❌ FAIL | 38,228 | 27.97 |
| sys_typedef | SystemTypedef | 118 | 118 | ❌ FAIL | 118 | 1.16 |

## Recommendations

### Schema Mismatches
- Update CDM schema to include missing fields
- Or remove unexpected columns from parquet data

### Type Violations
- Ensure data types match schema expectations
- Add type conversion at ETL stage
