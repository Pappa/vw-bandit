import pandas as pd


def generate_vw_input(
    user_feedback: pd.DataFrame,
    model_features: pd.DataFrame,
    shared_features: list[str] | None = None,
) -> str:
    user_features = shared_features or ["user_id"]
    output = []
    for row in user_feedback.itertuples():
        feedback = float(row.feedback)
        shared = "shared |user " + " ".join(
            [f"{k}={str(getattr(row, k))}" for k in user_features]
        )
        output.append(shared)

        models = model_features.to_dict(orient="records")

        for idx, model in enumerate(models):
            label = ""
            if model["model_id"] == row.model_id:
                label = f"{idx}:{round(1.0 - feedback, 1)}:{round(feedback, 1)} "
            action_items = [f'{k}={str(v).replace(" ", "-")}' for k, v in model.items()]
            action = f"{label}|action {' '.join(action_items)}"
            output.append(action)

        output.append("")

    return "\n".join(output)
