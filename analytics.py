import pandas as pd

def load_data():

    df = pd.read_csv("data/mutual_funds.csv")

    # Keep only Open Ended funds
    df = df[df["Scheme_Type"] == "Open Ended"]

    # Convert numeric columns
    df["NAV"] = pd.to_numeric(df["NAV"], errors="coerce")
    df["Average_AUM_Cr"] = pd.to_numeric(df["Average_AUM_Cr"], errors="coerce")
    df["Scheme_Min_Amt"] = pd.to_numeric(df["Scheme_Min_Amt"], errors="coerce")

    df = df.dropna(subset=["Scheme_Name", "NAV"])

    df = df.reset_index(drop=True)

    return df


def convert_to_documents(df):

    documents = []

    for _, row in df.iterrows():

        doc = (
            f"Scheme Name: {row['Scheme_Name']} | "
            f"AMC: {row['AMC']} | "
            f"Category: {row['Scheme_Category']} | "
            f"Type: {row['Scheme_Type']} | "
            f"NAV: {row['NAV']} | "
            f"AUM (Cr): {row['Average_AUM_Cr']} | "
            f"Minimum Investment: {row['Scheme_Min_Amt']} | "
            f"Launch Date: {row['Launch_Date']}"
        )

        documents.append(doc)

    return documents
