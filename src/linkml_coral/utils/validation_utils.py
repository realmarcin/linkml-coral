#!/usr/bin/env python3
"""
Validation utilities for ENIGMA TSV data.

Provides comprehensive validation infrastructure including:
- Enum value validation
- Foreign key validation
- Data quality metrics
- Validation result aggregation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any, Tuple
from enum import Enum
from pathlib import Path
import re
import statistics
from linkml_runtime.utils.schemaview import SchemaView


class ValidationStatus(Enum):
    """Validation result status."""
    PASS = "PASS"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class ValidationResult:
    """Individual validation result."""
    status: ValidationStatus
    message: str
    field_name: Optional[str] = None
    value: Optional[str] = None
    expected: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'status': self.status.value,
            'message': self.message,
            'field': self.field_name,
            'value': self.value,
            'expected': self.expected,
            'context': self.context
        }


@dataclass
class RecordValidationResult:
    """Validation results for a single record."""
    record_line: int
    entity_id: Optional[str]
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def status(self) -> ValidationStatus:
        """Overall status for this record."""
        if any(r.status == ValidationStatus.ERROR for r in self.results):
            return ValidationStatus.ERROR
        if any(r.status == ValidationStatus.WARNING for r in self.results):
            return ValidationStatus.WARNING
        return ValidationStatus.PASS

    @property
    def error_count(self) -> int:
        """Number of errors."""
        return sum(1 for r in self.results if r.status == ValidationStatus.ERROR)

    @property
    def warning_count(self) -> int:
        """Number of warnings."""
        return sum(1 for r in self.results if r.status == ValidationStatus.WARNING)


@dataclass
class FileValidationResult:
    """Validation results for an entire file."""
    filename: str
    total_records: int
    record_results: List[RecordValidationResult] = field(default_factory=list)
    quality_metrics: Dict[str, Any] = field(default_factory=dict)

    @property
    def pass_count(self) -> int:
        """Number of records that passed."""
        return sum(1 for r in self.record_results if r.status == ValidationStatus.PASS)

    @property
    def warning_count(self) -> int:
        """Number of records with warnings."""
        return sum(1 for r in self.record_results if r.status == ValidationStatus.WARNING)

    @property
    def error_count(self) -> int:
        """Number of records with errors."""
        return sum(1 for r in self.record_results if r.status == ValidationStatus.ERROR)

    @property
    def pass_rate(self) -> float:
        """Percentage of records that passed."""
        if self.total_records == 0:
            return 0.0
        return self.pass_count / self.total_records

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'filename': self.filename,
            'total_records': self.total_records,
            'pass_count': self.pass_count,
            'warning_count': self.warning_count,
            'error_count': self.error_count,
            'pass_rate': self.pass_rate,
            'record_results': [
                {
                    'record_line': r.record_line,
                    'entity_id': r.entity_id,
                    'status': r.status.value,
                    'error_count': r.error_count,
                    'warning_count': r.warning_count,
                    'results': [vr.to_dict() for vr in r.results]
                }
                for r in self.record_results
            ],
            'quality_metrics': self.quality_metrics
        }


class EnumValidator:
    """Validates enum field values against schema definitions."""

    def __init__(self, schema: SchemaView):
        """
        Initialize enum validator.

        Args:
            schema: LinkML schema view
        """
        self.schema = schema
        self._enum_cache: Dict[str, Set[str]] = {}

    def _get_enum_values(self, enum_name: str) -> Set[str]:
        """Get all permissible values for an enum."""
        if enum_name in self._enum_cache:
            return self._enum_cache[enum_name]

        enum_def = self.schema.get_enum(enum_name)
        if not enum_def or not enum_def.permissible_values:
            self._enum_cache[enum_name] = set()
            return set()

        # Get all permissible value keys
        values = set(enum_def.permissible_values.keys())
        self._enum_cache[enum_name] = values
        return values

    def _parse_ontology_term(self, value: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Parse ontology term format: "Label <PREFIX:ID>".

        Returns:
            Tuple of (label, prefix, id) or (None, None, None) if invalid
        """
        if not value:
            return None, None, None

        # Pattern: "Label <PREFIX:ID>"
        match = re.match(r'^(.+?)\s+<([A-Z_]+):(\d+)>$', value.strip())
        if match:
            return match.group(1), match.group(2), match.group(3)

        return None, None, None

    def validate(self, slot_name: str, value: Any, enum_name: Optional[str] = None) -> ValidationResult:
        """
        Validate an enum field value.

        Args:
            slot_name: Name of the slot/field
            value: Value to validate
            enum_name: Name of the enum (if known), otherwise inferred from slot

        Returns:
            ValidationResult
        """
        if value is None or value == '':
            return ValidationResult(
                status=ValidationStatus.PASS,
                message="Empty value allowed for optional field",
                field_name=slot_name
            )

        # Get enum name from slot if not provided
        if not enum_name:
            slot = self.schema.induced_slot(slot_name)
            if not slot or not slot.range:
                return ValidationResult(
                    status=ValidationStatus.PASS,
                    message="No enum range defined for slot",
                    field_name=slot_name
                )
            enum_name = slot.range

        # Check if it's actually an enum
        enum_def = self.schema.get_enum(enum_name)
        if not enum_def:
            return ValidationResult(
                status=ValidationStatus.PASS,
                message=f"Range {enum_name} is not an enum",
                field_name=slot_name
            )

        # Get valid enum values
        valid_values = self._get_enum_values(enum_name)
        if not valid_values:
            return ValidationResult(
                status=ValidationStatus.WARNING,
                message=f"Enum {enum_name} has no permissible values defined",
                field_name=slot_name
            )

        # Handle ontology term format
        label, prefix, term_id = self._parse_ontology_term(str(value))
        if label is not None:
            # For ontology terms, we need to match against the value without the ontology annotation
            # This is a simplification - ideally we'd validate the ontology term itself
            # For now, just pass if it has the right format
            return ValidationResult(
                status=ValidationStatus.PASS,
                message=f"Ontology term format valid",
                field_name=slot_name,
                value=str(value)
            )

        # Direct value match
        if str(value) in valid_values:
            return ValidationResult(
                status=ValidationStatus.PASS,
                message="Valid enum value",
                field_name=slot_name,
                value=str(value)
            )

        # Value not found
        return ValidationResult(
            status=ValidationStatus.ERROR,
            message=f"Invalid enum value",
            field_name=slot_name,
            value=str(value),
            expected=f"One of: {', '.join(sorted(list(valid_values)[:5]))}{'...' if len(valid_values) > 5 else ''}",
            context={'valid_values': list(valid_values)}
        )


class ForeignKeyValidator:
    """Validates foreign key references."""

    def __init__(self, fk_index: Optional[Dict[str, Set[str]]] = None):
        """
        Initialize FK validator.

        Args:
            fk_index: Dictionary mapping entity type to set of valid IDs
        """
        self.fk_index = fk_index or {}

    def add_entities(self, entity_type: str, entity_ids: Set[str]):
        """Add entities to the FK index."""
        if entity_type not in self.fk_index:
            self.fk_index[entity_type] = set()
        self.fk_index[entity_type].update(entity_ids)

    def validate(self, source_field: str, target_class: str, value: Any) -> ValidationResult:
        """
        Validate a foreign key reference.

        Args:
            source_field: Name of the source field
            target_class: Target entity class name
            value: FK value to validate

        Returns:
            ValidationResult
        """
        if value is None or value == '':
            return ValidationResult(
                status=ValidationStatus.PASS,
                message="Empty FK value allowed for optional field",
                field_name=source_field
            )

        # Handle multivalued FKs (array notation)
        if isinstance(value, list):
            results = []
            for v in value:
                result = self.validate(source_field, target_class, v)
                if result.status != ValidationStatus.PASS:
                    results.append(result)

            if results:
                return ValidationResult(
                    status=ValidationStatus.ERROR,
                    message=f"{len(results)} invalid FK references in multivalued field",
                    field_name=source_field,
                    value=str(value),
                    context={'invalid_references': [r.value for r in results]}
                )
            return ValidationResult(
                status=ValidationStatus.PASS,
                message="All FK references valid",
                field_name=source_field
            )

        # Parse bracket notation: [EntityType:ID]
        str_value = str(value).strip()
        match = re.match(r'^\[([^:]+):([^\]]+)\]$', str_value)
        if match:
            entity_type = match.group(1)
            entity_id = match.group(2)

            # Check if entity type matches target class
            if entity_type != target_class:
                return ValidationResult(
                    status=ValidationStatus.WARNING,
                    message=f"FK entity type mismatch",
                    field_name=source_field,
                    value=str_value,
                    expected=f"[{target_class}:...]",
                    context={'actual_type': entity_type, 'expected_type': target_class}
                )
        else:
            # Plain ID reference
            entity_id = str_value

        # Check if target entity exists in index
        if target_class not in self.fk_index:
            return ValidationResult(
                status=ValidationStatus.WARNING,
                message=f"No FK index available for {target_class}",
                field_name=source_field,
                value=entity_id
            )

        valid_ids = self.fk_index[target_class]
        if entity_id not in valid_ids:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message=f"FK reference not found",
                field_name=source_field,
                value=entity_id,
                expected=f"Valid {target_class} ID",
                context={'target_class': target_class, 'available_count': len(valid_ids)}
            )

        return ValidationResult(
            status=ValidationStatus.PASS,
            message="FK reference valid",
            field_name=source_field,
            value=entity_id
        )


@dataclass
class FieldMetrics:
    """Data quality metrics for a field."""
    field_name: str
    total_values: int
    non_empty_count: int
    unique_count: int
    completeness: float  # Percentage non-empty
    value_distribution: Dict[str, int] = field(default_factory=dict)  # Top values
    numeric_stats: Optional[Dict[str, float]] = None  # For numeric fields

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'field_name': self.field_name,
            'total_values': self.total_values,
            'non_empty_count': self.non_empty_count,
            'unique_count': self.unique_count,
            'completeness': self.completeness,
            'value_distribution': self.value_distribution
        }
        if self.numeric_stats:
            result['numeric_stats'] = self.numeric_stats
        return result


class DataQualityAnalyzer:
    """Analyzes data quality metrics for fields."""

    def analyze_field(self, field_name: str, values: List[Any]) -> FieldMetrics:
        """
        Analyze a single field's data quality.

        Args:
            field_name: Name of the field
            values: List of values

        Returns:
            FieldMetrics
        """
        total_values = len(values)
        non_empty_values = [v for v in values if v is not None and str(v).strip() != '']
        non_empty_count = len(non_empty_values)
        unique_values = set(str(v) for v in non_empty_values)
        unique_count = len(unique_values)
        completeness = (non_empty_count / total_values * 100) if total_values > 0 else 0

        # Value distribution (top 10)
        value_counts: Dict[str, int] = {}
        for v in non_empty_values:
            str_v = str(v)
            value_counts[str_v] = value_counts.get(str_v, 0) + 1

        # Get top 10 most common values
        top_values = dict(sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:10])

        # Numeric statistics (if applicable)
        numeric_stats = None
        numeric_values = []
        for v in non_empty_values:
            try:
                numeric_values.append(float(v))
            except (ValueError, TypeError):
                # Non-numeric values are expected and should be skipped when collecting numeric statistics
                pass

        if len(numeric_values) > 0 and len(numeric_values) / len(non_empty_values) > 0.5:
            # Field is mostly numeric
            numeric_stats = {
                'min': min(numeric_values),
                'max': max(numeric_values),
                'mean': statistics.mean(numeric_values),
                'median': statistics.median(numeric_values)
            }
            if len(numeric_values) > 1:
                numeric_stats['stdev'] = statistics.stdev(numeric_values)

        return FieldMetrics(
            field_name=field_name,
            total_values=total_values,
            non_empty_count=non_empty_count,
            unique_count=unique_count,
            completeness=completeness,
            value_distribution=top_values,
            numeric_stats=numeric_stats
        )

    def detect_outliers(self, values: List[float], threshold: float = 3.0) -> List[int]:
        """
        Detect outliers using z-score method.

        Args:
            values: List of numeric values
            threshold: Z-score threshold (default: 3.0)

        Returns:
            List of indices that are outliers
        """
        if len(values) < 3:
            return []

        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0

        if stdev == 0:
            return []

        outliers = []
        for i, v in enumerate(values):
            z_score = abs((v - mean) / stdev)
            if z_score > threshold:
                outliers.append(i)

        return outliers


def build_fk_index_from_tsvs(tsv_dir: Path) -> Dict[str, Set[str]]:
    """
    Build FK index by reading all TSV files and extracting entity IDs.

    Args:
        tsv_dir: Directory containing TSV files

    Returns:
        Dictionary mapping entity type to set of IDs
    """
    import csv

    fk_index: Dict[str, Set[str]] = {}

    for tsv_file in tsv_dir.glob('*.tsv'):
        # Entity type is filename without extension
        entity_type = tsv_file.stem

        if entity_type == 'ENIGMA':
            continue  # Skip root entity

        try:
            with open(tsv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                ids = set()
                for row in reader:
                    # Get ID field (first column is usually 'id')
                    if 'id' in row and row['id']:
                        ids.add(row['id'])
                    # Also get 'name' field for FKs that reference by name
                    if 'name' in row and row['name']:
                        ids.add(row['name'])

                fk_index[entity_type] = ids
                print(f"  Loaded {len(ids)} IDs for {entity_type}")

        except Exception as e:
            print(f"  Warning: Could not load {tsv_file}: {e}")

    return fk_index
