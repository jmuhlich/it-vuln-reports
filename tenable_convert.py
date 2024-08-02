import pandas as pd
import re
import sys

if len(sys.argv) != 2:
    print(f"Usage: tenable_convert.py input.xlsx")
    sys.exit(1)

df = pd.read_excel(sys.argv[1])
g = pd.merge(
    df.fillna(''),
    df["Plugin Output"]
    .str.extractall(
        r"(?:Path|Installed package)\s*: (?P<Location>.*?)\n.*?Fixed (?:version|package)\s*: (?P<FixedVersion>.*?)$",
        re.MULTILINE | re.DOTALL,
    )
    .reset_index(names=['Index', 'Match']),
    left_index=True,
    right_on='Index',
).groupby(["IP Address", "MAC Address", "DNS Name", "NetBIOS Name", "Location", "FixedVersion"])[
    ["Plugin", "Plugin Name", "Severity"]
]
out = (
    g.apply(
        lambda x: "\n".join(
            f"{r.Plugin} : {r._2}; Severity={r.Severity}"
            for r in x.itertuples()
        )
    )
    .rename("Plugins")
    .reset_index()
)
print(out.to_csv(index=False))
