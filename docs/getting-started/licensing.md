---
sidebar_position: 3
title: "Licensing"
description: "How to activate, manage, and troubleshoot your MZpack license"
---

# Licensing

MZpack uses machine-locked licenses that are tied to your hardware. An internet connection is required for initial activation; after that, MZpack works offline.

## License Types

| License | Indicators | API/Strategies | Duration |
|---|---|---|---|
| **MZpack Indicators** | All 6 indicators | No | Subscription or perpetual |
| **MZpack API** | No | Full strategy framework | Subscription or perpetual |
| **MZpack TRIAL** | All 6 indicators | Full strategy framework | 30 days |
| **MZpack FREE** | Limited features | No | Unlimited |

## Activation

When you add an MZpack indicator to a chart for the first time, the activation window appears automatically.

### Activate with a License Key

1. Add any MZpack indicator to a NinjaTrader chart
2. The **Activation Window** will appear
3. Enter your license key in the text field
4. Click **Activate**
5. MZpack will verify your license online and bind it to your machine
6. When activation succeeds, **restart NinjaTrader 8** to apply

### Start a Trial

If you don't have a license key:

1. Add any MZpack indicator to a chart
2. In the Activation Window, click **START TRIAL**
3. A 30-day full-featured trial will be activated
4. **Restart NinjaTrader 8** to apply

:::note
The trial is tied to your machine and can only be started once.
:::

## Licensed Features

Each MZpack indicator is individually licensed. Depending on your license package, you may have access to different sets of indicators:

| Indicator | Indicators License | Indicators w/ Divergence |
|---|---|---|
| mzVolumeProfile | Yes | Yes |
| mzFootprint | Yes | Yes |
| mzBigTrade | Yes | Yes |
| mzMarketDepth | Yes | Yes |
| mzVolumeDelta | Yes | Yes |
| mzDeltaDivergence | — | Yes |

## Managing Your License

### Check License Status

Your current license status is displayed in the NinjaTrader **Output Window** when MZpack loads. Look for a message like:

```
MZpack Indicators: License is valid. Subscription expires on 2026-12-31.
```

### Transfer to Another Machine

MZpack licenses are locked to the hardware they are activated on. The same process applies when you replace critical hardware parts (motherboard, CPU) on the same machine — the hardware ID changes, so a transfer is required.

To move your license:

1. Uninstall MZpack from the old machine (if it is still accessible)
2. Purchase the **Transfer Service** at [mzpack.pro](https://mzpack.pro)
3. Wait for the order to be processed (within 24 business hours)
4. Install MZpack on the new machine
5. Activate with your existing license key

:::note
The Transfer Service releases all activations tied to your license key. If you have multiple activation slots, you can reassign any or all of them to different machines after the transfer.
:::

### Subscription Renewal

When your subscription expires, MZpack indicators will stop loading. Renew your subscription at [mzpack.pro](https://mzpack.pro), then restart NinjaTrader — your existing activation will reconnect to the renewed license automatically.

## Troubleshooting

### Common License Errors

| Error Message | Cause | Solution |
|---|---|---|
| **License key is not valid** | Incorrect key format | Double-check the key and re-enter it |
| **Invalid Hardware Id** | License is bound to a different machine | Contact support for license transfer |
| **Subscription expired** | License period has ended | Renew your subscription |
| **License cannot be verified for this machine** | Machine limit exceeded | Deactivate on another machine first |
| **License server temporarily unavailable** | Server or network issue | Check your internet connection and try again later |
| **License verification requires internet connection** | No network access | Connect to the internet for verification |
| **License module not found** | Missing DLL dependency | Reinstall MZpack |

### Activation Fails

If activation fails:

1. Verify your internet connection
2. Check that your firewall or antivirus is not blocking `mzpack.pro`
3. Try again after a few minutes — the licensing server may be temporarily unavailable
4. If the problem persists, contact support with your license key and Hardware ID
