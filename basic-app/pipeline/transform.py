import pandas as pd


def transform_claims(df):

    claim_count = df.groupby("ClaimStatus").size().reset_index(name="ClaimCount")
    claim_status_summary = (
        df.groupby("ClaimStatus")
        .agg(
            ClaimCount=("ClaimId", "count"),
            TotalClaimAmount=("ClaimAmount", "sum"),
            AverageClaimAmount=("ClaimAmount", "mean"),
        )
        .reset_index()
    )

    claim_tpa_summary = (
        df.groupby("ClaimTPA")
        .agg(
            ClaimCount=("ClaimId", "count"),
            TotalClaimAmount=("ClaimAmount", "sum"),
            AverageClaimAmount=("ClaimAmount", "mean"),
        )
        .reset_index()
    )

    tpa_status_summary = (
        df.groupby(["ClaimTPA", "ClaimStatus"])
        .agg(
            ClaimCount=("ClaimId", "count"),
            TotalClaimAmount=("ClaimAmount", "sum"),
        )
        .reset_index()
    )

    new_df = df.copy()
    new_df["ClaimMonth"] = pd.to_datetime(df["ClaimDate"])
    new_df["ClaimMonth"] = new_df["ClaimMonth"].dt.to_period("M")

    monthly_summary = (
        new_df.groupby("ClaimMonth")
        .agg(
            ClaimCount=("ClaimId", "count"),
            TotalClaimAmount=("ClaimAmount", "sum"),
            AverageClaimAmount=("ClaimAmount", "mean"),
        )
        .reset_index()
    )

    monthly_status_summary = (
        new_df.groupby(["ClaimMonth", "ClaimStatus"])
        .agg(
            ClaimCount=("ClaimId", "count"),
            TotalClaimAmount=("ClaimAmount", "sum"),
        )
        .reset_index()
    )

    claim_type_summary = (
        df.groupby("ClaimName")
        .agg(
            ClaimCount=("ClaimId", "count"),
            TotalClaimAmount=("ClaimAmount", "sum"),
            AverageClaimAmount=("ClaimAmount", "mean"),
        )
        .reset_index()
    )

    claim_type_status_summary = (
        df.groupby(["ClaimName", "ClaimStatus"])
        .agg(
            ClaimCount=("ClaimId", "count"),
            TotalClaimAmount=("ClaimAmount", "sum"),
            AverageClaimAmount=("ClaimAmount", "mean"),
        )
        .reset_index()
    )

    claim_location_status_summary = (
        df.groupby(["ClaimPlaceOfService", "ClaimStatus"])
        .agg(
            ClaimCount=("ClaimId", "count"),
            TotalClaimAmount=("ClaimAmount", "sum"),
            AverageClaimAmount=("ClaimAmount", "mean"),
        )
        .reset_index()
    )

    return {
        "claim_count": claim_count,
        "claim_status_summary": claim_status_summary,
        "claim_tpa_summary": claim_tpa_summary,
        "tpa_status_summary": tpa_status_summary,
        "monthly_summary": monthly_summary,
        "monthly_status_summary": monthly_status_summary,
        "claim_type_summary": claim_type_summary,
        "claim_type_status_summary": claim_type_status_summary,
        "claim_location_status_summary": claim_location_status_summary,
    }
