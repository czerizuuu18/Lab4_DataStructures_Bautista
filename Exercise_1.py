# ============================================================
# APPENDIX EXERCISE 1
# ENGINEERING TEST DATA ORGANIZER
# ============================================================

from importlib import import_module

try:
    pd = import_module("pandas")
except ModuleNotFoundError as exc:
    if exc.name != "pandas":
        raise
    raise SystemExit(
        "pandas is required. Install it in the active Python environment "
        "with: python -m pip install pandas"
    ) from exc

# ------------------------------------------------------------
# STUDENT-SPECIFIC INPUTS
# ------------------------------------------------------------

LAST_NAME = "Bautista"
SEED_NUM = 1271

FAVORITE_ARTIST = input("Enter your FAVORITE_ARTIST: ").strip()

if not FAVORITE_ARTIST:
    raise ValueError("FAVORITE_ARTIST cannot be empty.")

# Character-position calculation
artist_code = sum(
    (i + 1) * ord(ch)
    for i, ch in enumerate(FAVORITE_ARTIST)
)

print("\n==============================================")
print("STUDENT-SPECIFIC INPUTS")
print("==============================================")
print("LAST_NAME:", LAST_NAME)
print("SEED_NUM:", SEED_NUM)
print("FAVORITE_ARTIST:", FAVORITE_ARTIST)
print("Artist character-position code:", artist_code)


# ------------------------------------------------------------
# DATA GENERATION
# ------------------------------------------------------------

CATEGORIES = [
    "TEMPERATURE",
    "VOLTAGE",
    "CURRENT",
    "PRESSURE",
    "SPEED"
]

SOURCES = [
    f"{LAST_NAME}_T{i}"
    for i in range(1, 6)
]


def measurement_value(seed, artist_code, source_no, category_no, repeat_no=0):
    raw = (
        seed
        + artist_code
        + source_no * 37
        + category_no * 53
        + repeat_no * 17
    )

    return round((raw % 9000) / 100 + 10, 2)


records = []


# Generate one measurement for every source/category
for source_no, source in enumerate(SOURCES, start=1):

    for category_no, category in enumerate(CATEGORIES, start=1):

        records.append({
            "Test Source": source,
            "Measurement Category": category,
            "Measurement Value": measurement_value(
                SEED_NUM,
                artist_code,
                source_no,
                category_no
            )
        })


# ------------------------------------------------------------
# REQUIRED REPEATED RECORD
# ------------------------------------------------------------

records.append({
    "Test Source": SOURCES[0],
    "Measurement Category": CATEGORIES[0],
    "Measurement Value": measurement_value(
        SEED_NUM,
        artist_code,
        1,
        1,
        1
    )
})


# ------------------------------------------------------------
# REQUIRED MULTIPLE MEASUREMENTS
# ------------------------------------------------------------

for repeat_no in [1, 2]:

    records.append({
        "Test Source": SOURCES[1],
        "Measurement Category": "VOLTAGE",
        "Measurement Value": measurement_value(
            SEED_NUM,
            artist_code,
            2,
            2,
            repeat_no
        )
    })

    records.append({
        "Test Source": SOURCES[2],
        "Measurement Category": "CURRENT",
        "Measurement Value": measurement_value(
            SEED_NUM,
            artist_code,
            3,
            3,
            repeat_no
        )
    })


generated_df = pd.DataFrame(records)


# ------------------------------------------------------------
# 1. GENERATED TEST DATA
# ------------------------------------------------------------

print("\n==============================================")
print("1. GENERATED TEST DATA")
print("==============================================")

print(generated_df.to_string(index=False))


# ------------------------------------------------------------
# 2. ORGANIZED TEST DATA
# ------------------------------------------------------------

organized_df = generated_df.sort_values(
    [
        "Test Source",
        "Measurement Category",
        "Measurement Value"
    ]
).reset_index(drop=True)

print("\n==============================================")
print("2. ORGANIZED TEST DATA")
print("==============================================")

print(organized_df.to_string(index=False))


# ------------------------------------------------------------
# 3. REPEATED / DISTINCT DATA
# ------------------------------------------------------------

key_columns = [
    "Test Source",
    "Measurement Category"
]

duplicate_mask = generated_df.duplicated(
    subset=key_columns,
    keep=False
)

repeated_df = generated_df[
    duplicate_mask
].sort_values(key_columns)

distinct_df = generated_df.drop_duplicates(
    subset=key_columns,
    keep="first"
).sort_values(key_columns)

print("\n==============================================")
print("3. REPEATED / DISTINCT DATA")
print("==============================================")

print("\nRepeated source/category records:")
print(repeated_df.to_string(index=False))

print("\nDistinct source/category records:")
print(distinct_df.to_string(index=False))


# ------------------------------------------------------------
# 4. NUMERICAL AND CATEGORICAL SUMMARIES
# ------------------------------------------------------------

categorical_summary = (
    generated_df
    .groupby("Measurement Category")
    .agg(
        Records=("Measurement Value", "count"),
        Average=("Measurement Value", "mean"),
        Minimum=("Measurement Value", "min"),
        Maximum=("Measurement Value", "max")
    )
    .round(2)
)

source_summary = (
    generated_df
    .groupby("Test Source")
    .agg(
        Records=("Measurement Value", "count"),
        Average=("Measurement Value", "mean"),
        Minimum=("Measurement Value", "min"),
        Maximum=("Measurement Value", "max")
    )
    .round(2)
)

print("\n==============================================")
print("4. NUMERICAL AND CATEGORICAL SUMMARIES")
print("==============================================")

print("\nSummary by measurement category:")
print(categorical_summary.to_string())

print("\nSummary by test source:")
print(source_summary.to_string())


# ------------------------------------------------------------
# 5. PROCESSED RESULTS
# ------------------------------------------------------------

processed_df = (
    generated_df
    .groupby(
        [
            "Test Source",
            "Measurement Category"
        ],
        as_index=False
    )
    .agg(
        Measurement_Count=("Measurement Value", "count"),
        Average_Value=("Measurement Value", "mean"),
        Minimum_Value=("Measurement Value", "min"),
        Maximum_Value=("Measurement Value", "max")
    )
    .round(2)
)

print("\n==============================================")
print("5. PROCESSED RESULTS")
print("==============================================")

print(processed_df.to_string(index=False))


# ------------------------------------------------------------
# 6. ORDERED RESULTS
# ------------------------------------------------------------

ordered_df = processed_df.sort_values(
    [
        "Measurement Category",
        "Average_Value"
    ],
    ascending=[
        True,
        False
    ]
).reset_index(drop=True)

print("\n==============================================")
print("6. ORDERED RESULTS")
print("==============================================")

print(ordered_df.to_string(index=False))


# ------------------------------------------------------------
# 7. FINAL SUMMARY
# ------------------------------------------------------------

overall_average = generated_df[
    "Measurement Value"
].mean()

highest_row = generated_df.loc[
    generated_df["Measurement Value"].idxmax()
]

lowest_row = generated_df.loc[
    generated_df["Measurement Value"].idxmin()
]

print("\n==============================================")
print("7. FINAL ENGINEERING TEST DATA SUMMARY")
print("==============================================")

print("Total records:", len(generated_df))

print(
    "Distinct source/category combinations:",
    len(distinct_df)
)

print(
    "Repeated source/category records:",
    len(repeated_df)
)

print(
    "Overall average:",
    round(overall_average, 2)
)

print(
    "Highest measurement:",
    highest_row["Measurement Value"],
    "from",
    highest_row["Test Source"],
    "-",
    highest_row["Measurement Category"]
)

print(
    "Lowest measurement:",
    lowest_row["Measurement Value"],
    "from",
    lowest_row["Test Source"],
    "-",
    lowest_row["Measurement Category"]
)

print("\nFinal ordered results:")
print(ordered_df.to_string(index=False))

print("\n==============================================")
print("EXERCISE 1 COMPLETED")
print("==============================================")