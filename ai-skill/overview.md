---
sidebar_position: 1
title: "MZpack AI Skill"
description: "Portable Agent Skill for creating NinjaTrader 8 strategies with the MZpack Strategies API."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MZpack AI Skill

## What Is MZpack AI Skill

MZpack AI Skill is a portable, versioned Agent Skill that gives AI agents the correct context for creating NinjaTrader 8 strategies with the MZpack Strategies API.

It includes the API surface, 16 worked examples, three buildable templates, and common pitfalls. It requires MZpack Strategies or Full Suite: the corpus does not compile with the Indicators-only package.

## Compatibility

| Component | Version or Requirement |
| --- | --- |
| MZpack AI Skill | 1.0.2 |
| Strategies API | 2.4.17 |
| Platform | NinjaTrader 8 |
| Runtime | .NET Framework 4.8 |
| Language | C# 7.3 |
| Build | MSBuild |

## Installation

From the root of your strategy project, install the fixed `skill-v1.0.2` release in your agent's skill directory.

<Tabs>
<TabItem value="codex" label="Codex" default>

```powershell
git clone --branch skill-v1.0.2 --depth 1 https://github.com/mikhail-zhelnov/mzpack-strategy-corpus.git .codex\skills\mzpack-strategies
```

</TabItem>
<TabItem value="claude-code" label="Claude Code">

```powershell
New-Item -ItemType Directory -Force .claude\skills | Out-Null
git clone --branch skill-v1.0.2 --depth 1 https://github.com/mikhail-zhelnov/mzpack-strategy-corpus.git .claude\skills\mzpack-strategies
```

</TabItem>
<TabItem value="cursor" label="Cursor">

```powershell
New-Item -ItemType Directory -Force .cursor\skills | Out-Null
git clone --branch skill-v1.0.2 --depth 1 https://github.com/mikhail-zhelnov/mzpack-strategy-corpus.git .cursor\skills\mzpack-strategies
```

</TabItem>
</Tabs>

## First Step

After installation, open your agent and give it this task:

```text
add a delta divergence signal to this strategy, following AGENTS.md
```

## What Is Included

| Path | Contents |
| --- | --- |
| `AGENTS.md` | Start here. How an MZpack strategy is put together: host, algo class, signals, the signal tree, entries, risk, the signal probe, build, and deploy. |
| `docs/api-surface.md` | Types, members, and enums for `MZpack.NT8.Algo` in one place. |
| `docs/pitfalls.md` | Reasons code can compile but do nothing; read this before debugging. |
| `docs/catalog.md` | Which sample to open for a given pattern. |
| `samples/` | 16 worked examples, one technique per example, each with a README. |
| `templates/` | Three buildable templates: plain strategy, Pattern Dashboard, and Control Panel. |
| `Directory.Build.props` | Central paths to NinjaTrader and MZpack; edit once or set environment variables. |

<details>
<summary>Build and Configuration</summary>

MSBuild is required. It is already on `PATH` in Developer PowerShell for Visual Studio:

```powershell
msbuild templates\StrategyTemplate\StrategyTemplate.csproj
```

- Build the template, not the corpus root: `samples/` is intentionally not part of a project, and there is nothing to build at the root.
- Close NinjaTrader before building. Otherwise it holds assemblies in `bin\Custom`, and a successful build will not add the strategy to the list.
- For a standard installation, `Directory.Build.props` already contains the required paths. For custom paths, edit that file or set `NINJATRADER_INSTALL`, `NINJATRADER_USER`, and `MZPACK_DLL` as environment variables, then restart your shell or Visual Studio.

</details>

## Links

- [Fixed-release source](https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/tree/skill-v1.0.2)
- [Fixed-release ZIP](https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/archive/refs/tags/skill-v1.0.2.zip)
