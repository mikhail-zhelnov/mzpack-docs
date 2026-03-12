---
sidebar_position: 4
title: "Control Panel"
description: "MZpack Control Panel with [ControlPanel] attribute and custom UI elements (Button, ComboBox)."
---

# Control Panel

Demonstrates both ways to add controls to the MZpack Control Panel: the `[ControlPanel]` attribute on properties, and custom UI elements via `CreateControlPanelElements()`. The strategy trades up/down bars on bar close.

**Source:** `MZpack.NT8/Algo/Samples/Built-in/ControlPanel.cs`
**Class:** `ControlPanel : MZpackStrategyBase`

## What It Covers

- `[ControlPanel]` attribute on `bool` and `enum` properties
- Custom `Button` and `ComboBox` via `CreateControlPanelElements()`
- Event handler attach/detach lifecycle
- Live property updates from UI controls

## Two Ways to Add Controls

### 1. `[ControlPanel]` Attribute

Add the attribute to any public `bool` or `enum` property. The control panel renders it automatically:

```csharp
[Display(Name = "Operating", GroupName = "MZpack", Order = 2)]
[ControlPanel]
public override StrategyOperating Operating { get; set; }

[Display(Name = "Opposite Pattern Action", GroupName = "Common", Order = 1)]
[ControlPanel]
public OppositePatternAction OppositePatternAction { get; set; }

[Display(Name = "Direction", GroupName = "Position", Order = 0)]
[ControlPanel()]
public SignalDirection Position_Direction
{
    get { return position_Direction; }
    set
    {
        position_Direction = value;
        if (Strategy != null && Strategy.Pattern != null)
            Strategy.Pattern.AllowedDirection = value;
    }
}
```

### 2. Custom UI Elements

Override `CreateControlPanelElements()` to return WPF controls:

```csharp
public override UIElement[] CreateControlPanelElements()
{
    UIElement[] ui = new UIElement[3];

    // Label + ComboBox for direction
    ui[0] = new Label()
    {
        Content = "Direction",
        Foreground = ChartControl.Properties.ChartText,
        Margin = new Thickness(
            ControlPanelAttribute.UIELEMENT_LEFT_MARGIN, 0,
            ControlPanelAttribute.UIELEMENT_RIGHT_MARGIN,
            ControlPanelAttribute.UIELEMENT_BOTTOM_MARGIN)
    };
    ui[1] = directionComboBox = new ComboBox()
    {
        ItemsSource = Enum.GetValues(typeof(SignalDirection)),
        SelectedValue = Position_Direction
    };

    // Button
    ui[2] = showPatternsButton = new Button()
    {
        Content = ShowPatterns ? "Hide patterns" : "Show patterns"
    };

    return ui;
}
```

## Event Handler Lifecycle

Attach handlers in `ControlPanel_AttachEventHandlers`, detach in `ControlPanel_DetachEventHandlers`:

```csharp
public override void ControlPanel_AttachEventHandlers()
{
    if (directionComboBox != null)
        directionComboBox.SelectionChanged += DirectionComboBox_SelectionChanged;
    if (showPatternsButton != null)
        showPatternsButton.Click += ShowPatternsButton_Click;
}

public override void ControlPanel_DetachEventHandlers()
{
    if (directionComboBox != null)
        directionComboBox.SelectionChanged -= DirectionComboBox_SelectionChanged;
    if (showPatternsButton != null)
        showPatternsButton.Click -= ShowPatternsButton_Click;
}
```

Handlers update strategy state directly:

```csharp
public void DirectionComboBox_SelectionChanged(object sender,
    SelectionChangedEventArgs e)
{
    Position_Direction = (SignalDirection)(sender as ComboBox).SelectedItem;
}

public void ShowPatternsButton_Click(object sender, RoutedEventArgs e)
{
    ShowPatterns = !ShowPatterns;
    (sender as Button).Content = ShowPatterns ? "Hide patterns" : "Show patterns";
}
```

## Strategy Logic

The included `UpDownBarSignal` is a simple on-bar-close signal: Long for up-bars, Short for down-bars. The strategy uses `OppositePatternAction.Reverse` to reverse position on opposite signals.

## Properties

| Property | Default | Description |
|---|---|---|
| `OppositePatternAction` | `Reverse` | Action on opposite signal |
| `Position_Direction` | `Any` | Allowed direction |
| `Position_Quantity` | `2` | Contracts |
| `Position_StopLoss` | `6` | Stop loss ticks |
| `Position_ProfitTarget` | `12` | Profit target ticks |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — `CreateControlPanelElements()` reference
- [Advanced Template](advanced-template.md) — control panel with Trading On/Off, Close, Break Even buttons
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
