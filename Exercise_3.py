# ============================================================
# APPENDIX EXERCISE 3
# TRANSACTION HISTORY ANALYZER
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

CUSTOMERS = [
    f"{LAST_NAME}_C{i}"
    for i in range(1, 6)
]

PRODUCTS = [
    "NOTEBOOK",
    "PEN",
    "USB",
    "HEADPHONES",
    "CALCULATOR"
]


# ------------------------------------------------------------
# FIXED PRODUCT PRICES
# ------------------------------------------------------------

PRICES = {
    "NOTEBOOK": 50.00,
    "PEN": 15.00,
    "USB": 350.00,
    "HEADPHONES": 750.00,
    "CALCULATOR": 450.00
}


# ------------------------------------------------------------
# QUANTITY GENERATION
# ------------------------------------------------------------

def quantity_value(
    seed,
    artist_code,
    customer_no,
    product_no,
    repeat_no=0
):

    raw = (
        seed
        + artist_code
        + customer_no * 17
        + product_no * 31
        + repeat_no * 11
    )

    return 1 + (raw % 5)


# ------------------------------------------------------------
# GENERATE TRANSACTIONS
# ------------------------------------------------------------

records = []


transaction_pairs = [
    (1, 1),
    (1, 2),
    (2, 2),
    (2, 3),
    (3, 3),
    (3, 4),
    (4, 4),
    (4, 5),
    (5, 5),
    (5, 1)
]


for customer_no, product_no in transaction_pairs:

    customer = CUSTOMERS[
        customer_no - 1
    ]

    product = PRODUCTS[
        product_no - 1
    ]

    quantity = quantity_value(
        SEED_NUM,
        artist_code,
        customer_no,
        product_no
    )

    records.append({
        "Customer": customer,
        "Product": product,
        "Quantity": quantity,
        "Unit Price": PRICES[product]
    })


# ------------------------------------------------------------
# REQUIRED REPEATED CUSTOMER-PRODUCT TRANSACTION
# ------------------------------------------------------------

customer_no = 1
product_no = 1

customer = CUSTOMERS[
    customer_no - 1
]

product = PRODUCTS[
    product_no - 1
]

quantity = quantity_value(
    SEED_NUM,
    artist_code,
    customer_no,
    product_no,
    1
)

records.append({
    "Customer": customer,
    "Product": product,
    "Quantity": quantity,
    "Unit Price": PRICES[product]
})


generated_df = pd.DataFrame(records)


# ------------------------------------------------------------
# CALCULATE TRANSACTION VALUE
# ------------------------------------------------------------

generated_df["Transaction Value"] = (
    generated_df["Quantity"]
    * generated_df["Unit Price"]
)


# ------------------------------------------------------------
# 1. GENERATED TRANSACTION RECORDS
# ------------------------------------------------------------

print("\n==============================================")
print("1. GENERATED TRANSACTION RECORDS")
print("==============================================")

print(generated_df.to_string(index=False))


# ------------------------------------------------------------
# 2. ORGANIZED TRANSACTION DATA
# ------------------------------------------------------------

organized_df = generated_df.sort_values(
    [
        "Customer",
        "Product"
    ]
).reset_index(drop=True)

print("\n==============================================")
print("2. ORGANIZED TRANSACTION DATA")
print("==============================================")

print(organized_df.to_string(index=False))


# ------------------------------------------------------------
# 3. REPEATED / DISTINCT TRANSACTIONS
# ------------------------------------------------------------

repeated_df = generated_df[
    generated_df.duplicated(
        subset=["Customer", "Product"],
        keep=False
    )
].sort_values(
    ["Customer", "Product"]
)

distinct_customer_df = generated_df.drop_duplicates(
    "Customer"
)

distinct_product_df = generated_df.drop_duplicates(
    "Product"
)

print("\n==============================================")
print("3. REPEATED / DISTINCT TRANSACTIONS")
print("==============================================")

print("\nRepeated customer-product transactions:")
print(repeated_df.to_string(index=False))

print("\nDistinct customers:")
print(
    distinct_customer_df[
        ["Customer"]
    ].to_string(index=False)
)

print("\nDistinct products:")
print(
    distinct_product_df[
        ["Product"]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 4. TRANSACTION VALUES
# ------------------------------------------------------------

print("\n==============================================")
print("4. TRANSACTION VALUES")
print("==============================================")

print(
    generated_df[
        [
            "Customer",
            "Product",
            "Quantity",
            "Unit Price",
            "Transaction Value"
        ]
    ].to_string(index=False)
)

overall_value = generated_df[
    "Transaction Value"
].sum()

print(
    "\nOverall transaction value: ₱",
    round(overall_value, 2)
)


# ------------------------------------------------------------
# 5. CUSTOMER SUMMARIES
# ------------------------------------------------------------

customer_summary = (
    generated_df
    .groupby("Customer")
    .agg(
        Transactions=("Product", "count"),
        Total_Quantity=("Quantity", "sum"),
        Total_Spending=("Transaction Value", "sum"),
        Average_Transaction=(
            "Transaction Value",
            "mean"
        )
    )
    .round(2)
    .sort_values(
        "Total_Spending",
        ascending=False
    )
)

print("\n==============================================")
print("5. CUSTOMER SUMMARIES")
print("==============================================")

print(customer_summary.to_string())


# ------------------------------------------------------------
# 6. PRODUCT SUMMARIES
# ------------------------------------------------------------

product_summary = (
    generated_df
    .groupby("Product")
    .agg(
        Transactions=("Customer", "count"),
        Total_Quantity=("Quantity", "sum"),
        Total_Sales=("Transaction Value", "sum")
    )
    .round(2)
    .sort_values(
        "Total_Sales",
        ascending=False
    )
)

print("\n==============================================")
print("6. PRODUCT SUMMARIES")
print("==============================================")

print(product_summary.to_string())


# ------------------------------------------------------------
# 7. ORDERED RESULTS
# ------------------------------------------------------------

ordered_df = generated_df.sort_values(
    [
        "Transaction Value",
        "Customer",
        "Product"
    ],
    ascending=[
        False,
        True,
        True
    ]
).reset_index(drop=True)

print("\n==============================================")
print("7. ORDERED RESULTS")
print("==============================================")

print(ordered_df.to_string(index=False))


# ------------------------------------------------------------
# 8. OVERALL TRANSACTION SUMMARY
# ------------------------------------------------------------

top_transaction = generated_df.loc[
    generated_df["Transaction Value"].idxmax()
]

top_customer = customer_summary.index[0]

top_product = product_summary.index[0]


print("\n==============================================")
print("8. FINAL CONSOLIDATED TRANSACTION REPORT")
print("==============================================")

print(
    "Total transaction records:",
    len(generated_df)
)

print(
    "Distinct customers:",
    generated_df["Customer"].nunique()
)

print(
    "Distinct products:",
    generated_df["Product"].nunique()
)

print(
    "Repeated customer-product records:",
    len(repeated_df)
)

print(
    "Overall transaction value: ₱",
    round(overall_value, 2)
)

print(
    "Highest transaction: ₱",
    round(
        top_transaction["Transaction Value"],
        2
    ),
    "-",
    top_transaction["Customer"],
    "-",
    top_transaction["Product"]
)

print(
    "Top customer by spending:",
    top_customer
)

print(
    "Top product by sales value:",
    top_product
)

print("\nCustomer Summary:")
print(customer_summary.to_string())

print("\nProduct Summary:")
print(product_summary.to_string())

print("\nOrdered Results:")
print(ordered_df.to_string(index=False))

print("\n==============================================")
print("EXERCISE 3 COMPLETED")
print("==============================================")