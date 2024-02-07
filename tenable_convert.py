import pandas as pd
import re
import sys

if len(sys.argv) != 2:
    print(f"Usage: tenable_convert.py input.xlsx")
    sys.exit(1)

df = pd.read_excel(sys.argv[1])
g = pd.concat(
    [
        df.fillna(""),
        df["Plugin Output"]
        .str.extractall(r"Path\s*: (?P<Path>.*)$", re.MULTILINE)
        .reset_index(level="match"),
    ],
    axis="columns",
).groupby(["IP Address", "MAC Address", "DNS Name", "NetBIOS Name", "Path"])[
    ["Plugin", "Plugin Name", "Family", "Severity"]
]
out = (
    g.apply(
        lambda x: "\n".join(
            f"{r.Plugin} : {r._2}; Family={r.Family}; Severity={r.Severity}"
            for r in x.itertuples()
        )
    )
    .rename("Plugins")
    .reset_index()
)
print(out.to_csv(index=False))
