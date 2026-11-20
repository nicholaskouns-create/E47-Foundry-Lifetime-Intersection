"""Compare input splits while holding the lifetime policy fixed."""

from data_lifetime_algebra import Override, Policy, PolicyKind, condemned, evaluate, view_membership
from intersectionality_validator import build_graph, ts


def main() -> None:
    policy = Policy(PolicyKind.LATEST_VIEW_ONLY, "examples", branches={"main"})
    for live, expired in [(1, 0), (1, 1), (3, 7), (47, 78), (78, 47)]:
        graph = build_graph(live, expired)
        now = ts(2 * (live + expired))
        visible = view_membership(graph, "raw", "main")
        stamped = condemned(evaluate(graph, {"raw": policy}), now)
        override = Override("derived", replacement=None)
        after_override = condemned(evaluate(graph, {"raw": policy}, overrides=[override]), now)

        expected_live = {f"k{i}" for i in range(live)}
        expected_raw = {f"p{i}" for i in range(expired)}
        expected_derived = {f"d{i}" for i in range(expired)}
        if visible != expected_live or stamped != expected_raw | expected_derived:
            raise AssertionError(f"Incorrect view, stamping or inheritance for {live}/{expired}")
        if after_override != expected_raw:
            raise AssertionError(f"Derived override changed the raw stamps for {live}/{expired}")
        print(f"{live} live / {expired} expired: {len(stamped)} condemned, "
              f"{len(after_override)} after derived override")


if __name__ == "__main__":
    main()
