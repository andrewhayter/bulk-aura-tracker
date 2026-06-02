# bulk-aura-tracker

Community tools for tracking BULK Exchange AURA points — Season 1 (2026).

Includes a projection calculator, wallet tracker, and dilution model. No dependencies beyond Python 3.10+.

> Community-maintained. Not affiliated with BULK Exchange. For official info: [docs.bulk.trade](https://docs.bulk.trade)

---

## Tools

| Script | What it does |
|--------|-------------|
| `tools/aura_calculator.py` | Projects your weekly AURA earnings and cumulative total based on confirmed mechanics |
| `tools/dilution_model.py` | Shows how your retro AURA share erodes over the campaign as 1M AURA/week is emitted |

> **What's confirmed vs estimated:** The 1M AURA/week, the pro-rata formula (USDC × time held), the 500K retroactive pool, and the 30% community allocation are all confirmed by BULK. The depositor bucket percentage and total token supply are estimates — BULK has not published these numbers. Token value projections are speculative.

---

## Quick Start

```bash
git clone https://github.com/andrewhayter/bulk-aura-tracker
cd bulk-aura-tracker
python --version  # requires 3.10+
```

No pip installs needed — all tools use the standard library only.

---

## AURA Calculator

Estimates weekly AURA earnings based on your deposit, current TVL, and campaign length.

```bash
# Basic: $1,000 deposit at $8.5M TVL, 12-week campaign
python tools/aura_calculator.py --deposit 1000 --tvl 8500000 --weeks 12

# With 621 retro AURA already banked and 50 referral AURA/week
python tools/aura_calculator.py --deposit 500 --tvl 8500000 --weeks 20 \
  --retro 621 --referral-weekly 50

# Show custom token price scenarios
python tools/aura_calculator.py --deposit 2500 --tvl 8500000 --weeks 16 \
  --token-prices 1 3 5 10 20
```

**Sample output:**

```
================================================================
  BULK Exchange — AURA Projection Calculator
  builtonbulk.xyz/aura-points-guide
================================================================
  Deposit:          $1,000.00 USDC
  Starting TVL:     $8,500,000
  Campaign length:  12 weeks
  TVL growth/week:  20.0%
================================================================

 Wk           TVL   Wkly AURA   Cumul AURA   Pool Share
------------------------------------------------------------
  1      $8.5M          70.6         70.6     0.0069%
  4     $14.6M          41.2        247.2     0.0059%
  8     $25.3M          23.7        407.4     0.0038%
 12     $43.8M          13.7        524.9     0.0027%
```

**Formula used:**

```
weekly_aura = (your_deposit / total_tvl) * 600_000
```

The depositor bucket is approximately 60% of the 1M weekly total. TVL growth is modeled at 20%/week by default — adjust with `--tvl-growth`.

---

## Dilution Model

Shows how your retro AURA share shrinks as 1M AURA/week is emitted into the pool.

```bash
python tools/dilution_model.py --retro 621

# Custom token price range
python tools/dilution_model.py --retro 800 --prices 1 3 5 10 20
```

**Sample output:**

```
================================================================
  BULK Exchange — AURA Dilution Model
================================================================
  Your retro AURA:  621
  Retro pool total: 500,000
  Weekly emission:  1,000,000
================================================================

  Week    Total pool    Your share     $1     $3     $5    $10
  ─────────────────────────────────────────────────────────────
     0       500,000      0.1242%    $372  $1.1K  $1.9K  $3.7K
     1     1,500,000      0.0414%    $124    $37    $62    $124
     4     4,500,000      0.0138%     $41    $12    $21     $41
    12    12,500,000      0.0050%     $15     $4     $8     $15
    26    26,500,000      0.0023%      $7     $2     $4      $7
```

This is why deposit size matters: every week you hold USDC in the pre-deposit, you add to your AURA and partially offset dilution from new participants.

---

## Season 1 Mechanics Reference

The following are from the official BULK Exchange Season 1 launch announcement (June 1, 2026). The docs.bulk.trade/points and /referral pages were marked "coming soon" as of June 2, 2026.

| Parameter | Value | Source |
|-----------|-------|--------|
| Weekly AURA total | 1,000,000 | Official announcement |
| Distribution formula | USDC deposited × time held | Official announcement |
| First snapshot | Saturday, June 6, 2026 | Official announcement |
| Minimum deposit | $10 USDC | Official announcement |
| Maximum deposit | $5,000,000 per account | Official announcement |
| Withdrawal | Anytime (no lockup) | Official announcement |
| Referral rate | 1 AURA per $100 referred and held | Official announcement |
| Community allocation | 30% of total BULK supply | Official announcement |
| Total token supply | Not published | — |
| AURA-to-token conversion | Not published | — |

**Retroactive categories** (June 1, 2026 snapshot — closed):

| Category | What qualified |
|----------|---------------|
| `retro_roles` | OG / Contributor Discord role |
| `retro_alphanet` | Alphanet testnet participation |
| `retro_testnet` | Paper trading competition |
| `retro_exponent` | BulkSOL held on Exponent Finance |
| `retro_loopscale` | BulkSOL used on Loopscale |
| `retro_bulksol_stake` | Native BulkSOL staking |
| `retro_bulk_validator_stake` | Staked to a BULK validator |
| `retro_p0` | P0 genesis cohort |

---

## Start Earning AURA

Pre-deposits are open at [early.bulk.trade/deposit](https://builtonbulk.xyz/go/bulk-app). Withdrawable anytime.

Full guides at [builtonbulk.xyz](https://builtonbulk.xyz):

- [AURA Points Explained](https://builtonbulk.xyz/aura-points-guide)
- [Airdrop Checklist](https://builtonbulk.xyz/airdrop-checklist)
- [BulkSOL Yield Guide](https://builtonbulk.xyz/bulksol)
- [Loopscale Loop Strategy](https://builtonbulk.xyz/bulksol-loop-strategy)

Swap SOL → BulkSOL: [Titan Exchange](https://titan.exchange/@hittincorners)
Leverage BulkSOL: [Loopscale](https://loop.sl/i/ivL9G)

Referral code: **`yeti`** — use it at [builtonbulk.xyz/go/bulk-app](https://builtonbulk.xyz/go/bulk-app)

---

## Contributing

PRs welcome. If you build something useful (a funding rate tracker, a bot framework, a live dashboard), open a PR or raise an issue.

## License

MIT
