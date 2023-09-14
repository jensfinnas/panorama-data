import argparse
from lib.slack import post_to_slack
from settings import SLACK_WEBHOOK_URL


def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("msg", help="Message to be posted")
    args = parser.parse_args()
    assert SLACK_WEBHOOK_URL is not None, "SLACK_WEBHOOK_URL must be set"
    post_to_slack(SLACK_WEBHOOK_URL, args.msg)


if __name__ == "__main__":
    main()
