---
sidebar_position: 3
title: "mzVolumeProfile"
description: "Volume profile and Market Profile (TPO) indicator with POC, Value Area, VWAP, stacked profiles, and TPO levels for NinjaTrader 8"
---

# mzVolumeProfile

The mzVolumeProfile indicator displays horizontal volume distribution across price levels overlaid on the NinjaTrader chart. It supports Volume Profile, TPO (Market Profile), and combined VP+TPO modes. Profiles can be created per session, daily, weekly, monthly, or by custom criteria, with up to 3 independent stacked profiles on the chart right margin.

**Data required:** Level 1 (tick data). Tick Replay is optional — enable for precise delta on historical data, or disable and use Minute accuracy for faster loading.

## Key Features

- **Multiple profile creation modes** — Session, Daily, Weekly, Monthly, Quarterly, Yearly, Composite, Custom, Volume-based, Delta-based, Tick-based, Continuous, RTH/ETH
- **3 profile views** — Ladders, Area, Contour
- **4 profile types** — Volume, BuySell, Delta, VolumeDelta
- **TPO (Market Profile)** with letters/blocks, Initial Balance, halfback, open/close markers
- **POC and Value Area** (VAH/VAL) with 6 level modes — Off, On, Naked, Extended, Developing, DevelopingNaked
- **VWAP** with configurable standard deviations
- **3 TPO level groups** with 10 level types each (Open, Close, High, Low, Mid, IB High, IB Low, TPO POC, TPO VAL, TPO VAH)
- **3 independent stacked profiles** on the chart right margin
- **Profile statistics** — Volume, Delta, High/Low, Range, POC, VAH/VAL, VWAP, Begin/End, TPOs
- **Custom profiles** with mouse interaction — add, divide, merge, unmerge, split
- **5 color modes** — Solid, Saturation, Heatmap, GrayScaleHeatmap, Custom
- **Profile accuracy** — Tick (precise) or Minute (fast)
- **Working time filter** with start/stop time
- **Custom S/R levels** with alerts (licensed builds)

## Profile Creation Modes

| Mode | Description |
|---|---|
| **Session** | One profile per trading session |
| **Daily** | One profile per calendar day |
| **Weekly** | One profile per week |
| **Monthly** | One profile per month |
| **Quarterly** | One profile per quarter |
| **Yearly** | One profile per year |
| **Composite** | Cumulative profile for all chart data |
| **Bar** | One profile per bar |
| **Bars** | One profile per N bars (set N via Creation value) |
| **Sessions** | Cumulated profile for N last sessions (stacked profiles only) |
| **Days** | Cumulated profile for N last days (stacked profiles only) |
| **Weeks** | Cumulated profile for N last weeks (stacked profiles only) |
| **Months** | Cumulated profile for N last months (stacked profiles only) |
| **Volume** | New profile when cumulative volume reaches Creation value |
| **Delta** | New profile when cumulative delta reaches Creation value |
| **Tick** | New profile every N ticks |
| **Custom** | Manually add profiles with mouse click |
| **Continuous** | Single continuous profile — use with Working time filter |
| **RTH_ETH** | Separate profiles for RTH and ETH sessions |
| **None** | No profile |

## Profile Views

| View | Description |
|---|---|
| **Ladders** | Horizontal histogram bars showing volume at each price level |
| **Area** | Filled area shape |
| **Contour** | Outline only |

## Profile Types

| Type | Description |
|---|---|
| **Volume** | Total volume histogram |
| **BuySell** | Separate buy and sell volume ladders |
| **Delta** | Bid/ask delta histogram |
| **VolumeDelta** | Volume ladders colored by delta direction |
| **None** | Profile hidden |

## Color Modes

| Mode | Description |
|---|---|
| **Solid** | Uniform color for all ladders |
| **Saturation** | Color intensity scales with value — higher values are more saturated |
| **Heatmap** | Multi-color gradient from cool to hot |
| **GrayScaleHeatmap** | Monochrome intensity gradient |
| **Custom** | User-defined color thresholds — Percent or Value based |

### Custom Color Mode

When Color mode is set to **Custom**, you choose between two sub-modes:

**Percent** — 10 percentage-based tiers, each with its own color. Each ladder is colored based on its value as a percentage of the profile's maximum:

| Tier | Default Color |
|---|---|
| 0–10% | DarkRed |
| 10–20% | Red |
| 20–30% | Chocolate |
| 30–40% | DarkOrange |
| 40–50% | Orange |
| 50–60% | Yellow |
| 60–70% | Green |
| 70–80% | LightGreen |
| 80–90% | Teal |
| 90–100% | DodgerBlue |

**Value** — 5 absolute value thresholds:

| Threshold | Default Color |
|---|---|
| >= 0 | DarkRed |
| >= 1,000 | Red |
| >= 10,000 | Orange |
| >= 20,000 | Yellow |
| >= 40,000 | DodgerBlue |

## Settings Reference

### Common

| Setting | Default | Description |
|---|---|---|
| **Chart profiles** | VP | Profile type displayed on chart — TPO, VP, VP_TPO, or None |
| **Chart profile mode** | Session | How profiles are created (see Profile Creation Modes) |
| **RTH begin** | 08:30 | Regular Trading Hours start time |
| **RTH end** | 15:15 | Regular Trading Hours end time |
| **ETH** | true | Enable Extended Trading Hours |
| **ETH begin** | 17:30 | Extended Trading Hours start time |
| **ETH end** | 08:30 | Extended Trading Hours end time |
| **Profile creation value** | 5 | Creation threshold for value-based modes (Volume, Delta, Tick, Bars) |
| **Session break** | true | New session breaks profile when mode = Bars |
| **Profile accuracy** | Tick | Tick (precise, slower) or Minute (fast, approximate) |
| **Ticks per level** | 1 | Price level aggregation — set to 2+ to merge adjacent levels |
| **Border** | true | Show profile border |
| **Border** | Cyan, Dot, 1px | Border line style |
| **Background** | false | Show profile background fill |
| **Background** | DarkSlateBlue | Background color |
| **Background opacity, %** | 10 | Background transparency |
| **Buttons** | true | Show toolbar buttons |
| **Buttons font** | Montserrat, 10pt | Toolbar button font |

### Volume Profile

| Setting | Default | Description |
|---|---|---|
| **Profile type** | Volume | Volume, BuySell, Delta, VolumeDelta, or None |
| **Profile view** | Ladders | Ladders, Area, or Contour |
| **VA, %** | 68 | Value Area percentage |
| **Show last N profiles** | -1 | Show only last N profiles (-1 = all) |
| **Position** | Left | Profile placement — Left, Right, or RightOnChartMargin |
| **Width, %** | 50 | Profile width as percentage of bar space (-100 to 100) |
| **Relative width** | false | Scale width of profiles relative to each other across all chart profiles |
| **Profile: left margin, px** | 0 | Left margin in pixels |
| **Profile: right margin, px** | 10 | Right margin in pixels |
| **Color mode** | Solid | Solid, Saturation, Heatmap, GrayScaleHeatmap, or Custom |
| **Custom color mode** | Percent | Percent (10 tiers) or Value (5 thresholds) |
| **VA color** | RoyalBlue | Value Area ladder color |
| **VAH/VAL color** | Gray | Ladders outside Value Area |
| **Buy color** | LightGreen | Buy-side ladder color (BuySell mode) |
| **Sell color** | Red | Sell-side ladder color (BuySell mode) |
| **Opacity, %** | 50 | Ladder fill transparency |
| **Values: show** | None | Display values on ladders — Volume, Delta, BidAsk, or None |
| **Values: 1K divider** | true | Divide displayed values by 1,000 |
| **Values: color** | White | Values text color |
| **Values: font** | Montserrat, 10pt | Values font |
| **Delta: show** | false | Show delta histogram alongside profile |
| **Delta: % of profile width** | 20 | Delta histogram width relative to profile (-100 to 100) |
| **Delta: positive** | LimeGreen | Positive delta color |
| **Delta: negative** | Red | Negative delta color |
| **Delta: opacity, %** | 100 | Delta histogram transparency |
| **Delta: saturation** | false | Enable delta color saturation |
| **Profile: developing border** | Yellow, Dot, 1px | Border style for the developing (current) profile |
| **Profile: ladders borders** | false | Show borders around individual ladders |
| **Profile: labels font** | Montserrat, 11pt | Profile label font |
| **Custom profile: unique settings** | false | Each custom profile has unique settings accessible via buttons |
| **Custom profile: add = Mouse Left +** | LeftCtrl | Key modifier to add a custom profile |

### Volume Profile Levels

| Setting | Default | Description |
|---|---|---|
| **POC: mode** | On | POC level mode — Off, On, Naked, Extended, Developing, DevelopingNaked |
| **POC: line** | DarkOrange, Dash, 2px | POC line style |
| **Developing Tick POC** | false | Show developing Tick POC line |
| **Tick POC: line** | Red, Dash, 2px | Tick POC line style |
| **VAH/VAL: mode** | On | VAH/VAL level mode — Off, On, Naked, Extended, Developing, DevelopingNaked |
| **VAH/VAL: line** | Gray, Dash, 1px | VAH/VAL line style |
| **Levels values** | Price | Value displayed at level lines — Price, Volume, Delta, or None |

#### Level Modes Explained

| Mode | Description |
|---|---|
| **Off** | Level not displayed |
| **On** | Level drawn within profile boundaries only |
| **Extended** | Level extends from profile to chart right edge |
| **Naked** | Level extends until price touches it (then disappears) |
| **Developing** | Level updates in real time as the profile builds |
| **DevelopingNaked** | Developing + disappears when price touches the level |

### Volume Profile VWAP

| Setting | Default | Description |
|---|---|---|
| **VWAP: mode** | Dynamic | Last, Dynamic, DynamicStdDev1, DynamicStdDev2, or None |
| **VWAP: line** | SteelBlue, Dash, 2px | VWAP line style |
| **VWAP: Sigma 1** | 1 | First standard deviation multiplier |
| **VWAP: Std deviation #1** | RoyalBlue, 1px | First deviation band line style |
| **VWAP: Sigma 2** | 2 | Second standard deviation multiplier |
| **VWAP: Std deviation #2** | Brown, 1px | Second deviation band line style |

## TPO (Market Profile)

TPO (Time Price Opportunity) displays the time distribution of price activity using letters or blocks. Each letter/block represents one time period (default 30 minutes) during which a price level was traded.

| Setting | Default | Description |
|---|---|---|
| **Letter period, min** | 30 | Duration of one TPO letter/block period |
| **Presentation** | Letter | Display as Letter or Block |
| **Split** | false | Unfold (split) each TPO period separately |
| **Stretched** | false | Stretch TPO to fill available width |
| **Width, %** | 80 | Maximum TPO width as percentage (1–100) |
| **Position** | Left | TPO placement — Left, Right, or RightOnChartMargin |
| **Rotate colors** | false | Cycle through 6 colors for consecutive periods |
| **Letter/block color 1–6** | Red, Orange, Yellow, LimeGreen, DodgerBlue, Sienna | Six rotating TPO colors |
| **Letters font** | Montserrat, 12pt | TPO letters font |
| **Open: letter** | true | Highlight the opening letter |
| **Close: letter** | true | Highlight the closing letter |
| **Open: marker** | true | Show open price marker |
| **Close: marker** | true | Show close price marker |
| **Open period color** | Lime | Color for the opening period |
| **Close period color** | Magenta | Color for the closing period |
| **Open/close profile color** | White | Color for open/close markers on the profile |
| **Show POC** | false | Highlight the TPO POC row |
| **POC: letters/blocks** | false | Use distinct color for POC letters/blocks |
| **POC color** | Goldenrod | TPO POC highlight color |
| **VA, %** | 68 | TPO Value Area percentage |
| **VA box** | true | Draw a box around the Value Area |
| **VA letters/blocks** | true | Use distinct color for VA letters/blocks |
| **VA color** | DodgerBlue | TPO Value Area color |
| **POC/VA opacity, %** | 15 | POC/VA highlight transparency |
| **Show IB** | true | Show Initial Balance range |
| **IB, min** | 60 | Initial Balance period in minutes |
| **IB color** | Chocolate | Initial Balance highlight color |
| **Show Halfback** | false | Show halfback (midpoint) level |
| **Halfback color** | SaddleBrown | Halfback color |

**Notes:**
- TPO letters rotate through 6 colors when **Rotate colors** is enabled
- When there is not enough room for letters, blocks are rendered automatically
- **Split** (unfold) shows each TPO period separately side by side
- **IB** (Initial Balance) = the first N minutes of the session (default 60 min)

## TPO Levels

TPO levels project key price levels from profiles as horizontal lines across the chart. There are **3 independent level groups**, each configurable to track different profiles.

### T-Index Concept

Profiles are indexed using **T-index**: the most recent profile is T0, the one before it is T1, and so on. T-index determines which profile's levels are drawn.

### Per-Group Settings (repeated for groups #1, #2, #3)

| Setting | Default | Description |
|---|---|---|
| **Enable** | #1: true, #2/#3: false | Enable this level group |
| **Attach to** | All | Attach levels to a specific T-index profile (T) or all profiles (All) |
| **Attach to T -** | 0 | T-index of the profile to attach to (when Attach to = T) |
| **Naked by** | Any | How naked levels are canceled — by specific T profile (T), next profile (Next), or any profile (Any) |
| **Naked by T -** | 0 | T-index for naked cancellation (when Naked by = T) |
| **End of Day** | true | Cancel naked levels at end of day |
| **Value position** | None (#1), AboveRight (default) | Position of value labels on level lines |

Each group has **10 level types**, each set to Disabled, Extended, or Naked:

| Level Type | #1 Default | Description |
|---|---|---|
| **Open** | Disabled | Session/profile open price |
| **Close** | Disabled | Session/profile close price |
| **High** | Disabled | Session/profile high |
| **Low** | Disabled | Session/profile low |
| **Mid/Halfback** | Disabled | Midpoint between high and low |
| **IB High** | Disabled | Initial Balance high |
| **IB Low** | Disabled | Initial Balance low |
| **TPO POC** | Naked | TPO Point of Control |
| **TPO VAL** | Naked | TPO Value Area Low |
| **TPO VAH** | Naked | TPO Value Area High |

### Shared Line Styles

| Setting | Default | Description |
|---|---|---|
| **Open line** | DodgerBlue, 1px | Open level line style |
| **Close line** | Blue, 1px | Close level line style |
| **High line** | Red, 2px | High level line style |
| **Low line** | LimeGreen, 2px | Low level line style |
| **Mid line** | Navy, 2px | Mid/Halfback level line style |
| **IB High line** | Orange, 1px | IB High level line style |
| **IB Low line** | DarkOrange, 1px | IB Low level line style |
| **TPO POC line** | Goldenrod, 2px | TPO POC level line style |
| **TPO VAL line** | ForestGreen, Dash, 2px | TPO VAL level line style |
| **TPO VAH line** | Crimson, Dash, 2px | TPO VAH level line style |
| **Value color** | LightGray | Level value text color |
| **Value font** | Montserrat, 11pt | Level value font |

## Profile Statistics

Summary information displayed above each profile.

| Setting | Default | Description |
|---|---|---|
| **Volume** | true | Show total volume |
| **Delta** | Delta | Delta display mode — Delta, BidAsk, or None |
| **High/Low** | true | Show profile high and low prices |
| **Range, points/ticks** | false | Show price range in points and ticks |
| **POC** | false | Show POC price |
| **VAH/VAL** | false | Show VAH and VAL prices |
| **VWAP** | false | Show VWAP price |
| **Begin/End** | false | Show profile begin and end times |
| **TPOs** | true | Show TPO count |

## Stacked Profiles

Up to **3 independent volume profiles** rendered on the chart right margin. Each stacked profile can display a different time period, creation mode, and profile type. Stacked profiles support cumulation and time shifting.

### Per-Profile Settings (repeated for #1, #2, #3)

| Setting | Default (#1) | Description |
|---|---|---|
| **Show** | VP | Profile type — TPO, VP, VP_TPO, or None |
| **Mode** | Session | Profile creation mode |
| **Creation value** | 0 | N for cumulated/shifted profiles (e.g., Sessions[2] = last 2 sessions) |
| **Type** | Volume | Volume, BuySell, Delta, VolumeDelta, or None |
| **Presentation** | Area | Ladders, Area, or Contour |
| **POC/VAH/VAL mode** | Extended | Off, On, or Extended |
| **POC** | RoyalBlue, Dash, 3px | POC line style |
| **VAH/VAL** | Coral, Dash, 2px | VAH/VAL line style |
| **Delta** | false | Show delta alongside stacked profile |

Stacked profiles #2 and #3 default to **None** (disabled).

### Shared Stacked Settings

| Setting | Default | Description |
|---|---|---|
| **Delta width, %** | 80 | Delta histogram width relative to stacked profile (-100 to 100) |
| **Left margin, px** | 50 | Left margin for stacked profiles |
| **Right margin, px** | 0 | Right margin for stacked profiles |
| **Legend** | true | Show profile legend |

### Creation Value Examples

- **Sessions[2]** — cumulated profile for the last 2 sessions
- **Daily[1]** — profile for 1 day ago
- **Monthly[0]** — current month's profile
- **Session[0]** — current session (developing profile)

A stacked profile is "developing" if it contains the last chart bar.

Extended POC/VAH/VAL lines from stacked profiles start at the profile edge and continue to the right.

## Profile Interaction

Profile interaction features let you modify profiles directly on the chart via toolbar buttons.

- **Splitting (unfolding)** — unfold TPO profiles to show each period separately
- **Dividing** — click the Divide button, then click a bar to split the profile at that point
- **Merging** — merge a profile with its left or right neighbor
- **Unmerging** — undo a merge (not available in Custom mode)

Profile interaction is **not available** in Composite modes.

## Custom Profiles

When Chart profile mode is set to **Custom**:

- Add a profile by holding **Mouse Left + LeftCtrl** (configurable) and clicking on the chart
- Enable **Custom profile: unique settings** to give each custom profile its own type, view, and color settings (accessible via on-chart buttons)
- The last added custom profile has T-index = 0

## Profile Accuracy and Calculate Modes

| Loading Time | Real-time Performance | Calculate | Historical Resolution | Real-time Resolution |
|---|---|---|---|---|
| Normal | Normal | OnEachTick | 1 Tick | 1 Tick |
| Fast | Normal | OnEachTick | 1 Minute | 1 Tick |
| Fast | Fast | OnBarClose | 1 Minute | 1 Minute |

**Tick accuracy:**
- Provides the most precise volume distribution and delta
- Enable **Tick Replay** for accurate delta on historical data
- Higher CPU and loading time

**Minute accuracy:**
- Disable Tick Replay and use a minute-based chart period (e.g., 30 Min)
- Historical volumes are spread proportionally across each minute bar's price range; up-bar volume = buy, down-bar volume = sell
- Significantly reduces loading time
- Recommended for large profiles (weekly, monthly, yearly, TPO)

## Working Time

Filter when the indicator processes market data using General > **Working time filter** with **Start time** / **Stop time**.

- Supports overnight sessions (Stop time falls on the next day)
- Recommended to use with **Continuous** profile mode when Working time filter is enabled

| Setting | Default | Description |
|---|---|---|
| **Working time** | false | Enable working time filter |
| **Start time** | 08:30 | Data processing start time |
| **Stop time** | 15:30 | Data processing stop time |

## Levels (Licensed Builds)

Custom support/resistance levels drawn on the chart with mouse interaction.

| Setting | Default | Description |
|---|---|---|
| **Enable** | false | Enable custom S/R levels |
| **Support level** | LightGreen, Opacity 25 | Support level line style |
| **Resistance level** | Red, Opacity 25 | Resistance level line style |
| **Value position** | AboveRight | Label placement on level lines |
| **Value/Label color** | LightGray | Level label text color |
| **Value/Label font** | Arial, 10pt | Level label font |
| **Alert** | true | Enable sound alerts |
| **Alert on** | LevelCross | Alert trigger event |
| **Rearm** | true | Re-enable alert after firing |
| **Rearm interval, sec** | 3 | Seconds before alert can fire again |
| **Sound** | crossed.wav | Alert sound file |
| **Add/remove: Mouse Left +** | LeftShift | Key modifier to add or remove a level |
| **Modify: Mouse Left +** | LeftAlt | Key modifier to move a level |
| **Drag with Mouse** | true | Enable drag-and-drop level repositioning |

## Performance Tips

- Set **Ticks per level** to 2+ for instruments with many price levels
- Set **Profile accuracy** to **Minute** for large profiles (weekly, monthly, yearly)
- Use **OnBarClose** calculate mode with Minute accuracy for maximum performance
- Toggle TPO visibility via the eye button when TPO is not needed
- Set **MaximalRenderMs** to 20–50 ms for responsive charts (chart may flash briefly)
- Close unused shadow workspaces and remove unused indicators

## Non-Bid/Ask Data Support

Some markets (Forex, cryptocurrencies, NSE/Indian stock market) do not provide historical bid/ask data. Without it, all historical trades appear on the Bid side only.

**Solution:** Set `Orderflow > Calculation mode` to **UpDownTick** for these instruments.

**Hybrid mode (NSE):** NSE data providers do not transmit historical bid/ask data. Use **Hybrid** mode, which applies UpDownTick calculation for historical data and BidAsk for real-time data.

**Recommendation:** For Forex pairs, use the relevant futures contract (e.g., 6E for EURUSD) to get accurate bid/ask data and full order flow features.
