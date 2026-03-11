---
sidebar_position: 3
title: "ILevelsIndicator"
description: "Reference for the ILevelsIndicator interface — horizontal price levels with alerts, keyboard shortcuts, and drag support."
---

# ILevelsIndicator

Interface for indicators that support interactive horizontal price levels on the chart. Users can add, remove, drag, and set alerts on levels. Levels persist across sessions via XML serialization.

**Namespace:** `MZpack`
**Inheritance:** `ILevelsIndicator : IIndicator`

Implemented by `LevelsIndicator` (abstract), which is the base class for `mzBigTrade`, `mzFootprint`, `mzMarketDepth`, and `mzVolumeDelta`. There is no standalone "mzLevels" indicator — levels are a feature built into these order flow indicators.

## Properties

### Data

| Property | Type | Description |
|---|---|---|
| `Levels` | `List<LevelBase>` | Collection of all price levels on the chart |

### Enable / Disable

| Property | Type | Default | Description |
|---|---|---|---|
| `LevelsEnabled` | `bool` | — | Master switch for levels feature |

### Alert Configuration

| Property | Type | Default | Description |
|---|---|---|---|
| `UseLevelAlert` | `bool` | `true` | Enable alerts on levels |
| `LevelAlertEvent` | `AlertEvent` | `LevelCross` | When alert fires: touch or cross |
| `LevelAlertRearm` | `bool` | `true` | Re-arm alert after it fires |
| `LevelAlertRearmInterval` | `int` | 3 | Re-arm interval in seconds |
| `LevelAlertSound` | `string` | `"crossed.wav"` | Sound file for alert |

### Interaction

| Property | Type | Default | Description |
|---|---|---|---|
| `AddRemoveLevelKey` | `KeyBase` | `LeftShift` | Mouse Left + key to add/remove a level |
| `ModifyLevelKey` | `KeyBase` | `LeftAlt` | Mouse Left + key to open level properties |
| `MouseDragLevels` | `bool` | `true` | Allow dragging levels with the mouse |

## Methods

| Method | Returns | Description |
|---|---|---|
| `CreateLevel(IVisual, double, bool)` | `LevelBase` | Create a new level at the given price |
| `GetLevelValueByY(int)` | `double` | Convert a Y pixel coordinate to a price value |
| `GetCurrentChartValue(double)` | `double` | Convert a level value to the current chart coordinate |

## LevelBase (abstract class)

Base class for all level objects. Each level represents a horizontal line at a specific price.

**Namespace:** `MZpack`
**Inheritance:** `LevelBase : VisualBase`

### Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `Value` | `double` | — | Price level |
| `Label` | `string` | — | Display label |
| `Duration` | `LevelDuration` | `Infinite` | How long the level persists |
| `Direction` | `LevelDirection` | `Up` | Alert direction filter |
| `UseAlert` | `bool` | `true` | Alert enabled for this level |
| `Event` | `AlertEvent` | `LevelTouch` | Alert event type for this level |
| `DrawOnRightCanvas` | `bool` | `true` | Draw on the right canvas area |

### Methods

| Method | Returns | Description |
|---|---|---|
| `CheckAlert(double, DateTime)` | `bool` | Evaluate whether the alert should fire at the given price and time |
| `AssignValue(double)` | `void` | Set the price value |

## Enums

### LevelDuration

| Value | Description |
|---|---|
| `Infinite` | Level persists indefinitely |
| `Custom` | Level has a defined start/stop time range |

### LevelDirection

| Value | Description |
|---|---|
| `Up` | Alert only when price crosses up through the level |
| `Down` | Alert only when price crosses down through the level |
| `UpDown` | Alert on any crossing |

### AlertEvent

| Value | Description |
|---|---|
| `LevelTouch` | Alert fires when price touches the level |
| `LevelCross` | Alert fires when price crosses through the level |

## Example

```csharp
// Access levels from any indicator that implements ILevelsIndicator
ILevelsIndicator indicator = footprintIndicator;

if (indicator.LevelsEnabled)
{
    foreach (var level in indicator.Levels)
    {
        double price = level.Value;
        string label = level.Label;
        // Check if current price triggers this level's alert
        bool alert = level.CheckAlert(currentPrice, DateTime.Now);
    }
}

// Create a new level programmatically
var newLevel = indicator.CreateLevel(owner, 4500.00, zeroBased: false);
```
