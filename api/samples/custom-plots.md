---
sidebar_position: 5
title: "Custom Plots"
description: "Custom chart plots via StrategyPlotIndicator — overlay and panel indicators with footprint data access."
---

# Custom Plots

Demonstrates `StrategyPlotIndicator` for drawing custom plot lines on the chart. Two indicators are created: one overlaid on the price chart, and one on a separate panel below.

**Source:** `[INSTALL PATH]/API/Samples/Built-in/CustomPlots.cs`
**Class:** `CustomPlots : MZpackStrategyBase`

## What It Covers

- Subclassing `StrategyPlotIndicator` for custom plots
- Overlay plots on the price chart
- Panel plots below the chart (`IsOnPanel = true`)
- Accessing footprint bar data (`IFootprintBar`) from a plot indicator
- Configuring plot strokes, visibility, and panel height

## Chart Overlay Indicator

`CustomPlotsIndicator` plots two lines on the price chart — one above bar highs, one below bar lows (intermittently):

```csharp
class CustomPlotsIndicator : StrategyPlotIndicator
{
    int c;

    public CustomPlotsIndicator(MZpackStrategyBase strategy,
        ISeries<double> input)
        : base(strategy, input, new Series<double>[2])  // 2 plots
    {
    }

    public override string IndicatorName() => "Custom Plots";

    public override void BarUpdate()
    {
        if (__CurrentBar > 0)
        {
            int currBarIdx = __CurrentBar - 1;
            // Plot 0: above bar high
            Values[0][currBarIdx] = __High[1] + 2 * strategy.TickSize;

            // Plot 1: below bar low (only 4 out of 8 bars)
            c++;
            if (c <= 4)
                Values[1][currBarIdx] = __Low[1] - 2 * strategy.TickSize;
            else if (c >= 8)
                c = 0;
        }
    }
}
```

## Panel Indicator

`CustomPlotsOnPanelIndicator` plots COT High/Low from footprint data on a separate panel:

```csharp
class CustomPlotsOnPanelIndicator : StrategyPlotIndicator
{
    public CustomPlotsOnPanelIndicator(MZpackStrategyBase strategy,
        ISeries<double> input)
        : base(strategy, input, new Series<double>[2])
    {
    }

    public override string IndicatorName() => "Custom Plots on Panel";

    public override void BarUpdate()
    {
        if (__CurrentBar > 0)
        {
            int currBarIdx = __CurrentBar - 1;
            IFootprintBar bar;
            if ((strategy as CustomPlots).FootprintIndicator
                .FootprintBars.TryGetValue(currBarIdx, out bar))
            {
                Values[0][currBarIdx] = bar.COTHigh;
                Values[1][currBarIdx] = bar.COTLow;
            }
        }
    }
}
```

## Configuration

Both indicators are configured in `CreateIndicators`:

```csharp
// Overlay indicator
customPlotsIndicator = new CustomPlotsIndicator(this, Close);
customPlotsIndicator.Calculate = Calculate.OnBarClose;
customPlotsIndicator.Strokes[0] = new Stroke(Brushes.Red, 2);
customPlotsIndicator.Strokes[1] = new Stroke(Brushes.Green, 2);
customPlotsIndicator.Visible = true;

// Panel indicator
customPlotsOnPanelIndicator = new CustomPlotsOnPanelIndicator(this, Close);
customPlotsOnPanelIndicator.Calculate = Calculate.OnBarClose;
customPlotsOnPanelIndicator.IsOnPanel = true;
customPlotsOnPanelIndicator.PanelHeight = 400;
customPlotsOnPanelIndicator.IsUpperPanel = false;
customPlotsOnPanelIndicator.Strokes[0] = new Stroke(Brushes.DodgerBlue, 2);
customPlotsOnPanelIndicator.Strokes[1] = new Stroke(Brushes.Yellow, 2);
customPlotsOnPanelIndicator.Visible = true;
```

## StrategyPlotIndicator Key Points

| Property / Method | Description |
|---|---|
| Constructor `new Series<double>[N]` | Number of plot series |
| `IndicatorName()` | Display name for the indicator |
| `BarUpdate()` | Called on each bar close — write values to `Values[n][barIdx]` |
| `Strokes[n]` | Plot line color and width |
| `IsOnPanel` | `true` = render on separate panel, `false` = overlay on chart |
| `PanelHeight` | Panel height in pixels (when `IsOnPanel = true`) |
| `IsUpperPanel` | Panel position: above (`true`) or below (`false`) the chart |
| `Visible` | Show/hide the indicator |
| `Calculate` | `OnBarClose` or `OnEachTick` |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzFootprint](data-access-footprint.md) — footprint data access
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
