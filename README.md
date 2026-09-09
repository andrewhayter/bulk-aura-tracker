# bulk-aura-tracker

Community tools for analyzing BULK Exchange AURA — **Season 1 (2026), now closed.**

> **Historical (September 2026):** these tools model Season 1's pre-deposit AURA formula (USDC × time held, 1M AURA/week Saturday snapshots), which **closed September 5, 2026 at mainnet launch**. Every pre-deposit converted to trading margin. AURA on mainnet now accrues through **trading volume, BulkSOL holding, and referrals** — the per-volume formula has not been published. The tools below are preserved as a historical reference for the closed campaign; they no longer project live AURA.

Includes a projection calculator, wallet tracker, and dilution model. No dependencies beyond Python 3.10+.

> Community-maintained. Not affiliated with BULK Exchange. For official info: [docs.bulk.trade](https://docs.bulk.trade)

---

## Tools

| Script                     | What it does                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------ |
| `tools/aura_calculator.py` | Projects weekly AURA under Season 1's closed deposit-and-hold formula (historical)   |
| `tools/dilution_model.py`  | Shows how a retro AURA share eroded as 1M AURA/week was emitted in Season 1 (historical) |

> **Historical basis:** The tools run on Season 1's confirmed parameters — 1M AURA/week, pro-rata formula (USDC × time held), 500K retroactive pool, 30% community allocation. All of these were confirmed by BULK for Season 1. Total token supply and AURA-to-token value remain unpublished. Token value projections are speculative.

---

## Quick Start

```bash
git clone https://github.com/andrewhayter/bulk-aura-tracker
cd bulk-aura-tracker
python --version  # requires 3.10+
```

No pip installs needed — all tools use the standard library only.

---

## AURA Calculator (Historical — Season 1, closed Sept 5, 2026)

Models weekly AURA earnings under the closed pre-deposit formula, based on deposit, current TVL, and campaign length.

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
  BULK Exchange — AURA Projection Calculator (Season 1, historical)
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

**Formula used (Season 1):**

```
weekly_aura = (your_deposit / total_tvl) * 600_000
```

The depositor bucket was approximately 60% of the 1M weekly total. TVL growth is modeled at 20%/week by default — adjust with `--tvl-growth`. This formula closed with Season 1 at mainnet launch.

---

## Dilution Model (Historical — Season 1, closed Sept 5, 2026)

Shows how a retro AURA share shrank as 1M AURA/week was emitted into the Season 1 pool.

```bash
python tools/dilution_model.py --retro 621

# Custom token price range
python tools/dilution_model.py --retro 800 --prices 1 3 5 10 20
```

**Sample output:**

```
================================================================
  BULK Exchange — AURA Dilution Model (Season 1, historical)
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

This is why deposit size mattered in Season 1: every week USDC was held in the pre-deposit, it added to AURA and partially offset dilution from new participants. That deposit lane is now closed.

---

## Season 1 Mechanics Reference (Historical — campaign closed Sept 5, 2026)

The following were from the official BULK Exchange Season 1 launch announcement (June 1, 2026). The docs.bulk.trade/points and /referral pages were marked "coming soon" as of June 2, 2026.

| Parameter                | Value                             | Source                |
| ------------------------ | --------------------------------- | --------------------- |
| Weekly AURA total        | 1,000,000                         | Official announcement |
| Distribution formula     | USDC deposited × time held        | Official announcement |
| First snapshot           | Saturday, June 6, 2026            | Official announcement |
| Minimum deposit          | $10 USDC                          | Official announcement |
| Maximum deposit          | $5,000,000 per account            | Official announcement |
| Withdrawal               | Anytime (no lockup)               | Official announcement |
| Referral rate            | 1 AURA per $100 referred and held | Official announcement |
| Community allocation     | 30% of total BULK supply          | Official announcement |
| Total token supply       | Not published                     | —                     |
| AURA-to-token conversion | Not published                     | —                     |

**Retroactive categories** (June 1, 2026 snapshot — closed):

| Category                     | What qualified                   |
| ---------------------------- | -------------------------------- |
| `retro_roles`                | OG / Contributor Discord role    |
| `retro_alphanet`             | Alphanet testnet participation   |
| `retro_testnet`              | Paper trading competition        |
| `retro_exponent`             | BulkSOL held on Exponent Finance |
| `retro_loopscale`            | BulkSOL used on Loopscale        |
| `retro_bulksol_stake`        | Native BulkSOL staking           |
| `retro_bulk_validator_stake` | Staked to a BULK validator       |
| `retro_p0`                   | P0 genesis cohort                |

**What replaced this at mainnet (Sept 5, 2026):** AURA now accrues through mainnet trading volume (primary), BulkSOL holding, and referrals (dedicated pool as referred accounts trade). The exact per-volume formula has not been published. Pre-deposit access codes were replaced by mainnet access via referral link + weekly access code.

---

## Earn AURA Now (Mainnet)

Mainnet is live at [app.bulk.trade/ref/YETI](https://app.bulk.trade/ref/YETI). Invite-only: referral link plus a weekly access code. Free codes: [builtonbulk.xyz/bulk-access-codes](https://builtonbulk.xyz/bulk-access-codes). Trading volume earns AURA and access codes (1 per $1M, weekly reset) — start on a liquid pair like [BTC-USD](https://app.bulk.trade/trade/BTC-USD?ref=YETI) or [SOL-USD](https://app.bulk.trade/trade/SOL-USD?ref=YETI).

Full guides at [builtonbulk.xyz](https://builtonbulk.xyz):

- [AURA Points Explained](https://builtonbulk.xyz/aura-points-guide)
- [Airdrop Checklist](https://builtonbulk.xyz/airdrop-checklist)
- [BulkSOL Yield Guide](https://builtonbulk.xyz/bulksol)
- [Loopscale Loop Strategy](https://builtonbulk.xyz/bulksol-loop-strategy)

Swap SOL → BulkSOL: [Titan Exchange](https://titan.exchange/@hittincorners)
Leverage BulkSOL: [Loopscale](https://loop.sl/i/ivL9G)

Referral code: **`YETI`** — use it at [app.bulk.trade/ref/YETI](https://app.bulk.trade/ref/YETI)

---

## Related Repos

| Resource | URL |
|----------|-----|
| Mainnet airdrop / AURA checklist | [github.com/andrewhayter/bulk-airdrop-guide](https://github.com/andrewhayter/bulk-airdrop-guide) |
| Developer docs + TypeScript SDK | [github.com/andrewhayter/bulk-exchange-docs](https://github.com/andrewhayter/bulk-exchange-docs) |

---

## Contributing

PRs welcome. If you build something useful for mainnet (a funding rate tracker, a volume/AURA tracker, a bot framework), open a PR or raise an issue.

## License

MIT

_Last updated: September 8, 2026 — Season 1 tools marked historical; mainnet mechanics noted._

