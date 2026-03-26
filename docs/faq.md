---
sidebar_position: 5
title: "FAQ"
description: "Frequently asked questions about MZpack indicators, licensing, and NinjaTrader 8 integration"
---

# FAQ

Common questions about MZpack indicators for NinjaTrader 8.

## General

### Does MZpack work with any NinjaTrader 8 license?

Yes. MZpack works with every NinjaTrader 8 license type — demo, free, subscription, and lifetime. Note that NinjaTrader's demo license is limited to simulated accounts and expires after approximately two weeks. The free NinjaTrader platform requires a NinjaTrader Brokerage account. See [NinjaTrader pricing](https://ninjatrader.com/pricing/) for details on their license options.

### What is the difference between Trial and FREE versions?

**Trial** gives you access to all MZpack features for 14 days. It can only be started once per machine.

**FREE** includes mzFootprint, mzVolumeProfile, and mzBigTrade with limited features. It has no expiration and does not require a license key.

See [Licensing](getting-started/licensing.md) for the full license comparison table.

### How do I submit a feature request?

Post a new topic on the [MZpack Forum](https://forum.mzpack.pro). Other users vote on the request with a Like. When enough interest builds, the MZpack team announces a funding goal. Development starts after funding is collected. The minimum contribution is EUR 25.

## Download and Installation

### Where can I download the latest version?

Download the latest MZpack installer from [mzpack.pro](https://mzpack.pro). You can also find download links in your account at **My Profile → Account** or in your order confirmation email.

See [Installation](getting-started/installation.md) for the full download and setup guide.

### How do I update MZpack?

1. Close NinjaTrader 8
2. Run the new MZpack installer
3. Restart NinjaTrader 8

Your license and settings are preserved across updates. See [Installation — Update](getting-started/installation.md#update) for details.

### How do I check which version is installed?

There are three ways:

1. **Indicators list** — open the Indicators dialog and look under the **MZpack/NT8** folder in the Available list. The version number appears next to each indicator name.
2. **Chart overlay** — the current version is displayed in the bottom-right corner of the chart. You can hide this via the indicator's **General → Version** checkbox.
3. **Label property** — the **Label** property shown in the indicator setup dialog reflects the version from when the indicator was first added to the chart, not the currently installed version. Do not rely on it to check your current version.

## Licensing

### Where can I find my license key?

Two places to look:

1. **Account page** — log in at [mzpack.pro](https://mzpack.pro) → **My Profile → Account → Orders → View**
2. **Order confirmation email** — check your inbox for the order confirmation. Also check spam, junk, and promotions folders.

See [Licensing](getting-started/licensing.md) for activation steps.

### I didn't receive my license key

License keys are sent within the next business day after purchase, usually within 3–5 hours. If you haven't received yours:

1. Check your spam, junk, and promotions folders
2. Some mail servers block messages from unknown senders — try adding the sender to your contacts or provide an alternative email address (e.g., Gmail)
3. If you still can't find it, contact support at [mzpack.pro](https://mzpack.pro)

### Can I transfer my license to another machine?

Yes. MZpack licenses are machine-locked, so a transfer is required when you move to a new machine or replace critical hardware (motherboard, CPU). You'll need to purchase the Transfer Service at mzpack.pro. See [Licensing — Transfer](getting-started/licensing.md#transfer-to-another-machine) for the full steps.

### How can I manage my subscription provided by PayPro Global?

Your MZpack subscription payments are collected by **PayPro Global**. To manage your subscription, update payment details, or download invoices, visit the [PayPro Global Customer Portal](https://payproglobal.com/customer-support/).

### Is MZpack ready to use immediately after installation, or is some initial setup required?

The installation itself is simple — MZpack deploys all indicators, chart templates, and workspaces automatically. However, there are a few steps you need to take before things work correctly:

- **Enable Tick Replay** in NinjaTrader (**Tools → Options → Market Data**), and also turn it on per chart via **Data Series → Tick Replay**. Without this, the indicators won't process historical Bid/Ask data accurately — this is the most important step.
- **Activate your license** — an activation prompt appears on first launch.

Once those are done, you can load a workspace and start analyzing right away using the pre-built chart templates. For live trading with the strategies, some additional tuning of filters, stops, and risk limits is expected — the strategies ship with default values, but they're designed to be adjusted to your instrument and style rather than used blindly out of the box.

So in short: ready to analyze quickly, ready to trade after some parameter review.

## Strategies

### Do the built-in strategies include recommendations for specific instruments and timeframes?

Each built-in strategy comes with dedicated documentation covering its logic, signals, filters, and recommended usage scenarios — but explicit per-asset or per-timeframe recommendations are not provided.

For **Footprint Action**, the documentation focuses on the 10 order-flow signals and available filters, leaving instrument and timeframe selection to the trader's discretion.

For **Ghost Resistance**, the documentation is more specific about market conditions: the strategy performs best during rotational, range-bound sessions with clearly defined support/resistance levels and frequent stop-runs. Strong trend days and news events are flagged as unfavorable conditions.

Both strategies are designed for liquid futures markets, making instruments like ES or NQ natural candidates — but no default configuration is tied to a specific symbol or bar type. Finding the right combination for your setup will require your own testing and optimization.
