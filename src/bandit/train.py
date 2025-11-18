from vowpalwabbit import Workspace


def train_bandit(training_data: list[str]) -> Workspace:
    """
    Trains a Vowpal Wabbit contextual bandit model.

    Args:
        training_data: A list of strings in the VW contextual bandit format.

    Returns:
        The trained Vowpal Wabbit model.
    """
    # Initialize the VW model with the contextual bandit algorithm
    vw_args = "--cb_explore_adf --rnd 3 --epsilon 0.025 --quiet -q UA"
    model = Workspace(vw_args)

    for event in training_data:
        model.learn(event)

    return model
