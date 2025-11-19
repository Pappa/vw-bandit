import pandas as pd
import argparse
import json
from bandit.utils.processing import generate_vw_input, generate_vw_actions
from bandit.train import train_bandit
from bandit.utils.data import create_model_features_data, create_user_feedback_data


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
    model_scores = model_features.copy()[
        ["country_code", "variant_id", "model_type", "version", "model_id"]
    ]
    model_scores["score"] = predictions

    # model_scores.to_csv(
    #     f"./data/model_scores_{args.country_code}.csv", index=False
    # )
    print(model_scores.to_string())


def generate_data() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", type=bool, required=False, default=False)
    args = parser.parse_args()
    overwrite = args.overwrite

    with open("./data/sample_data_properties.json", "r") as f:
        properties = json.load(f)

    model_features_df = create_model_features_data(properties)
    user_feedback_df = create_user_feedback_data(properties, model_features_df)

    if overwrite:
        model_features_df.to_csv("./data/model_features.csv", index=False)
        user_feedback_df.to_csv("./data/user_feedback.csv", index=False)
    else:
        print(model_features_df.head(3))
        print(user_feedback_df.head(3))

    print(f"Model features: {model_features_df.shape}")
    print(f"User feedback: {user_feedback_df.shape}")
