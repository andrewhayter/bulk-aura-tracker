#!/usr/bin/env python3
"""
BULK Exchange — AURA Points Calculator (Season 1, HISTORICAL)

HISTORICAL TOOL: models Season 1's pre-deposit AURA formula, which CLOSED
September 5, 2026 at BULK mainnet launch. Every pre-deposit converted to
trading margin. AURA on mainnet now accrues through trading volume, BulkSOL
holding, and referrals (exact per-volume formula not yet published). This
tool is preserved as a historical reference for the closed campaign only.

Season 1 CONFIRMED mechanics (from official BULK announcements, now closed):
  - 1,000,000 AURA distributed every week (June 6 - Sept 5, 2026)
  - Formula: USDC deposited x time held (pro-rata share of total TVL)
  - Depositors received the "majority" of weekly AURA
  - Referrers, BulkSOL stakers/holders received the remainder
  - 30% of total BULK token supply allocated to community

ESTIMATED (not published by BULK team):
  - Exact depositor/referral/staker bucket split (defaulting to 70% depositors)
  - Total token supply (unknown — 1B is a placeholder assumption)
  - TVL growth rate

Token allocation projections are speculative. TGE conversion formula not published.
Not financial advice.

More info: https://builtonbulk.xyz/aura-points-guide
"""

import argparse
import sys


WEEKLY_AURA_TOTAL = 1_000_000   # CONFIRMED

# ESTIMATED — BULK says depositors get the "majority". Exact split not published.
DEPOSITOR_BUCKET_PCT = 0.70
DEPOSITOR_BUCKET = WEEKLY_AURA_TOTAL * DEPOSITOR_BUCKET_PCT

# ESTIMATED — total supply not confirmed. Used only for token projection output.
TOTAL_TOKEN_SUPPLY = 1_000_000_000
COMMUNITY_ALLOCATION_PCT = 0.30   # CONFIRMED (30% community allocation)
COMMUNITY_TOKENS = TOTAL_TOKEN_SUPPLY * COMMUNITY_ALLOCATION_PCT

RETRO_POOL = 500_000              # one-time retroactive AURA already distributed


def calc_weekly_aura(deposit: float, tvl: float) -> float:
    if tvl <= 0:
        return 0.0
    return (deposit / tvl) * DEPOSITOR_BUCKET


def project_campaign(
    deposit: float,
    initial_tvl: float,
    weeks: int,
    tvl_growth_pct: float,
    retro_aura: float = 0.0,
    referral_aura_per_week: float = 0.0,
) -> list[dict]:
    rows = []
    tvl = initial_tvl
    cumulative = retro_aura

    for week in range(1, weeks + 1):
        weekly = calc_weekly_aura(deposit, tvl) + referral_aura_per_week
        cumulative += weekly
        total_aura_ever = RETRO_POOL + (WEEKLY_AURA_TOTAL * week)
        share_pct = (cumulative / total_aura_ever) * 100
        rows.append({
            "week": week,
            "tvl": tvl,
            "weekly_aura": weekly,
            "cumulative_aura": cumulative,
            "total_pool": total_aura_ever,
            "share_pct": share_pct,
        })
        tvl *= (1 + tvl_growth_pct / 100)

    return rows


def token_value(aura: float, total_aura_at_tge: float, token_price: float) -> float:
    if total_aura_at_tge <= 0:
        return 0.0
    share = aura / total_aura_at_tge
    tokens = share * COMMUNITY_TOKENS
    return tokens * token_price


def format_usd(v: float) -> str:
    if v >= 1_000_000:
        return f"${v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"${v/1_000:.1f}K"
    return f"${v:.2f}"


def main():
    parser = argparse.ArgumentParser(
        description="BULK Exchange AURA Points Projection Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic: $1,000 deposit, $8.5M TVL, 12 weeks
  python aura_calculator.py --deposit 1000 --tvl 8500000 --weeks 12

  # With retro AURA and referral income
  python aura_calculator.py --deposit 500 --tvl 8500000 --weeks 20 \\
    --retro 621 --referral-weekly 50

  # Show token value at different prices
  python aura_calculator.py --deposit 2500 --tvl 8500000 --weeks 16 \\
    --token-prices 1 3 5 10

  # Compare TVL growth scenarios
  python aura_calculator.py --deposit 1000 --tvl 8500000 --weeks 12 \\
    --tvl-growth 15
        """,
    )
    parser.add_argument("--deposit", type=float, required=True,
                        help="Your USDC deposit amount")
    parser.add_argument("--tvl", type=float, default=8_500_000,
                        help="Current total TVL in USD (default: 8500000)")
    parser.add_argument("--weeks", type=int, default=16,
                        help="Campaign length in weeks (default: 16)")
    parser.add_argument("--tvl-growth", type=float, default=20.0,
                        help="TVL growth percent per week (default: 20%%)")
    parser.add_argument("--retro", type=float, default=0.0,
                        help="Your retroactive AURA already banked (default: 0)")
    parser.add_argument("--referral-weekly", type=float, default=0.0,
                        help="Estimated AURA earned per week from referrals (default: 0)")
    parser.add_argument("--token-prices", type=float, nargs="+", default=[1, 3, 5, 10],
                        help="Token prices to show estimated value at TGE (default: 1 3 5 10)")
    parser.add_argument("--show-all-weeks", action="store_true",
                        help="Print every week (default: show summary milestones only)")

    args = parser.parse_args()

    print()
    print("=" * 64)
    print("  BULK Exchange — AURA Projection Calculator")
    print("  builtonbulk.xyz/aura-points-guide")
    print("=" * 64)
    print(f"  Deposit:          ${args.deposit:,.2f} USDC")
    print(f"  Starting TVL:     ${args.tvl:,.0f}")
    print(f"  Campaign length:  {args.weeks} weeks")
    print(f"  TVL growth/week:  {args.tvl_growth}%")
    print(f"  Retro AURA:       {args.retro:,.0f}")
    print(f"  Referral AURA/wk: {args.referral_weekly:,.1f}")
    print("=" * 64)
    print()

    rows = project_campaign(
        deposit=args.deposit,
        initial_tvl=args.tvl,
        weeks=args.weeks,
        tvl_growth_pct=args.tvl_growth,
        retro_aura=args.retro,
        referral_aura_per_week=args.referral_weekly,
    )

    # week-by-week table
    milestones = {1, 4, 8, 12, args.weeks}
    print(f"{'Wk':>3}  {'TVL':>12}  {'Wkly AURA':>10}  {'Cumul AURA':>12}  {'Pool Share':>10}")
    print("-" * 60)
    for r in rows:
        if args.show_all_weeks or r["week"] in milestones:
            tvl_str = f"${r['tvl']/1_000_000:.1f}M"
            print(
                f"{r['week']:>3}  {tvl_str:>12}  {r['weekly_aura']:>10.1f}  "
                f"{r['cumulative_aura']:>12.1f}  {r['share_pct']:>9.4f}%"
            )
    print()

    final = rows[-1]
    total_aura_at_tge = final["total_pool"]
    final_aura = final["cumulative_aura"]

    print("=" * 64)
    print("  PROJECTED TGE ALLOCATION")
    print("=" * 64)
    print(f"  Your AURA at TGE:     {final_aura:,.0f}")
    print(f"  Total AURA pool:      {total_aura_at_tge:,.0f}")
    print(f"  Your pool share:      {final['share_pct']:.4f}%")
    tokens = (final_aura / total_aura_at_tge) * COMMUNITY_TOKENS
    print(f"  Estimated tokens:     {tokens:,.0f} BULK")
    print()
    print(f"  {'Token Price':>12}  {'Estimated Value':>16}")
    print("  " + "-" * 32)
    for price in args.token_prices:
        val = tokens * price
        print(f"  ${price:>10.2f}  {format_usd(val):>16}")
    print()
    print("  IMPORTANT: Token projections are estimates only.")
    print("  Total supply and TGE conversion formula are not published.")
    print("  Depositor bucket % (70%) is estimated — BULK says 'majority'.")
    print("  30% community allocation is confirmed by BULK team.")
    print("  Historical (Season 1): pre-deposits closed at mainnet launch Sept 5, 2026.")
    print("  More info: builtonbulk.xyz/aura-points-guide")
    print()

    # Referral scenario
    if args.referral_weekly == 0:
        print("=" * 64)
        print("  REFERRAL UPSIDE (if you drive referrals)")
        print("=" * 64)
        print("  Rule: 1 AURA per $100 referred and held per week")
        ref_scenarios = [
            (1, 500),
            (3, 1000),
            (5, 2500),
            (10, 10000),
        ]
        print(f"  {'Referrals':>10}  {'Avg $':>8}  {'AURA/wk':>9}  {'Over campaign':>14}")
        print("  " + "-" * 48)
        for count, avg_dep in ref_scenarios:
            weekly_ref_aura = (count * avg_dep) / 100
            total_ref_aura = weekly_ref_aura * args.weeks
            print(
                f"  {count:>10}  ${avg_dep:>7,}  {weekly_ref_aura:>9.1f}  "
                f"{total_ref_aura:>14,.0f}"
            )
        print()
        print("  Historical tool — referrals now earn via trading on mainnet.")
        print("  Track it at: builtonbulk.xyz/bulk-referral-program")
        print()


if __name__ == "__main__":
    main()
