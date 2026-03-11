---
sidebar_position: 3
title: "ValueDescriptor"
description: "Reference for ValueDescriptor, IndValue enum, value delegates, and related types for defining export columns."
---

# ValueDescriptor

Describes a single column in the export schema — its name, data source, kind, and how to retrieve the value.

**Namespace:** `MZpack.NT8.Algo`

## Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Name` | `string` | — | Column name (used in CSV header) |
| `IndValue` | `IndValue` | `None` | Built-in indicator value type |
| `Index` | `int` | — | Sub-index for multi-value descriptors (e.g., order book level) |
| `Kind` | `ValueKind` | `Feature` | Column kind: Feature, Label, or Internal |
| `IsMany` | `bool` | — | `true` if the descriptor produces multiple values per bar |
| `Source` | `ValueSorce` | `Indicator` | How the value is obtained |
| `SourceName` | `string` | — | For `DataSet` source: name of the column to reference |
| `SourceColumn` | `int` | −1 | For `DataSet` source: resolved column index |
| `Column` | `int` | — | Position in the schema's descriptor list |
| `Shift` | `int` | `0` | Historical shift (0 = current bar) |
| `ChartObjectDescriptor` | `ChartObjectDescriptor` | — | For `DrawingObject` source: mapping descriptor |

### Delegate Properties

| Property | Type | Description |
|---|---|---|
| `GetValue` | `GetExportValueDelegate` | Retrieve a single value from indicator data |
| `GetValues` | `GetExportValuesDelegate` | Retrieve multiple values from indicator data |
| `CalculateValue` | `CalculateExportValueDelegate` | Calculate a single value from custom logic |
| `CalculateValues` | `CalculateExportValuesDelegate` | Calculate multiple values from custom logic |

## Delegates

### Single-Value Delegates

```csharp
public delegate double GetExportValueDelegate(
    GeneralExport export, ValueDescriptor desc, object data);

public delegate double CalculateExportValueDelegate(
    GeneralExport export, ValueDescriptor desc, object data);
```

### Multi-Value Delegates

```csharp
public delegate List<double> GetExportValuesDelegate(
    GeneralExport export, ValueDescriptor desc, object data);

public delegate List<double> CalculateExportValuesDelegate(
    GeneralExport export, ValueDescriptor desc, object data);
```

`GetExportValueDelegate` / `GetExportValuesDelegate` are set automatically by `ExportedIndicator.SetExportValueHandler()` when the source is `Indicator`. `CalculateExportValueDelegate` / `CalculateExportValuesDelegate` are user-provided when the source is `Calculate`.

## ValueKind Enum

| Value | Description |
|---|---|
| `Feature` | Input/feature column (exported before labels in CSV) |
| `Label` | Label/target column (exported after features in CSV) |
| `Internal` | Internal column (not exported, used for intermediate calculations) |

## ValueSorce Enum

:::note
The enum name contains a typo (`ValueSorce` instead of `ValueSource`) in the source code.
:::

| Value | Description |
|---|---|
| `Indicator` | Value retrieved from an indicator via `GetValue`/`GetValues` delegates |
| `DrawingObject` | Value mapped from a chart drawing object via `ChartObjectDescriptor` |
| `Calculate` | Value computed by a user-provided `CalculateValue`/`CalculateValues` delegate |
| `DataSet` | Value referenced from another column in the same DataSet |

## IndValue Enum

Built-in indicator value identifiers. Used to specify which indicator metric to export.

### Bar Values

| Value | Description |
|---|---|
| `Open` | Bar open price |
| `Close` | Bar close price |
| `High` | Bar high price |
| `Low` | Bar low price |
| `RangeTicks` | Bar range in ticks |
| `RangeLevels` | Number of price levels in bar |
| `Side` | Bar side (buy/sell) |
| `DurationMs` | Bar duration in milliseconds |

### Order Flow — Single Values

| Value | Description |
|---|---|
| `Volume` | Total bar volume |
| `BuyVolume` | Buy (ask) volume |
| `SellVolume` | Sell (bid) volume |
| `Delta` | Delta (BuyVolume − SellVolume) |
| `DeltaPercentage` | Delta as percentage of volume |
| `DeltaChange` | Delta change from prior bar |
| `DeltaCumulative` | Cumulative delta |
| `DeltaRate` | Delta rate |
| `DeltaRateHigh` | Delta rate high |
| `DeltaRateLow` | Delta rate low |
| `MinDelta` | Minimum delta in bar |
| `MaxDelta` | Maximum delta in bar |
| `AbsoluteDeltaAverage` | Average absolute delta |
| `AbsoluteDeltaTotal` | Total absolute delta |
| `BuyPercentage` | Buy percentage |
| `SellPercentage` | Sell percentage |
| `TradesNumber` | Number of trades |
| `VolumePerSecond` | Volume per second |
| `RatioNumbers` | Ratio numbers |

### Order Flow — Multi-Value (per price level)

| Value | Description |
|---|---|
| `Volumes` | Volume at each price level |
| `Bids` | Bid volume at each level |
| `Asks` | Ask volume at each level |
| `Deltas` | Delta at each level |
| `TradesNumbers` | Trade count at each level |
| `Ticks` | Tick data at each level |

### Profile & Session

| Value | Description |
|---|---|
| `POC` | Point of Control price |
| `POCVolume` | Volume at POC |
| `VAH` | Value Area High |
| `VAL` | Value Area Low |
| `VWAP` | Volume Weighted Average Price |
| `_1StdDeviationPos` | +1 standard deviation |
| `_1StdDeviationNeg` | −1 standard deviation |
| `_2StdDeviationPos` | +2 standard deviation |
| `_2StdDeviationNeg` | −2 standard deviation |
| `IBHigh` | Initial Balance High |
| `IBLow` | Initial Balance Low |
| `MID` | Mid price |
| `TPO_POC` | TPO Point of Control |
| `TPO_VAH` | TPO Value Area High |
| `TPO_VAL` | TPO Value Area Low |
| `TPOLettersCount` | TPO letter count |
| `BuyPOCVolume` | Buy POC volume |
| `SellPOCVolume` | Sell POC volume |
| `TickPOC` | Tick POC |
| `TickPOCVolume` | Tick POC volume |
| `VAVolume` | Value Area volume |
| `SessionOpen` | Session open price |
| `SessionClose` | Session close price |
| `SessionHigh` | Session high |
| `SessionLow` | Session low |
| `SessionVAH` | Session Value Area High |
| `SessionVAL` | Session Value Area Low |
| `SessionPOC` | Session POC |

### Imbalance & Absorption

| Value | Description |
|---|---|
| `BuyImbalanceCount` | Buy imbalance count |
| `SellImbalanceCount` | Sell imbalance count |
| `BuyAbsorptionCount` | Buy absorption count |
| `SellAbsorptionCount` | Sell absorption count |
| `BuyStackedImbalanceCount` | Stacked buy imbalance count |
| `SellStackedImbalanceCount` | Stacked sell imbalance count |
| `BuyStackedAbsorptionCount` | Stacked buy absorption count |
| `SellStackedAbsorptionCount` | Stacked sell absorption count |
| `BuyStackedImbalanceMaxConsec` | Max consecutive buy stacked imbalances |
| `SellStackedImbalanceMaxConsec` | Max consecutive sell stacked imbalances |
| `BuyStackedAbsorptionMaxConsec` | Max consecutive buy stacked absorptions |
| `SellStackedAbsorptionMaxConsec` | Max consecutive sell stacked absorptions |
| `UnfinishedAuctionHigh` | Unfinished auction at high |
| `UnfinishedAuctionLow` | Unfinished auction at low |
| `COTHigh` | COT high |
| `COTLow` | COT low |

### Big Trade

| Value | Description |
|---|---|
| `IcebergVolume` | Iceberg volume |
| `TicksNumber` | Number of ticks |
| `DomPressureVolume` | DOM pressure volume |
| `DomSupportVolume` | DOM support volume |
| `Smart` | Smart order flag |

### Market Depth

| Value | Description |
|---|---|
| `MarketDepth` | Market depth snapshot |
| `RealMarketDepth` | Real market depth |
| `RealtimeBid` | Real-time best bid volume |
| `RealtimeOffer` | Real-time best offer volume |
| `RealtimeBidPrice` | Real-time best bid price |
| `RealtimeOfferPrice` | Real-time best offer price |
| `RealtimeBids` | Real-time bid levels (multi-value) |
| `RealtimeOffers` | Real-time offer levels (multi-value) |
| `RealtimeBidsWithPrices` | Bid levels with prices (multi-value) |
| `RealtimeOffersWithPrices` | Offer levels with prices (multi-value) |
| `RealtimeOffersTotal` | Total offer volume |
| `RealtimeBidsTotal` | Total bid volume |
| `BestBid` | Best bid |
| `BestOffer` | Best offer |

### Divergence & Other

| Value | Description |
|---|---|
| `DeltaDivergence` | Delta divergence value |
| `HQA` | HQA value |
| `UQ` | UQ value |
| `AC` | AC value |
| `UpdatesNumber` | Number of updates |

### Liquidity

| Value | Description |
|---|---|
| `LiquidityOpen` | Liquidity open |
| `LiquidityClose` | Liquidity close |
| `LiquidityHigh` | Liquidity high |
| `LiquidityLow` | Liquidity low |
| `LiquidityMigrationOpen` | Liquidity migration open |
| `LiquidityMigrationClose` | Liquidity migration close |
| `LiquidityMigrationHigh` | Liquidity migration high |
| `LiquidityMigrationLow` | Liquidity migration low |
