#!/usr/bin/env python3
"""
BULK Exchange — AURA Dilution Model
Shows how your retro AURA share shrinks over time as weekly emissions accumulate.

CONFIRMED mechanics:
  - 500,000 AURA retroactively distributed on June 1, 2026 (one-time)
  - 1,000,000 AURA emitted every week from June 6, 2026
  - 30% of total BULK token supply allocated to community

ESTIMATED (not published):
  - Total token supply (1B is a placeholder — actual supply unknown)
  - AURA-to-token conversion formula at TGE

Token value columns are speculative. Use them for relative comparison only.
More info: https://builtonbulk.xyz/bulk-aura-dilution-calculator
"""

import argparse


RETRO_POOL = 500_000
WEEKLY_EMISSIONS = 1_000_000
COMMUNITY_TOKENS = 300_000_000  # 30% of 1B assumed supply


def run_model(retro_aura: float, token_prices: list[float]):
    total = RETRO_POOL + retro_aura  # week 0 cumulative

    print()
    print("=" * 72)
    print("  BULK Exchange — AURA Dilution Model")
    print("  Your retro AURA share over time as weekly emissions compound")
    print("  builtonbulk.xyz/bulk-aura-dilution-calculator")
    print("=" * 72)
    print(f"  Your retro AURA:  {retro_aura:,.0f}")
    print(f"  Retro pool total: {RETRO_POOL:,}")
    print(f"  Weekly emission:  {WEEKLY_EMISSIONS:,}")
    print("=" * 72)
    print()

    price_headers = "".join(f"  ${p:>6.0f}" for p in token_prices)
    print(f"  {'Week':>4}  {'Total pool':>12}  {'Your share':>11}{price_headers}")
    print("  " + "-" * (42 + len(token_prices) * 10))

    milestones = [0, 1, 2, 4, 8, 12, 16, 20, 26, 36, 52]

    for week in milestones:
        pool = RETRO_POOL + (WEEKLY_EMISSIONS * week)
        share_pct = (retro_aura / pool) * 100
        tokens = (retro_aura / pool) * COMMUNITY_TOKENS
        price_vals = "".join(f"  {_fmt(tokens * p):>8}" for p in token_prices)
        print(f"  {week:>4}  {pool:>12,.0f}  {share_pct:>10.4f}%{price_vals}")

    print()
    print("  HOW TO READ THIS:")
    print("  Your retro AURA is fixed. Every week, 1M more AURA is minted.")
    print("  Your % of the total pool shrinks — even if you do nothing.")
    print("  Depositing USDC adds to your AURA and partially offsets dilution.")
    print()
    print("  START EARNING: https://builtonbulk.xyz/go/bulk-app (ref: yeti)")
    print()

    # break-even analysis: how much USDC needed to maintain current % share
    print("  DEPOSIT TO OFFSET DILUTION (maintain week-0 share)")
    print("  ─────────────────────────────────────────────────────")
    initial_share = retro_aura / RETRO_POOL
    print(f"  Your initial share: {initial_share:.4%}")
    print()

    tvl_scenarios = [8_500_000, 15_000_000, 30_000_000]
    deposit_bucket_pct = 0.60

    for tvl in tvl_scenarios:
        # weekly AURA to stay proportional: initial_share * 1M
        needed_weekly = initial_share * WEEKLY_EMISSIONS
        # your deposit / tvl * 600k = needed_weekly
        needed_deposit = (needed_weekly / (WEEKLY_EMISSIONS * deposit_bucket_pct)) * tvl
        print(f"  At ${tvl/1_000_000:.0f}M TVL: deposit ~${needed_deposit:,.0f} to hold pace")

    print()
    print("  NOTE: These are estimates. AURA-to-BULK conversion at TGE unconfirmed.")
    print("        30% community allocation is confirmed by BULK team.")
    print()


def _fmt(v: float) -> str:
    if v >= 1_000_000:
        return f"${v/1_000_000:.1f}M"
    if v >= 1_000:
        return f"${v/1_000:.0f}K"
    return f"${v:.0f}"


def main():
    parser = argparse.ArgumentParser(
        description="BULK Exchange AURA dilution model over campaign",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Model dilution for 621 retro AURA
  python dilution_model.py --retro 621

  # Custom token price scenarios
  python dilution_model.py --retro 800 --prices 1 3 5 10 20
        """,
    )
    parser.add_argument("--retro", type=float, required=True,
                        help="Your retroactive AURA from the June 1 snapshot")
    parser.add_argument("--prices", type=float, nargs="+", default=[1, 3, 5, 10],
                        help="Token prices to evaluate at TGE (default: 1 3 5 10)")

    args = parser.parse_args()
    run_model(args.retro, args.prices)


if __name__ == "__main__":
    main()
