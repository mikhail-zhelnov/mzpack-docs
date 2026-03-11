---
sidebar_position: 2
title: "DataSchema / DataSet"
description: "Reference for DataSchema, DataSet, DataSetRow, and DataSetRowValues classes that define and hold exported data."
---

# DataSchema / DataSet

Classes that define the structure of exported data and hold the exported rows.

**Namespace:** `MZpack.NT8.Algo`

## DataSchema

Defines the column structure of an export — an ordered list of [ValueDescriptor](value-descriptor.md) instances.

### Properties

| Property | Type | Description |
|---|---|---|
| `Descriptors` | `List<ValueDescriptor>` | Ordered list of column descriptors |
| `DataSet` | `DataSet` | Associated DataSet (set during `Init`) |

### Adding Columns

`DataSchema` uses a fluent API — all `Append` methods return `this`.

**By indicator value:**

```csharp
schema
    .Append(IndValue.POC)
    .Append(IndValue.Delta)
    .Append(IndValue.Volume);
```

**With custom name and kind:**

```csharp
schema.Append("my_poc", ValueKind.Feature, IndValue.POC);
```

**With calculated value:**

```csharp
schema.Append("spread", ValueKind.Feature,
    (export, desc, data) => strategy.GetCurrentAsk() - strategy.GetCurrentBid());
```

**With multiple indicator values:**

```csharp
schema.Append("levels", ValueKind.Feature,
    new[] { IndValue.VAH, IndValue.VAL, IndValue.POC });
```

**With drawing object mapping:**

```csharp
schema.Append("signal", ValueKind.Label, chartObjectDescriptor);
```

### Key Methods

| Method | Returns | Description |
|---|---|---|
| `Append(IndValue)` | `DataSchema` | Add column for built-in indicator value |
| `Append(string, ValueKind, IndValue, int)` | `DataSchema` | Add named column with kind and optional shift |
| `Append(string, ValueKind, CalculateExportValueDelegate)` | `DataSchema` | Add calculated single-value column |
| `Append(string, ValueKind, CalculateExportValuesDelegate)` | `DataSchema` | Add calculated multi-value column |
| `Append(string, ValueKind, ChartObjectDescriptor)` | `DataSchema` | Add drawing object column |
| `GetColumnByName(string)` | `int` | Column index by name (−1 if not found) |
| `GetColumnByIndValue(IndValue)` | `int` | Column index by IndValue (−1 if not found) |
| `GetFeatures()` | `string[]` | Names of all Feature columns |
| `GetLabels()` | `string[]` | Names of all Label columns |
| `GetOfKind(ValueKind)` | `List<ValueDescriptor>` | All descriptors of a given kind |
| `Drop(string, ValueKind)` | `void` | Remove descriptor by name and kind |
| `Clone()` | `DataSchema` | Deep copy of schema and all descriptors |
| `SaveToXml(string)` | `void` | Serialize schema to XML file |
| `LoadFromXml(MZpackStrategyBase, string)` | `DataSchema` | Deserialize schema from XML file (static) |

## DataSet

Container for exported data rows, organized by a `DataSchema`.

### Properties

| Property | Type | Description |
|---|---|---|
| `Schema` | `DataSchema` | Column definitions (setting clears all rows) |
| `Rows` | `List<DataSetRow>` | All data rows |
| `Cursor` | `int` | Index of the last added row |
| `Export` | `GeneralExport` | Parent export instance |

### Methods

| Method | Returns | Description |
|---|---|---|
| `AddRow(DateTime)` | `DataSetRow` | Create a new row with timestamp |
| `GetValue(int, int)` | `double` | Get value by column and shift from cursor |
| `GetValue(IndValue, int)` | `double` | Get value by IndValue and shift |
| `GetValue(string, int)` | `double` | Get value by column name and shift |
| `SetValue(double, int, int)` | `void` | Set value by column and shift |
| `GetLabel(int, int)` | `double` | Get label by column and shift |
| `SetLabel(double, int, int)` | `void` | Set label by column and shift |
| `Skip(int)` | `void` | Remove first N rows |
| `Append(DataSet)` | `void` | Append rows from another DataSet (schemas must match) |
| `ToEnumerable(ValueKind)` | `List<List<double>>` | All rows as nested lists, filtered by kind |
| `ToLines(ExportArgs, int)` | `List<string>` | Convert rows to CSV strings |
| `LastRowToString(ExportArgs)` | `string` | Last row as CSV string |

## DataSetRow

A single row of exported data with a timestamp.

### Properties

| Property | Type | Description |
|---|---|---|
| `Time` | `DateTime` | Row timestamp |
| `Values` | `DataSetRowValues` | Feature and Internal values |
| `Labels` | `DataSetRowValues` | Label values |

### Methods

| Method | Returns | Description |
|---|---|---|
| `ToString(ExportArgs)` | `string` | Row as a delimited string |

## DataSetRowValues

**Inheritance:** `DataSetRowValues : List<double>`

A list of `double` values for one row. Extends `List<double>` with no additional public API.

## Index

Simple wrapper for an integer value, used internally for position tracking.

| Property | Type | Description |
|---|---|---|
| `Value` | `int` | Index value |

## Example

```csharp
// Define schema with POC and Delta columns
var args = new ExportArgs { FileName = "output.csv", IsHeader = true, IsTime = true };
var export = new IndicatorExport(strategy, fpIndicator,
    ExportDataSource.Level1, ExportTemporality.Historical,
    ExportGranularity.Bar, args);

export.DataSet.Schema
    .Append(IndValue.POC)
    .Append(IndValue.Delta);

// After export, access data:
double poc = export.DataSet.GetValue(IndValue.POC);
double prevDelta = export.DataSet.GetValue(IndValue.Delta, shift: 1);
```
