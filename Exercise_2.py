# ============================================================
# APPENDIX EXERCISE 2
# STUDENT PERFORMANCE DATA ANALYZER
# ============================================================

from importlib import import_module

try:
    pd = import_module("pandas")
except ModuleNotFoundError as error:
    if error.name != "pandas":
        raise
    raise ModuleNotFoundError(
        "This script requires pandas. Install it with 'python -m pip install pandas'."
    ) from error

# ------------------------------------------------------------
# STUDENT-SPECIFIC INPUTS
# ------------------------------------------------------------

LAST_NAME = "Bautista"
SEED_NUM = 1271

FAVORITE_ARTIST = input("Enter your FAVORITE_ARTIST: ").strip()

if not FAVORITE_ARTIST:
    raise ValueError("FAVORITE_ARTIST cannot be empty.")

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
# DATA
# ------------------------------------------------------------

STUDENTS = [
    f"{LAST_NAME}_{i}"
    for i in range(1, 6)
]

SUBJECTS = [
    "PROGRAMMING",
    "MATHEMATICS",
    "ELECTRONICS",
    "PHYSICS",
    "ENGLISH"
]


# ------------------------------------------------------------
# SCORE GENERATION
# ------------------------------------------------------------

def score_value(
    seed,
    artist_code,
    student_no,
    subject_no,
    repeat_no=0
):

    raw = (
        seed
        + artist_code
        + student_no * 29
        + subject_no * 41
        + repeat_no * 13
    )

    return 60 + (raw % 41)


# ------------------------------------------------------------
# PERFORMANCE CATEGORY
# ------------------------------------------------------------

def performance_category(score):

    if score >= 90:
        return "EXCELLENT"

    elif score >= 80:
        return "VERY GOOD"

    elif score >= 75:
        return "GOOD"

    elif score >= 60:
        return "FAIR"

    else:
        return "POOR"


# ------------------------------------------------------------
# GENERATE RECORDS
# ------------------------------------------------------------

records = []

for student_no, student in enumerate(STUDENTS, start=1):

    for subject_no, subject in enumerate(SUBJECTS, start=1):

        score = score_value(
            SEED_NUM,
            artist_code,
            student_no,
            subject_no
        )

        records.append({
            "Student": student,
            "Subject": subject,
            "Score": score,
            "Performance Category":
                performance_category(score)
        })


# ------------------------------------------------------------
# REQUIRED REPEATED RECORD
# ------------------------------------------------------------

repeated_score = score_value(
    SEED_NUM,
    artist_code,
    1,
    1,
    1
)

records.append({
    "Student": STUDENTS[0],
    "Subject": SUBJECTS[0],
    "Score": repeated_score,
    "Performance Category":
        performance_category(repeated_score)
})


# ------------------------------------------------------------
# REQUIRED INCOMPLETE RECORD
# ------------------------------------------------------------

records.append({
    "Student": STUDENTS[4],
    "Subject": SUBJECTS[4],
    "Score": None,
    "Performance Category": "INCOMPLETE"
})


generated_df = pd.DataFrame(records)


# ------------------------------------------------------------
# 1. GENERATED PERFORMANCE RECORDS
# ------------------------------------------------------------

print("\n==============================================")
print("1. GENERATED PERFORMANCE RECORDS")
print("==============================================")

print(generated_df.to_string(index=False))


# ------------------------------------------------------------
# 2. ORGANIZED STUDENT/SUBJECT DATA
# ------------------------------------------------------------

organized_df = generated_df.sort_values(
    [
        "Student",
        "Subject"
    ]
).reset_index(drop=True)

print("\n==============================================")
print("2. ORGANIZED STUDENT/SUBJECT DATA")
print("==============================================")

print(organized_df.to_string(index=False))


# ------------------------------------------------------------
# 3. REPEATED / INCOMPLETE RECORDS
# ------------------------------------------------------------

repeated_df = generated_df[
    generated_df.duplicated(
        subset=["Student", "Subject"],
        keep=False
    )
].sort_values(
    ["Student", "Subject"]
)

incomplete_df = generated_df[
    generated_df["Score"].isna()
]

print("\n==============================================")
print("3. REPEATED / INCOMPLETE RECORDS")
print("==============================================")

print("\nRepeated student-subject records:")
print(repeated_df.to_string(index=False))

print("\nIncomplete records:")
print(incomplete_df.to_string(index=False))


# ------------------------------------------------------------
# 4. PERFORMANCE CATEGORIES
# ------------------------------------------------------------

valid_df = generated_df.dropna(
    subset=["Score"]
).copy()

category_summary = (
    valid_df["Performance Category"]
    .value_counts()
    .rename_axis("Performance Category")
    .reset_index(
        name="Number of Records"
    )
)

print("\n==============================================")
print("4. PERFORMANCE CATEGORIES")
print("==============================================")

print(category_summary.to_string(index=False))


# ------------------------------------------------------------
# 5. STUDENT AND SUBJECT SUMMARIES
# ------------------------------------------------------------

student_summary = (
    valid_df
    .groupby("Student")
    .agg(
        Records=("Score", "count"),
        Average_Score=("Score", "mean"),
        Highest_Score=("Score", "max"),
        Lowest_Score=("Score", "min")
    )
    .round(2)
    .sort_values(
        "Average_Score",
        ascending=False
    )
)

subject_summary = (
    valid_df
    .groupby("Subject")
    .agg(
        Records=("Score", "count"),
        Average_Score=("Score", "mean"),
        Highest_Score=("Score", "max"),
        Lowest_Score=("Score", "min")
    )
    .round(2)
    .sort_values(
        "Average_Score",
        ascending=False
    )
)

print("\n==============================================")
print("5. STUDENT AND SUBJECT SUMMARIES")
print("==============================================")

print("\nStudent Summary:")
print(student_summary.to_string())

print("\nSubject Summary:")
print(subject_summary.to_string())


# ------------------------------------------------------------
# 6. ORDERED RESULTS
# ------------------------------------------------------------

ordered_df = valid_df.sort_values(
    [
        "Score",
        "Student",
        "Subject"
    ],
    ascending=[
        False,
        True,
        True
    ]
).reset_index(drop=True)

print("\n==============================================")
print("6. ORDERED RESULTS")
print("==============================================")

print(ordered_df.to_string(index=False))


# ------------------------------------------------------------
# 7. FINAL STUDENT PERFORMANCE REPORT
# ------------------------------------------------------------

top_record = valid_df.loc[
    valid_df["Score"].idxmax()
]

overall_average = valid_df["Score"].mean()

print("\n==============================================")
print("7. FINAL STUDENT PERFORMANCE REPORT")
print("==============================================")

print(
    "Total generated records:",
    len(generated_df)
)

print(
    "Valid score records:",
    len(valid_df)
)

print(
    "Repeated student-subject records:",
    len(repeated_df)
)

print(
    "Incomplete records:",
    len(incomplete_df)
)

print(
    "Overall average score:",
    round(overall_average, 2)
)

print(
    "Highest score:",
    top_record["Score"],
    "-",
    top_record["Student"],
    "-",
    top_record["Subject"]
)

print("\nStudent Summary:")
print(student_summary.to_string())

print("\nSubject Summary:")
print(subject_summary.to_string())

print("\nOrdered Results:")
print(ordered_df.to_string(index=False))

print("\n==============================================")
print("EXERCISE 2 COMPLETED")
print("==============================================")