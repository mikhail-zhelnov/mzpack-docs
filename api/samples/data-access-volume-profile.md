---
sidebar_position: 8
title: "Data Access — mzVolumeProfile"
description: "Access StrategyVolumeProfileIndicator data — session profiles with POC, VAH, VAL, VWAP, and Minute accuracy."
---

# Data Access — mzVolumeProfile

Demonstrates how to access volume profile data from `StrategyVolumeProfileIndicator` with Minute accuracy. On each bar close, the strategy prints developing POC, VAH, VAL, and VWAP values for the current session profile.

**Source:** `[INSTALL PATH]/API/Samples/DataAccess_mzVolumeProfile_MinuteAccuracy.cs`
**Class:** `DataAccess_mzVolumeProfile_MinuteAccuracy : MZpackStrategyBase`

## Indicator Setup

```csharp
volumeProfileIndicator = new StrategyVolumeProfileIndicator(this, @"VolumeProfile")
{
    Calculate = Calculate.OnBarClose,
    ShowProfileType = ProfileType.VP,
    ProfileAccuracy = ProfileAccuracy.Minute,
    ProfileCreation = ProfileCreation.Session,
    POCMode = LevelMode.Developing,
    VAHVALMode = LevelMode.On,
    VWAPMode = VWAPMode.DynamicStdDev1,
    ProfileWidthPercentage = 20,
    Values1KDivider = false,

    // No stacked profiles
    StackedProfileCreation1 = ProfileCreation.None,
    StackedProfileCreation2 = ProfileCreation.None,
    StackedProfileCreation3 = ProfileCreation.None
};
```

Important configuration in `State.Configure`:

```csharp
Calculate = Calculate.OnBarClose;  // Minute accuracy requires OnBarClose
volumeProfileIndicator.ModelIncrementRefresh = ModelIncrementRefresh.HistoricalRealtime;
// Required to get historical data in backtesting
```

## Accessing IVolumeProfile

The strategy uses `OnBarUpdate` (not `OnBarCloseHandler`) because it accesses `volumeProfileIndicator.Profiles`:

```csharp
protected override void OnBarUpdate()
{
    base.OnBarUpdate();

    if (BarsInProgress == 0)
    {
        IVolumeProfile last = volumeProfileIndicator.Profiles.LastOrDefault()
            as IVolumeProfile;

        if (last != null)
        {
            // Detect new session profile
            if (last != current)
            {
                // Print totals for previous profile
                if (current != null)
                {
                    Print(string.Format("TOTALS Volume: {0}; Delta: {1}; " +
                        "High: {2}; Low: {3}",
                        current.Volume, current.Delta,
                        current.High, current.Low));
                }
            }

            // Print developing values
            Print(string.Format("{0} VAH: {1}; VAL: {2}; POC: {3}; VWAP: {4}",
                Time[0], last.VAH, last.VAL, last.POC, last.VWAP));

            if (last != current)
                current = last;
        }
    }
}
```

### Available Data

| Property | Type | Description |
|---|---|---|
| `last.POC` | `double` | Point of Control price |
| `last.VAH` | `double` | Value Area High |
| `last.VAL` | `double` | Value Area Low |
| `last.VWAP` | `double` | Volume-Weighted Average Price |
| `last.Volume` | `long` | Total profile volume |
| `last.Delta` | `long` | Total profile delta |
| `last.High` | `double` | Profile high price |
| `last.Low` | `double` | Profile low price |

### Profile Accuracy

| `ProfileAccuracy` | Update Frequency | Use Case |
|---|---|---|
| `Minute` | On bar close | Backtesting, historical analysis |
| `Tick` | On each tick | Real-time precision |

With `ProfileAccuracy.Minute`, set `Calculate = Calculate.OnBarClose` on both the strategy and the indicator.

### Profile Creation Modes

| `ProfileCreation` | Description |
|---|---|
| `Session` | New profile each session |
| `Daily` | New profile each day |
| `Weekly` | New profile each week |
| `Custom` | Manual profile management |
| `None` | Disabled |

## See Also

- [MZpackStrategyBase](../strategies/mzpack-strategy-base.md) — base class
- [Data Access — mzFootprint](data-access-footprint.md) — footprint data
- [Data Access — mzVolumeDelta](data-access-volume-delta.md) — volume delta data
- [Working with Samples](../getting-started/project-setup.md#working-with-samples) — how to compile samples
