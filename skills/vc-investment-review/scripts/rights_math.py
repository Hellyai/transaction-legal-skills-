#!/usr/bin/env python3
"""Deterministic calculations for VC investment-document review.

Calculates only the supplied economic model. It does not determine which
contractual definition, holder, tranche, priority, or remedy applies.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 28


def d(value: object) -> Decimal:
    return Decimal(str(value))


def returns(principal: Decimal, years: list[Decimal], simple_rate: Decimal | None,
            compound_rate: Decimal | None, fixed_multiple: Decimal | None) -> list[dict]:
    rows = []
    for year in years:
        row: dict[str, str] = {"years": str(year)}
        if simple_rate is not None:
            row["simple"] = str(principal * (d(1) + simple_rate * year))
        if compound_rate is not None:
            row["compound"] = str(principal * ((d(1) + compound_rate) ** year))
        if fixed_multiple is not None:
            row["fixed_multiple"] = str(principal * fixed_multiple)
        rows.append(row)
    return rows


def break_even_years(fixed_multiple: Decimal, simple_rate: Decimal) -> Decimal:
    if simple_rate <= 0:
        raise ValueError("simple_rate must be positive")
    return (fixed_multiple - d(1)) / simple_rate


def anti_dilution(mode: str, old_price: Decimal, new_price: Decimal,
                  old_fd_shares: Decimal, new_shares: Decimal,
                  consideration: Decimal | None) -> dict:
    if min(old_price, new_price, old_fd_shares, new_shares) <= 0:
        raise ValueError("prices and share counts must be positive")
    if mode == "full-ratchet":
        adjusted = new_price
        deemed = None
    else:
        cash = consideration if consideration is not None else new_price * new_shares
        deemed = cash / old_price
        adjusted = old_price * (old_fd_shares + deemed) / (old_fd_shares + new_shares)
    return {
        "mode": mode,
        "adjusted_price": str(adjusted),
        "deemed_old_price_shares": None if deemed is None else str(deemed),
    }


def pro_rata(available: Decimal, weights: list[Decimal]) -> list[Decimal]:
    if available < 0 or any(weight < 0 for weight in weights):
        raise ValueError("available amount and weights cannot be negative")
    total = sum(weights, d(0))
    if total == 0:
        raise ValueError("sum of weights must be positive")
    return [available * weight / total for weight in weights]


def liquidation_waterfall(proceeds: Decimal, tranches: list[dict]) -> dict:
    """Model stated claims, priorities and participating ownership.

    Each tranche accepts: name, priority (smaller paid first), claim,
    ownership, participating, and optional cap. Translate the agreement into
    these inputs first and assess conversion elections separately.
    """
    if proceeds < 0:
        raise ValueError("proceeds cannot be negative")
    received = {item["name"]: d(0) for item in tranches}
    remaining = proceeds
    priorities = sorted({int(item.get("priority", 0)) for item in tranches if d(item.get("claim", 0)) > 0})
    for priority in priorities:
        group = [item for item in tranches if int(item.get("priority", 0)) == priority and d(item.get("claim", 0)) > 0]
        claims = [d(item["claim"]) for item in group]
        paid = min(remaining, sum(claims, d(0)))
        for item, amount in zip(group, pro_rata(paid, claims)):
            received[item["name"]] += amount
        remaining -= paid
        if remaining == 0:
            break
    active = [item for item in tranches if bool(item.get("participating", False)) and d(item.get("ownership", 0)) > 0]
    while remaining > 0 and active:
        proposed = pro_rata(remaining, [d(item["ownership"]) for item in active])
        paid_round = d(0)
        next_active = []
        for item, amount in zip(active, proposed):
            cap_raw = item.get("cap")
            if cap_raw is None:
                paid = amount
                next_active.append(item)
            else:
                room = max(d(0), d(cap_raw) - received[item["name"]])
                paid = min(amount, room)
                if room > paid:
                    next_active.append(item)
            received[item["name"]] += paid
            paid_round += paid
        if paid_round == 0:
            break
        remaining -= paid_round
        active = next_active
    return {
        "proceeds": str(proceeds),
        "received": {name: str(amount) for name, amount in received.items()},
        "undistributed": str(remaining),
    }


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    p_returns = sub.add_parser("returns")
    p_returns.add_argument("--principal", required=True)
    p_returns.add_argument("--years", nargs="+", required=True)
    p_returns.add_argument("--simple-rate")
    p_returns.add_argument("--compound-rate")
    p_returns.add_argument("--fixed-multiple")
    p_break = sub.add_parser("break-even")
    p_break.add_argument("--fixed-multiple", required=True)
    p_break.add_argument("--simple-rate", required=True)
    p_anti = sub.add_parser("anti-dilution")
    p_anti.add_argument("--mode", choices=["full-ratchet", "weighted-average"], required=True)
    p_anti.add_argument("--old-price", required=True)
    p_anti.add_argument("--new-price", required=True)
    p_anti.add_argument("--old-fd-shares", required=True)
    p_anti.add_argument("--new-shares", required=True)
    p_anti.add_argument("--consideration")
    p_pro = sub.add_parser("pro-rata")
    p_pro.add_argument("--available", required=True)
    p_pro.add_argument("--weights", nargs="+", required=True)
    p_liq = sub.add_parser("liquidation")
    p_liq.add_argument("--input", required=True, help="UTF-8 JSON file containing proceeds and tranches")
    return root


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "returns":
        result = returns(d(args.principal), [d(value) for value in args.years],
                         None if args.simple_rate is None else d(args.simple_rate),
                         None if args.compound_rate is None else d(args.compound_rate),
                         None if args.fixed_multiple is None else d(args.fixed_multiple))
    elif args.command == "break-even":
        result = {"break_even_years": str(break_even_years(d(args.fixed_multiple), d(args.simple_rate)))}
    elif args.command == "anti-dilution":
        result = anti_dilution(args.mode, d(args.old_price), d(args.new_price), d(args.old_fd_shares),
                               d(args.new_shares), None if args.consideration is None else d(args.consideration))
    elif args.command == "pro-rata":
        result = {"allocations": [str(value) for value in pro_rata(d(args.available), [d(value) for value in args.weights])]}
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = liquidation_waterfall(d(data["proceeds"]), data["tranches"])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
