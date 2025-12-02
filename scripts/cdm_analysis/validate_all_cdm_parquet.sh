#!/usr/bin/env bash
#
# Validate all CDM parquet tables against LinkML schema
#
# This script validates all 44 parquet tables from the KBase CDM database.
# It uses different strategies based on table size:
# - Small tables (<100K rows): Full validation
# - Medium tables (100K-1M rows): Full validation with chunking
# - Large tables (>1M rows): Sample validation (first 10K rows)
#
# Usage:
#   ./validate_all_cdm_parquet.sh [database_path]
#   ./validate_all_cdm_parquet.sh /path/to/jmc_coral.db

set -euo pipefail

# Default database path
CDM_DB="${1:-/Users/marcin/Documents/VIMSS/ENIGMA/KBase/ENIGMA_in_CDM/minio/jmc_coral.db}"

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Output directory for validation reports
OUTPUT_DIR="${REPO_ROOT}/validation_reports/cdm_parquet"
mkdir -p "${OUTPUT_DIR}"

# Log file
LOG_FILE="${OUTPUT_DIR}/validation_$(date +%Y%m%d_%H%M%S).log"

# Validation script
VALIDATE_SCRIPT="${SCRIPT_DIR}/validate_parquet_linkml.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
total_tables=0
passed_tables=0
failed_tables=0
skipped_tables=0

log() {
    echo -e "$@" | tee -a "${LOG_FILE}"
}

validate_table() {
    local table_path="$1"
    local table_name="$(basename "${table_path}")"
    local class_name="$2"
    local strategy="$3"  # "full", "chunked", or "sample"
    local max_rows="${4:-}"
    local chunk_size="${5:-}"

    total_tables=$((total_tables + 1))

    log "${BLUE}[${total_tables}]${NC} Validating ${table_name} (${class_name}, strategy: ${strategy})..."

    local args=("${table_path}" "--class" "${class_name}")

    case "${strategy}" in
        full)
            # Full validation for small tables
            ;;
        chunked)
            # Chunked validation for medium tables
            args+=("--chunk-size" "${chunk_size}")
            ;;
        sample)
            # Sample validation for large tables
            args+=("--max-rows" "${max_rows}")
            log "${YELLOW}  Note: Validating only first ${max_rows} rows${NC}"
            ;;
    esac

    if uv run python "${VALIDATE_SCRIPT}" "${args[@]}" >> "${LOG_FILE}" 2>&1; then
        log "${GREEN}  ✅ PASSED${NC}"
        passed_tables=$((passed_tables + 1))
        return 0
    else
        log "${RED}  ❌ FAILED${NC}"
        log "${RED}  See ${LOG_FILE} for details${NC}"
        failed_tables=$((failed_tables + 1))
        return 1
    fi
}

# Check if database exists
if [[ ! -d "${CDM_DB}" ]]; then
    log "${RED}Error: Database not found at ${CDM_DB}${NC}"
    exit 1
fi

log "================================================"
log "CDM Parquet Validation Report"
log "================================================"
log "Database: ${CDM_DB}"
log "Log file: ${LOG_FILE}"
log "Started: $(date)"
log ""

# Static entity tables (sdt_*) - typically small to medium
log "${BLUE}=== Static Entity Tables (sdt_*) ===${NC}"
log ""

# Small tables (<100K rows)
validate_table "${CDM_DB}/sdt_location" "Location" "full"
validate_table "${CDM_DB}/sdt_sample" "Sample" "full"
validate_table "${CDM_DB}/sdt_community" "Community" "full"
validate_table "${CDM_DB}/sdt_reads" "Reads" "chunked" "" "10000"
validate_table "${CDM_DB}/sdt_assembly" "Assembly" "full"
validate_table "${CDM_DB}/sdt_bin" "Bin" "full"
validate_table "${CDM_DB}/sdt_genome" "Genome" "full"
validate_table "${CDM_DB}/sdt_strain" "Strain" "full"
validate_table "${CDM_DB}/sdt_taxon" "Taxon" "full"
validate_table "${CDM_DB}/sdt_asv" "ASV" "full"
validate_table "${CDM_DB}/sdt_protocol" "Protocol" "full"
validate_table "${CDM_DB}/sdt_image" "Image" "full"
validate_table "${CDM_DB}/sdt_condition" "Condition" "full"
validate_table "${CDM_DB}/sdt_dubseq_library" "DubSeqLibrary" "full"
validate_table "${CDM_DB}/sdt_tnseq_library" "TnSeqLibrary" "full"
validate_table "${CDM_DB}/sdt_enigma" "ENIGMA" "full"

# Large table (genes)
validate_table "${CDM_DB}/sdt_gene" "Gene" "sample" "10000"

log ""
log "${BLUE}=== System Tables (sys_*) ===${NC}"
log ""

validate_table "${CDM_DB}/sys_typedef" "SystemTypedef" "full"
validate_table "${CDM_DB}/sys_ddt_typedef" "SystemDDTTypedef" "full"
validate_table "${CDM_DB}/sys_oterm" "SystemOntologyTerm" "chunked" "" "5000"

# Large tables (process)
validate_table "${CDM_DB}/sys_process" "SystemProcess" "sample" "10000"
validate_table "${CDM_DB}/sys_process_input" "SystemProcessInput" "sample" "10000"
validate_table "${CDM_DB}/sys_process_output" "SystemProcessOutput" "sample" "10000"

log ""
log "${BLUE}=== Dynamic Data Tables (ddt_*) ===${NC}"
log ""

validate_table "${CDM_DB}/ddt_ndarray" "DynamicDataArray" "full"

log ""
log "${YELLOW}Note: Skipping individual brick tables (ddt_brick*) - 20 tables with 82M+ total rows${NC}"
log "${YELLOW}      These have heterogeneous schemas and require custom validation${NC}"
skipped_tables=20

log ""
log "================================================"
log "Validation Summary"
log "================================================"
log "Total tables validated: ${total_tables}"
log "  ${GREEN}✅ Passed: ${passed_tables}${NC}"
log "  ${RED}❌ Failed: ${failed_tables}${NC}"
log "  ${YELLOW}⊘ Skipped: ${skipped_tables}${NC}"
log ""
log "Completed: $(date)"
log "Full log: ${LOG_FILE}"
log ""

if [[ ${failed_tables} -gt 0 ]]; then
    log "${RED}Validation completed with ${failed_tables} failures${NC}"
    exit 1
else
    log "${GREEN}All validated tables passed!${NC}"
    exit 0
fi
