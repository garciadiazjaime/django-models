from django.core.management.base import BaseCommand

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow.keras import layers


def plot_loss(history):
    plt.plot(history.history["loss"], label="loss")
    plt.plot(history.history["val_loss"], label="val_loss")
    plt.ylabel("Loss")
    plt.xlabel("Epoch")
    plt.legend(["train", "test"])
    plt.grid(True)
    plt.show()


def plot_values(train_dataset):
    sns.pairplot(
        train_dataset[
            [
                "twitter_followers",
                "popularity",
            ]
        ],
        diag_kind="kde",
    )
    plt.show()


def plot_xy(x, y, feature, labels):
    plt.scatter(feature, labels, label="Data")
    plt.plot(x, y, color="k", label="Predictions")
    plt.xlabel("twitter_followers")
    plt.ylabel("popularity")
    plt.legend()
    plt.show()


def get_cleaned_data(raw_dataset):
    dataset = raw_dataset.copy()

    dataset = dataset[["twitter_followers", "popularity"]]
    dataset["popularity"] = dataset["popularity"] / 100
    # dataset["twitter_followers"] = np.log2(dataset["twitter_followers"])
    dataset["twitter_followers"] = dataset["twitter_followers"]

    return dataset


def get_split_data(dataset):
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    return train_dataset, test_dataset


def get_training_data(train_dataset, test_dataset):
    train_features = train_dataset.copy()
    test_features = test_dataset.copy()

    train_labels = train_features.pop("popularity")
    test_labels = test_features.pop("popularity")

    return train_features, test_features, train_labels, test_labels


def get_model(x, y):
    x_normalized = layers.Normalization(
        axis=None,
    )
    x_normalized.adapt(np.array(x))

    model = tf.keras.Sequential([x_normalized, layers.Dense(units=1)])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
        loss="mean_squared_error",
    )

    history = model.fit(
        x,
        y,
        epochs=2,
        # Suppress logging.
        verbose=0,
        # Calculate validation results on 20% of the training data.
        validation_split=0.2,
    )

    hist = pd.DataFrame(history.history)
    hist["epoch"] = history.epoch

    return model, history, hist


class Command(BaseCommand):
    help = "Artists Popularity Model generator"

    def add_arguments(self, parser):
        parser.add_argument(
            "--plot",
            action="store_true",
            help="Displays available plots",
        )

    def handle(self, **options):
        uri = "./data/artists.csv"

        raw_dataset = pd.read_csv(
            uri,
            na_values="?",
            comment="\t",
            sep=",",
            skipinitialspace=True,
        )

        dataset = get_cleaned_data(raw_dataset)
        print(dataset.tail())
        print(dataset.isna().sum())

        train_dataset, test_dataset = get_split_data(dataset)
        print(train_dataset.describe().transpose())
        if options["plot"]:
            plot_values(train_dataset)

        train_features, test_features, train_labels, test_labels = get_training_data(
            train_dataset, test_dataset
        )

        model, history, hist = get_model(
            train_features["twitter_followers"],
            train_labels,
        )
        model.summary()
        print(hist.tail())
        if options["plot"]:
            plot_loss(history)

        test_loss = model.evaluate(
            test_features["twitter_followers"], test_labels, verbose=2
        )
        print("\nTest loss:", test_loss)

        if options["plot"]:
            # x = tf.linspace(0.0, np.log2(max(raw_dataset["twitter_followers"])), 1000)
            x = tf.linspace(0.0, max(raw_dataset["twitter_followers"]), 1000)
            y = model.predict(x)
            plot_xy(x, y, train_features["twitter_followers"], train_labels)

        model.save("./data/model/artist_popularity_model.keras")
        model.export("./data/model/saved_model")
