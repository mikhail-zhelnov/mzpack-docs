---
sidebar_position: 3
title: "Biggest Trade Indicator"
description: "Custom indicator that marks the biggest trade on the chart with a rectangle using SharpDX rendering."
---

# Biggest Trade Indicator

Demonstrates custom chart rendering with `StrategyBigTradeIndicator`. The strategy finds the biggest trade visible on the chart and draws a rectangle around its marker using SharpDX.

**Source:** `[INSTALL PATH]/API/Samples/BiggestTradeIndicator.cs`
**Class:** `BiggestTradeIndicator : MZpackStrategyBase`

## What It Covers

- `StrategyBigTradeIndicator` setup with trade volume filter
- Custom `OnRender` override for SharpDX drawing
- Accessing `BigTradeBaseMVC.TradesView` to iterate chart trades
- `OnRenderTargetChanged` for brush lifecycle

## Indicator Setup

```csharp
protected List<TickIndicator> CreateIndicators()
{
    List<TickIndicator> indicators = new List<TickIndicator>();

    BigTradeIndicator = new StrategyBigTradeIndicator(this, @"BiggestTrade")
    {
        TradeFilterMin = TradeFilterMin,
        TradeFilterMax = TradeFilterMax,
        ShowVersionInfo = false
    };
    indicators.Add(BigTradeIndicator);

    return indicators;
}
```

## Custom Rendering

`OnRender` collects all trade views from visible chart bars, sorts by volume, and draws a rectangle around the largest:

```csharp
protected override void OnRender(ChartControl chartControl, ChartScale chartScale)
{
    base.OnRender(chartControl, chartScale);

    // Collect trades from visible chart bars
    List<ITradeView> chartTradesViews = new List<ITradeView>();
    for (int i = BigTradeIndicator.__ChartBars.FromIndex;
         i <= BigTradeIndicator.__ChartBars.ToIndex; i++)
    {
        List<ITradeView> tradesOfBar;
        if (((BigTradeBaseMVC)BigTradeIndicator.IndicatorMVC)
            .TradesView.TryGetValue(i, out tradesOfBar))
        {
            chartTradesViews.AddRange(tradesOfBar);
        }
    }

    // Find biggest trade
    chartTradesViews.Sort((a, b) => a.Trade.Volume.CompareTo(b.Trade.Volume));
    BigTradeViewItem biggestTradeView = chartTradesViews.LastOrDefault()
        as BigTradeViewItem;

    // Draw rectangle around it
    if (biggestTradeView != null)
    {
        var bounds = new System.Drawing.RectangleF(
            biggestTradeView.ShapeBounds.Location,
            biggestTradeView.ShapeBounds.Size);
        bounds.Inflate(new System.Drawing.SizeF(5, 5));

        RenderTarget.DrawRectangle(
            Helper.FromSystemDrawingRetcangleF(bounds),
            BiggestTradeMarkerStroke.BrushDX,
            BiggestTradeMarkerStroke.Width,
            BiggestTradeMarkerStroke.StrokeStyle);
    }
}
```

The `OnRenderTargetChanged` override sets `BiggestTradeMarkerStroke.RenderTarget = RenderTarget` to initialize the SharpDX brush when the render target changes.

## Properties

| Property | Default | Description |
|---|---|---|
| `TradeFilterMin` | `150` | Minimum trade size |
| `TradeFilterMax` | `-1` | Maximum trade size (-1 = no limit) |
| `BiggestTradeMarkerStroke` | LightBlue, width 3 | Stroke for the rectangle marker |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
