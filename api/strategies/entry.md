---
sidebar_position: 10
title: "Entry"
description: "Reference for Entry, BarStopLossEntry, SignalStopLossEntry, and FiboRetracementEntry — order submission and protective orders."
---

# Entry

`Entry` handles order submission and protective orders (stop loss, profit target, breakeven) within a pattern. Several specialized subclasses provide alternative stop loss and entry price calculations.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `Entry : EntryBase`
**Source:** `MZpack.NT8/Algo/Extensions/Entries/Entry.cs`

## EntryBase

Abstract base class for all entry types.

| Property | Type | Description |
|---|---|---|
| `SignalName` | `string` | Unique name of the entry |
| `TypeName` | `string` | Read-only, returns the class name |
| `Trail` | `TrailBase` | Trailing stop attached to this entry |
| `Exit` | `ExitBase` | Exit condition attached to this entry |

Abstract methods: `GetStopLossValue()`, `GetProfitTargetValue()`.

## Entry Properties

### Order Configuration

| Property | Type | Default | Description |
|---|---|---|---|
| `Quantity` | `int` | `1` | Number of contracts |
| `EntryMethod` | `EntryMethod` | `Market` | Order type: Market, Limit, or StopLimit |
| `LimitEntryShiftTicks` | `int` | `0` | Tick offset for limit entry price |
| `LimitEntryPriceChase` | `bool` | `false` | Move pending limit order tick by tick |
| `CancelLimitOrderType` | `CancelLimitOrderType` | `Bars` | When to cancel a pending limit order |
| `CancelLimitOrderValue` | `double` | `1` | Value for `CancelLimitOrderType` |

### Stop Loss

| Property | Type | Default | Description |
|---|---|---|---|
| `StopLossCalculationMode` | `CalculationMode` | `Ticks` | Ticks or Price |
| `StopLossTicks` | `int` | `6` | Stop loss distance in ticks |
| `StopLossPrice` | `double` | — | Stop loss price (when mode is Price) |

### Profit Target

| Property | Type | Default | Description |
|---|---|---|---|
| `ProfitTargetCalculationMode` | `CalculationMode` | `Ticks` | Ticks or Price |
| `ProfitTargetTicks` | `int` | `12` | Profit target distance in ticks |
| `ProfitTargetPrice` | `double` | — | Profit target price (when mode is Price) |

### Breakeven

| Property | Type | Default | Description |
|---|---|---|---|
| `IsBreakEven` | `bool` | `false` | Enable breakeven stop |
| `BreakEvenAfterCalculationMode` | `CalculationMode` | `Ticks` | Ticks or Price |
| `BreakEvenAfterTicks` | `int` | `8` | Ticks of profit before breakeven activates |
| `BreakEvenAfterPrice` | `double` | — | Price for breakeven activation |
| `BreakEvenShiftTicks` | `int` | `0` | Ticks added to breakeven stop (positive = extra profit) |

### Read-Only State

| Property | Type | Description |
|---|---|---|
| `Filled` | `int` | Filled quantity |
| `AverageEntryPrice` | `double` | Average fill price |
| `IsInBreakEven` | `bool` | True if breakeven stop is active |
| `BreakEvenPrice` | `double` | Current breakeven stop price |
| `HasPendingLimitOrder` | `bool` | True if a limit order is pending |
| `FilledBarIdx` | `int` | Bar index when order was filled |
| `IsStopLossTriggered` | `bool` | True if stop loss was hit |
| `IsProfitTargetTriggered` | `bool` | True if profit target was hit |

## Entry Methods

| Method | Description |
|---|---|
| `Initialize(Strategy strategy, Position position)` | Bind to strategy and position |
| `Reset()` | Reset fill state, breakeven, and triggers |
| `SubmitStopLoss(DateTime time, int quantity, double value, CalculationMode mode)` | Submit initial stop loss |
| `ChangeStopLoss(DateTime time, int quantity, double value, CalculationMode mode)` | Modify existing stop loss |
| `SubmitProfitTarget(DateTime time, int quantity, double value, CalculationMode mode)` | Submit profit target |
| `GetEntryPrice(double entry)` | Override to calculate custom entry price |
| `GetPnL()` | Returns unrealized PnL |

---

## BarStopLossEntry

Sets the stop loss from the high or low of a bar N bars ago.

**Inheritance:** `BarStopLossEntry : Entry`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `StopLossBarsAgo` | `int` | `1` | Bars ago for stop loss reference bar |
| `StopLossShiftTicks` | `int` | `1` | Tick shift from bar high/low |

### Stop Loss Calculation

- **Long:** `Min(CurrentBid - spread, Low[BarsAgo] - ShiftTicks)`
- **Short:** `Max(CurrentAsk + spread, High[BarsAgo] + ShiftTicks)`

Sets `StopLossCalculationMode = Price` automatically.

---

## SignalStopLossEntry

Uses the signal-calculated `StopLossPrice` property to set the stop loss.

**Inheritance:** `SignalStopLossEntry : Entry`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `StopLossShiftTicks` | `int` | `1` | Tick shift from signal stop loss price |

### Stop Loss Calculation

- **Long:** `Min(CurrentBid - spread, StopLossPrice - ShiftTicks)`
- **Short:** `Max(CurrentAsk + spread, StopLossPrice + ShiftTicks)`

Sets `StopLossCalculationMode = Price` automatically.

---

## FiboRetracementEntry

Places a limit entry at a Fibonacci retracement level between swing high and swing low.

**Inheritance:** `FiboRetracementEntry : Entry`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Fibo` | `double` | `50.0` | Fibonacci retracement percentage |
| `SwingHigh` | `double` | — | Swing high price |
| `SwingLow` | `double` | — | Swing low price |

### Entry Price Calculation

Retracement = `(SwingHigh - SwingLow) * Fibo / 100`

- **Long:** `SwingHigh - retracement` (must be \< CurrentAsk)
- **Short:** `SwingLow + retracement` (must be \> CurrentBid)

Returns 0 if the price constraint is violated. Sets `EntryMethod = Limit` automatically.

---

## Enums

### EntryMethod

| Value | Description |
|---|---|
| `Market` | Market order |
| `Limit` | Limit order |
| `StopLimit` | Stop-limit order |

### CancelLimitOrderType

| Value | Description |
|---|---|
| `None` | Never cancel |
| `Ticks` | Cancel after N ticks move |
| `Bars` | Cancel after N bars |
| `Milliseconds` | Cancel after N milliseconds |

### CalculationMode

| Value | Description |
|---|---|
| `Ticks` | Value in ticks |
| `Price` | Absolute price |

## See Also

- [Pipeline](pipeline.md) — execution order of components
- [Position](position.md) — position management
- [Exit](exit.md) — exit conditions
- [Trail](trail.md) — trailing stop management
