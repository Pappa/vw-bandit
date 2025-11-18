import pandas as pd
import argparse
from bandit.utils.processing import generate_vw_input, generate_vw_actions
from bandit.train import train_bandit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shared_features", type=str, required=False)
    parser.add_argument("--country_code", type=str, required=True)
    args = parser.parse_args()

    user_feedback = (
        pd.read_csv("./data/user_feedback.csv")
        .sort_values(by="timestamp")
        .reset_index(drop=True)
    )
    model_features = pd.read_csv("./data/model_features.csv")
    user_feedback = user_feedback[user_feedback["country_code"] == args.country_code]
    model_features = model_features[model_features["country_code"] == args.country_code]
    shared_features = args.shared_features.split(",") if args.shared_features else None
    training_data = generate_vw_input(user_feedback, model_features, shared_features)

    model = train_bandit(training_data)

    actions = generate_vw_actions(model_features.to_dict(orient="records"))
    predict_input = "shared |user user_id=null\n" + "\n".join(actions)
    predictions = model.predict(predict_input)
    model_predictions = model_features.copy()[
        ["country_code", "variant_id", "model_type", "version", "model_id"]
    ]
    model_predictions["prediction"] = predictions
    print("sum of predictions:", model_predictions["prediction"].sum().round(5))
    print(model_predictions.to_string())
