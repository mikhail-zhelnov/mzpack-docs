---
sidebar_position: 3
title: "Series & Synchronized Collections"
description: "Reference for Series<T>, SynchronizedList<T>, and SynchronizedDictionary<TKey, TValue> collection types in MZpack."
---

# Series & Synchronized Collections

Thread-safe and time-series collection types used throughout MZpack indicators.

**Namespace:** `MZpack`

## Series&lt;T&gt;

**Inheritance:** `Series<T> : Dictionary<int, T>`

A dictionary keyed by bar index with "ago"-based relative access. Used for time-series data where you need to look back N bars from the current position.

### Methods

| Method | Returns | Description |
|---|---|---|
| `GetAgo(int ago)` | `T` | Get value `ago` positions back from the latest entry (0 = latest, 1 = previous) |
| `SetAgo(int ago, T value)` | `void` | Set value `ago` positions back from the latest entry |
| `Add(int key, T value)` | `void` | Add entry (tracks the maximum key internally) |

### Indexer

```csharp
series[barIndex] = value;   // set by absolute bar index
var val = series[barIndex]; // get by absolute bar index
```

### Usage

```csharp
// Access the latest delta value
double currentDelta = deltaSeries.GetAgo(0);

// Access the previous bar's delta
double prevDelta = deltaSeries.GetAgo(1);
```

## SynchronizedList&lt;T&gt;

**Inheritance:** `SynchronizedList<T> : List<T>`

Thread-safe list wrapper using monitor-based locking. All standard `List<T>` operations are available — use `Lock()` / `Unlock()` to protect multi-step access.

### Constructor

```csharp
new SynchronizedList<T>(IIndicator indicator)
```

### Methods

| Method | Description |
|---|---|
| `Lock()` | Acquire exclusive lock (Monitor.Enter) |
| `Unlock()` | Release lock (Monitor.Exit) |

### Usage

```csharp
bigTrades.Lock();
try
{
    foreach (var trade in bigTrades)
    {
        // safe iteration
    }
}
finally
{
    bigTrades.Unlock();
}
```

:::warning
Always pair `Lock()` with `Unlock()` in a try/finally block to prevent deadlocks. Accessing items without locking may cause `InvalidOperationException` if the collection is modified concurrently by the indicator.
:::

## SynchronizedDictionary&lt;TKey, TValue&gt;

**Inheritance:** `SynchronizedDictionary<TKey, TValue> : Dictionary<TKey, TValue>`

Thread-safe dictionary wrapper using the same locking pattern as `SynchronizedList<T>`.

### Constructor

```csharp
new SynchronizedDictionary<TKey, TValue>(IIndicator indicator)
```

### Methods

| Method | Description |
|---|---|
| `Lock()` | Acquire exclusive lock (Monitor.Enter) |
| `Unlock()` | Release lock (Monitor.Exit) |

### Usage

```csharp
footprintBars.Lock();
try
{
    if (footprintBars.TryGetValue(barIndex, out var bar))
    {
        // access footprint bar data
    }
}
finally
{
    footprintBars.Unlock();
}
```
