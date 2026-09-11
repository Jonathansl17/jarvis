"""Spanish region names for `avocado_price_regression`, mapped to the
dataset's region strings (city/state names with the spaces removed).
"""

AVOCADO_REGION_ALIASES: dict[str, tuple[str, ...]] = {
    "SanFrancisco": ("san francisco",),
    "LosAngeles": ("los angeles", "los ángeles"),
    "NewYork": ("nueva york",),
    "SanDiego": ("san diego",),
    "Sacramento": ("sacramento",),
    "Seattle": ("seattle",),
    "Portland": ("portland",),
    "Denver": ("denver",),
    "Chicago": ("chicago",),
    "Houston": ("houston",),
    "DallasFtWorth": ("dallas",),
    "Atlanta": ("atlanta",),
    "Orlando": ("orlando",),
    "Tampa": ("tampa",),
    "MiamiFtLauderdale": ("miami",),
    "PhoenixTucson": ("phoenix",),
    "Philadelphia": ("filadelfia", "philadelphia"),
    "Boston": ("boston",),
    "LasVegas": ("las vegas",),
    "California": ("california",),
    "West": ("region oeste", "región oeste"),
    "Southeast": ("region sureste", "región sureste"),
    "Northeast": ("region noreste", "región noreste"),
    "TotalUS": ("todo estados unidos", "estados unidos", "total us"),
}
