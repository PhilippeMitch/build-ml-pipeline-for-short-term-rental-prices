#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info('Input artifact received')

    ######################
    # YOUR CODE HERE     #
    ######################
    
    # Load the data
    df = pd.read_csv(artifact_local_path)
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    logger.info('Dataframe cleaning steps done')

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Save the results to a CSV file called clean_sample.csv
    # Write cleaned version
    logger.info("Logging artifact")
    filename = args.output_artifact
    df.to_csv(filename, index=False)
    # df.to_csv("clean_sample.csv", index=False)
    logger.info('Dataframe saved to csv')

    # upload CSV file to W&B using
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )

    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    logger.info('Cleaned data artifact logged to W&B')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help= "Name of the input artifact raw data and version" , ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type= str, ## INSERT TYPE HERE: str, float or int,
        help="Name of the output artifact clean data", ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help="Type of the output artifcat", ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help="Description for the output steps", ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float, ## INSERT TYPE HERE: str, float or int,
        help="Minimum price value for rental", ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float, ## INSERT TYPE HERE: str, float or int,
        help="Maximum price value for rental", ## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)
