---
sidebar_position: 2
title: "Exceptions Reference"
description: "Complete reference of all MZpack exception classes — strategy, decision tree, and data export errors."
---

# Exceptions Reference

All exception classes in the MZpack API. Every MZpack exception inherits from `StrategyException`, which extends the standard `System.Exception`.

## Hierarchy

```
Exception
 └── StrategyException (abstract)
      ├── StrategyPrepareException
      ├── DecisionTreeException (abstract)
      │    ├── DecisionTreeInvalidStructureException
      │    ├── DecisionTreeSignalChartRangeIsNullException
      │    └── DecisionTreeSignalChartRangeIsInvalidException
      └── ExportException (abstract)
           ├── DataExportDuplicatedIndValueException
           ├── DataExportColumnNotFoundException
           ├── DataExportNoHandlerForIndValueException
           ├── DataExportNoChartObjectDescriptorException
           ├── DataExportNoHandlerForCustomValueException
           ├── DataExportEmptyPipelineException
           └── DataExportGranularityException

Exception
 └── DataExportNullArgumentsException
```

## Strategy Exceptions

**Namespace:** `MZpack.NT8.Algo`

| Class | Base | When Thrown |
|---|---|---|
| `StrategyException` | `Exception` | Abstract base for all MZpack strategy exceptions |
| `StrategyPrepareException` | `StrategyException` | Strategy preparation fails (e.g., missing indicators, invalid configuration) |

`StrategyPrepareException` message format: `"Strategy prepare error. {details}"`

## Decision Tree Exceptions

**Namespace:** `MZpack.NT8.Algo`

| Class | Base | When Thrown |
|---|---|---|
| `DecisionTreeException` | `StrategyException` | Abstract base for decision tree validation errors |
| `DecisionTreeInvalidStructureException` | `DecisionTreeException` | Decision tree has structural issues (e.g., empty root, invalid node arrangement) |
| `DecisionTreeSignalChartRangeIsNullException` | `DecisionTreeException` | Signal's `ChartRange` was not assigned in `OnCalculate()` while using tree range validation |
| `DecisionTreeSignalChartRangeIsInvalidException` | `DecisionTreeException` | Signal's `ChartRange` is invalid (e.g., out of bounds) while using tree range validation |

Message formats:
- `"Invalid structure of the decision tree. {details}"`
- `"Chart range of validated signal/filter is null. {details}"`
- `"Chart range of validated signal/filter is invalid. {details}"`

## Export Exceptions

**Namespace:** `MZpack.NT8.Algo.DataExport`

| Class | Base | When Thrown |
|---|---|---|
| `ExportException` | `StrategyException` | Abstract base for data export errors |
| `DataExportNullArgumentsException` | `StrategyException` | `ExportArgs` is `null` |
| `DataExportDuplicatedIndValueException` | `ExportException` | Same `IndValue` added to schema twice |
| `DataExportColumnNotFoundException` | `ExportException` | Referenced column name not found in schema |
| `DataExportNoHandlerForIndValueException` | `ExportException` | No handler registered for the specified `IndValue` in the indicator |
| `DataExportNoChartObjectDescriptorException` | `ExportException` | `ValueDescriptor` with `DrawingObject` source has no `ChartObjectDescriptor` |
| `DataExportNoHandlerForCustomValueException` | `ExportException` | `ValueDescriptor` with `Calculate` source has no delegate assigned |
| `DataExportEmptyPipelineException` | `ExportException` | `Pipeline.Init()` called with no exports added |
| `DataExportGranularityException` | `ExportException` | Unsupported `ExportGranularity` for the data source |

Message formats:
- `"Null export arguments"`
- `"Duplicated indicator value '{indValue}'"`
- `"Colum not found '{column}'"` (typo preserved from source)
- `"No handler for indicator value '{indValue}'"`
- `"No descriptor for chart object defined"`
- `"No handler for custom value '{name}'"`
- `"Data export pipeline is empty"`
- `"Granularity {granularity} not supported for the export."`
