---
sidebar_position: 3
title: "Delegates Reference"
description: "Complete reference of all public delegate types in the MZpack API."
---

# Delegates Reference

All public delegate types in the MZpack API.

## Strategy Lifecycle

**Namespace:** `MZpack.NT8.Algo`

### OnCreateAlgoStrategyDelegate

```csharp
public delegate Algo.Strategy OnCreateAlgoStrategyDelegate();
```

Factory delegate for creating an `Algo.Strategy` instance. Assigned to `MZpackStrategyBase.OnCreateAlgoStrategy`.

### OnCreateIndicatorsDelegate

```csharp
public delegate List<TickIndicator> OnCreateIndicatorsDelegate();
```

Factory delegate for creating the list of indicators used by the strategy. Assigned to `MZpackStrategyBase.OnCreateIndicators`.

## Market Data Handlers

**Namespace:** `MZpack.NT8.Algo`

### OnTickDelegate

```csharp
public delegate void OnTickDelegate(MarketDataEventArgs e, int currentBarIdx);
```

Handler for Level 1 market data events. Assigned to `MZpackStrategyBase.OnEachTickHandler` and `MZpackStrategyBase.OnBarCloseHandler`.

| Parameter | Type | Description |
|---|---|---|
| `e` | `MarketDataEventArgs` | NinjaTrader market data event |
| `currentBarIdx` | `int` | Current bar index |

### OnMarketDepthDelegate

```csharp
public delegate void OnMarketDepthDelegate(MarketDepthEventArgs e, int currentBarIdx);
```

Handler for Level 2 (DOM) market data events. Assigned to `MZpackStrategyBase.OnMarketDepthHandler`.

| Parameter | Type | Description |
|---|---|---|
| `e` | `MarketDepthEventArgs` | NinjaTrader market depth event |
| `currentBarIdx` | `int` | Current bar index |

## Pattern & Trail

**Namespace:** `MZpack.NT8.Algo`

### PatternHandler

```csharp
public delegate void PatternHandler(Pattern sender, DateTime time);
```

Callback invoked when a pattern is validated or not validated. Used for `Pattern.OnValidated` and `Pattern.OnNotValidated` events.

| Parameter | Type | Description |
|---|---|---|
| `sender` | `Pattern` | Pattern that was evaluated |
| `time` | `DateTime` | Time of evaluation |

### TrailEvent

```csharp
public delegate bool TrailEvent(TrailBase sender, DateTime time);
```

Callback for trailing logic evaluation. Returns `true` to trigger the trail action.

| Parameter | Type | Description |
|---|---|---|
| `sender` | `TrailBase` | Trail instance |
| `time` | `DateTime` | Current time |

## Order Flow Events

**Namespace:** `MZpack`

### OrderflowEventHandler

```csharp
public delegate void OrderflowEventHandler(OrderflowEventArguments e);
```

Handler for aggregated order flow events.

| Parameter | Type | Description |
|---|---|---|
| `e` | `OrderflowEventArguments` | Order flow event with price, volume, side, and time |

## Data Export

**Namespace:** `MZpack.NT8.Algo.DataExport`

### GetExportValueDelegate

```csharp
public delegate double GetExportValueDelegate(
    GeneralExport export, ValueDescriptor desc, object data);
```

Retrieves a single `double` value from indicator data. Set automatically by `ExportedIndicator.SetExportValueHandler()` when the `ValueDescriptor.Source` is `Indicator`.

### GetExportValuesDelegate

```csharp
public delegate List<double> GetExportValuesDelegate(
    GeneralExport export, ValueDescriptor desc, object data);
```

Retrieves multiple `double` values from indicator data (for multi-value `IndValue` types like `Volumes`, `Bids`, `Asks`).

### CalculateExportValueDelegate

```csharp
public delegate double CalculateExportValueDelegate(
    GeneralExport export, ValueDescriptor desc, object data);
```

User-provided delegate for computing a single calculated value. Used when `ValueDescriptor.Source` is `Calculate`.

### CalculateExportValuesDelegate

```csharp
public delegate List<double> CalculateExportValuesDelegate(
    GeneralExport export, ValueDescriptor desc, object data);
```

User-provided delegate for computing multiple calculated values.

### Common Parameters

All export delegates share the same parameter pattern:

| Parameter | Type | Description |
|---|---|---|
| `export` | `GeneralExport` | Parent export instance (access `DataSet`, `ExportArgs`) |
| `desc` | `ValueDescriptor` | Column descriptor being evaluated |
| `data` | `object` | Current data item (bar, tick, or drawing object) |
