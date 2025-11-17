from vowpalwabbit import pyvw


def train_bandit(training_data: list[str]) -> pyvw.vw:
    """
    Trains a Vowpal Wabbit contextual bandit model.

    Args:
        training_data: A list of strings in the VW contextual bandit format.

    Returns:
        The trained Vowpal Wabbit model.
    """
    # Initialize the VW model with the contextual bandit algorithm
    # --cb_explore_adf: Contextual Bandit with Action Dependent Features
    # --quiet: Suppress verbose output
    # --epsilon 0.2: Use an epsilon-greedy exploration strategy
    model = pyvw.vw("--cb_explore_adf --quiet --epsilon 0.2 -q UA")

    for event in training_data:
        model.learn(event)

    return model


# def get_bandit_predictions(model: pyvw.vw, context: str, num_actions: int) -> list:
#     """
#     Gets predictions from a trained Vowpal Wabbit model for a given context.

#     Args:
#         model: The trained VW model.
#         context: A string representing the shared context.
#         num_actions: The number of arms.

#     Returns:
#         A list of scores for each action.
#     """
#     # The multiline example format is required for prediction with cb_explore_adf
#     vw_prediction_example = [f"shared {context}"]
#     for i in range(num_actions):
#         vw_prediction_example.append(f"|action variant=variant-{i}")

#     # The predict method returns a list of action indices and their scores
#     predictions = model.predict(vw_prediction_example)
#     return predictions


# # Example Usage (continuing from the previous block)
# num_variants = len(all_model_variants)
# trained_bandit_model = train_bandit(vw_input, num_variants)

# # Example context for which to get new traffic weights
# # In a real scenario, you might average predictions over a sample of recent contexts
# sample_context = "|user user_id=user4 context_feature_1=0.6"
# action_scores = get_bandit_predictions(
#     trained_bandit_model, sample_context, num_variants
# )

# print(f"Action scores: {action_scores}")
