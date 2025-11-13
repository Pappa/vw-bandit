import pandas as pd

def generate_vw_input(user_feedback: pd.DataFrame, model_features: pd.DataFrame, shared_features: list[str] | None=None) -> str:
    user_features = shared_features or ["user_id"]
    output = []
    for row in user_feedback.itertuples():
        user_id = row.user_id
        model_id = row.model_id
        feedback = row.feedback
        shared = "shared |user " + " ".join([f"{k}={str(getattr(row, k))}" for k in user_features])
        output.append(shared)

        models = model_features.to_dict(orient="records")

        for idx, model in enumerate(models):
            label = ""
            if model["model_id"] == model_id:
                label = f"{idx}:{round(1.0 - float(feedback), 1)}:{round(float(feedback), 1)} "
            action = f"{label}|action {' '.join([f'{k}={str(v).replace(" ", "-")}' for k, v in model.items()])}"
            output.append(action)

        output.append("")
    return "\n".join(output)
