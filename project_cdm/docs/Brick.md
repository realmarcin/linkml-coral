
# Class: Brick

Abstract base for all brick data tables (ddt_brick*).

Each brick table stores measurement values in a denormalized format
where each row represents one cell in the N-dimensional array.

Common structure:
- Dimension indices (dim0_index, dim1_index, dim2_index, ...)
- Dimension values (dim0_value, dim1_value, dim2_value, ...)
- Variable values (var0_value, var1_value, var2_value, ...)

Schema is defined in sys_ddt_typedef and varies per brick.

Note: Individual brick classes (Brick0000001, Brick0000002, etc.)
are not explicitly defined in this schema because they have
heterogeneous structures. They should be validated against
sys_ddt_typedef at runtime.

URI: [kbase_cdm:Brick](https://w3id.org/enigma/kbase-cdm/Brick)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Brick])](https://yuml.me/diagram/nofunky;dir:TB/class/[Brick])

## Attributes


## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | Brick tables are created dynamically based on measurement needs |
|  | | Each brick can have different dimensions and variables |
|  | | Schema flexibility enables diverse experimental data types |
