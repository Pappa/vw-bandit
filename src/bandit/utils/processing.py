import pandas as pd


def generate_vw_input(
    user_feedback: pd.DataFrame,
    model_features: pd.DataFrame,
    shared_features: list[str] | None = None,
) -> list[str]:
    user_features = shared_features or ["user_id"]
    models = model_features.to_dict(orient="records")
    actions = generate_vw_actions(models)
    events = []

    for row in user_feedback.itertuples():
        event = []
        feedback = float(row.feedback)
        shared = "shared |user " + " ".join(
            [f"{k}={str(getattr(row, k))}" for k in user_features]
        )
        event.append(shared)

        for idx, (model, action) in enumerate(zip(models, actions)):
            label = ""
            if model["model_id"] == row.model_id:
                label = f"{idx}:{round(1.0 - feedback, 1)}:{round(feedback, 1)} "
            action = f"{label}{action}"
            event.append(action)

        events.append("\n".join(event))

    return events


def generate_vw_actions(models: list[dict]) -> list[str]:
    actions = []
    for model in models:
        action_items = [f'{k}={str(v).replace(" ", "-")}' for k, v in model.items()]
        action = f"|action {' '.join(action_items)}"
        actions.append(action)
    return actions
