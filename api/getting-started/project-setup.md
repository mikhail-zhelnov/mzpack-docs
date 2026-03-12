---
sidebar_position: 3
title: "Project Setup"
description: "How to set up a Visual Studio 2022 project to develop custom MZpack indicators and strategies for NinjaTrader 8."
---

# Project Setup

This page covers two workflows: using the **NinjaTrader built-in editor** (quickest) and setting up a **Visual Studio 2022 project** (recommended for multi-file projects).

## Option 1: NinjaTrader Built-in Editor

The fastest way to start:

1. In NinjaTrader, go to **New → NinjaScript Editor**
2. Right-click in the editor and select **New → Strategy**
3. Enter a name (e.g., `MyMZpackStrategy`) and click **Generate**
4. Replace the generated base class with `MZpackStrategyBase`:

```csharp
using MZpack;
using MZpack.NT8;
using MZpack.NT8.Algo;
using MZpack.NT8.Algo.Indicators;

namespace NinjaTrader.NinjaScript.Strategies
{
    public class MyMZpackStrategy : MZpackStrategyBase
    {
        // ...
    }
}
```

5. Press **F5** to compile

The built-in editor automatically resolves MZpack references from the `Documents\NinjaTrader 8\bin\Custom\` directory.

## Option 2: Visual Studio 2022

### Create the Project

1. Open Visual Studio 2022
2. **File → New → Project** → select **Class Library (.NET Framework)**
3. Set framework to **.NET Framework 4.8**
4. Set platform to **x64**
5. Name the project (e.g., `MyMZpackStrategies`)

### Add Assembly References

Right-click **References → Add Reference → Browse** and add the following DLLs:

**From `Documents\NinjaTrader 8\bin\Custom\`:**

| Assembly | Provides |
|---|---|
| `MZpack.NT8.dll` | MZpack API — all `MZpack.*` namespaces |

**From NinjaTrader installation directory** (typically `C:\Program Files\NinjaTrader 8\bin\`):

| Assembly | Provides |
|---|---|
| `NinjaTrader.Core.dll` | Core NinjaTrader types |
| `NinjaTrader.Gui.dll` | UI types (`Stroke`, `Brushes`) |
| `NinjaTrader.Vendor.dll` | Vendor integration |

**From NinjaTrader installation directory** (for Direct2D rendering in custom indicators):

| Assembly | Provides |
|---|---|
| `SharpDX.dll` | SharpDX core |
| `SharpDX.Direct2D1.dll` | Direct2D rendering |
| `SharpDX.DXGI.dll` | DXGI types |

**Framework assemblies** (Add Reference → Assemblies):

- `WindowsBase`
- `PresentationCore`
- `PresentationFramework`
- `System.Xml.Serialization`

### Set Build Output

Set the build output path to the NinjaTrader custom folder so your compiled DLL loads automatically:

1. Right-click the project → **Properties → Build**
2. Set **Output path** to: `Documents\NinjaTrader 8\bin\Custom\`
3. Set **Platform target** to **x64**

### Namespace Convention

NinjaTrader requires strategies to live under the `NinjaTrader.NinjaScript.Strategies` namespace:

```csharp
namespace NinjaTrader.NinjaScript.Strategies.MyProject
{
    public class MyStrategy : MZpackStrategyBase
    {
        // ...
    }
}
```

For custom indicators, use `NinjaTrader.NinjaScript.Indicators.MyProject`.

## Minimal Strategy Template

A minimal MZpack strategy with one indicator:

```csharp
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using MZpack;
using MZpack.NT8;
using MZpack.NT8.Algo;
using MZpack.NT8.Algo.Indicators;
using NinjaTrader.Data;

namespace NinjaTrader.NinjaScript.Strategies.MyProject
{
    public class MyFirstStrategy : MZpackStrategyBase
    {
        StrategyBigTradeIndicator bigTradeIndicator;

        public MyFirstStrategy() : base()
        {
            OnCreateIndicators = new OnCreateIndicatorsDelegate(CreateIndicators);
            OnBarCloseHandler = new OnTickDelegate(OnBarClose);
        }

        protected List<TickIndicator> CreateIndicators()
        {
            List<TickIndicator> indicators = new List<TickIndicator>();

            bigTradeIndicator = new StrategyBigTradeIndicator(this, "BigTrade")
            {
                TradeFilterEnable = true,
                TradeFilterMin = TradeMin
            };
            indicators.Add(bigTradeIndicator);

            return indicators;
        }

        protected override void OnStateChange()
        {
            base.OnStateChange();

            lock (Sync)
            {
                if (State == State.SetDefaults)
                {
                    BarsRequiredToTrade = 1;
                    EntriesPerDirection = 1;
                    TradeMin = 50;
                }
                else if (State == State.Configure)
                {
                    bigTradeIndicator.TradeFilterMin = TradeMin;
                }
            }
        }

        protected void OnBarClose(MarketDataEventArgs e, int currentBarIdx)
        {
            // Your trading logic here
        }

        [Display(Name = "Min trade volume", GroupName = "Strategy", Order = 0)]
        [Range(1, int.MaxValue)]
        [NinjaScriptProperty]
        public long TradeMin { get; set; }
    }
}
```

### Key Points

| Concept | Detail |
|---|---|
| **Base class** | Inherit from `MZpackStrategyBase`, not NinjaTrader's `Strategy` |
| **Constructor** | Set `OnCreateIndicators` and optionally `OnBarCloseHandler` / `OnEachTickHandler` delegates |
| **`OnStateChange`** | Always call `base.OnStateChange()` first and wrap in `lock (Sync)` |
| **`State.SetDefaults`** | Set default property values |
| **`State.Configure`** | Apply UI property values to indicators, create entries and patterns |
| **Indicator creation** | Return a `List<TickIndicator>` from your `CreateIndicators` method |
| **Properties** | Use `[Display]` and `[NinjaScriptProperty]` attributes for NinjaTrader UI |

## Working with Samples

All MZpack API samples are included in the source code within `#if APISAMPLE` blocks. To compile a sample in NinjaTrader:

1. Copy the sample `.cs` file to `Documents\NinjaTrader 8\bin\Custom\Strategies\`
2. Remove the `#if APISAMPLE` directive at the top and the `#endif` at the bottom
3. Compile in NinjaTrader (press **F5** in the NinjaScript Editor)

## Next Steps

- [API Overview](overview.md) — architecture and available interfaces
- [Advanced Template](../samples/advanced-template.md) — full-featured strategy template with dual entries, control panel, and XML persistence
- [Custom Strategy — VWAP/POC](../samples/custom-strategy-vwap-poc.md) — simple backtesting strategy using volume profile
