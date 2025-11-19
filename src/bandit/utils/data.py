import random
import uuid
import pandas as pd
from datetime import datetime, timedelta


def create_metrics(factor: float, quality_metrics: list[str]) -> list[float]:
    mae_lower = 4.0 - float(factor)
    other_lower = float(factor)
    other_upper = 10.0 - (4.0 - other_lower)
    mae = round(random.uniform(mae_lower, 10.0) / 10, 5)
    rmse = round(random.uniform(mae_lower + 1.0, 10.0) / 10, 5)
    return [
        mae,
        rmse,
    ] + [
        round(random.uniform(other_lower, other_upper) / 10.0, 5)
        for _ in quality_metrics
    ]


def create_model_features(
    model_name: str,
    country_codes: list[str],
    variant_ids: list[list[str]],
    model_types: list[str],
    versions: list[str],
    quality_metrics: list[str],
) -> list[list[str | float]]:
    model_features = []

    for country_code, variants in zip(country_codes, variant_ids):
        for variant_idx, (variant, model_type) in enumerate(zip(variants, model_types)):
            for version_idx, version in enumerate(versions):
                uid = str(uuid.uuid4()).split("-")[0]
                features = [model_name, country_code, variant, model_type, version, uid]
                metrics = create_metrics((variant_idx + version_idx), quality_metrics)
                model_features.append(features + metrics)
    return model_features


def create_model_features_data(
    properties: dict,
) -> pd.DataFrame:
    error_metrics = properties["metrics"]["error"]
    quality_metrics = properties["metrics"]["quality"]
    all_metrics = error_metrics + quality_metrics

    country_codes = properties["country_codes"]
    model_types = properties["model_types"]
    num_variants = len(model_types)
    num_versions = properties["num_versions"]
    variant_ids = [
        [f"{country_code}{i:04d}" for i in range(1, num_variants + 1)]
        for country_code in country_codes
    ]
    versions = [str(i) for i in range(1, num_versions + 1)]

    model_name = properties["model_name"]
    columns = properties["model_features"] + all_metrics

    model_features = create_model_features(
        model_name, country_codes, variant_ids, model_types, versions, quality_metrics
    )
    return pd.DataFrame(model_features, columns=columns).sort_values(
        ["country_code", "variant_id", "version"]
    )


def create_user_feedback_data(
    properties: dict,
    model_features_df: pd.DataFrame,
) -> pd.DataFrame:
    error_metrics = properties["metrics"]["error"]
    quality_metrics = properties["metrics"]["quality"]
    all_metrics = error_metrics + quality_metrics
    country_codes = properties["country_codes"]
    num_users = properties["num_users"]
    num_requests_per_user = properties["num_requests_per_user"]

    user_ids = [f"U{i:04d}" for i in range(1, num_users + 1)]
    columns = ["user_id", "model_id", "country_code", "timestamp", "feedback"]
    user_feedback = []
    for user_id in user_ids:
        start_time = datetime.now() - timedelta(days=1, hours=6)
        for country_code in country_codes:
            num_requests = random.randint(
                num_requests_per_user[0], num_requests_per_user[1] + 1
            )
            for _ in range(num_requests):
                model = model_features_df[
                    model_features_df["country_code"] == country_code
                ].sample(1)
                model["MAE"] = 1.0 - model["MAE"]
                model["RMSE"] = 1.0 - model["RMSE"]
                model["score"] = model.loc[:, all_metrics].mean(axis=1).round(5)
                model = model[["model_id", "score"]]
                model_props = model.to_dict(orient="records")[0]
                score = model_props["score"]
                feedback = random.choices([0, 1], weights=[1.0 - score, score])[0]
                timestamp = str(start_time).split(".")[0]
                user_response = [
                    user_id,
                    model_props["model_id"],
                    country_code,
                    timestamp,
                    feedback,
                ]
                user_feedback.append(user_response)
                start_time += timedelta(
                    minutes=random.randint(1, 5), seconds=random.randint(0, 59)
                )

    return pd.DataFrame(user_feedback, columns=columns).sort_values(["timestamp"])
