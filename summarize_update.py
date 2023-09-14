import argparse
import os
from lib.utils import compare_csv_files, convert_values_to_float
from lib.bot import generate_summary
from lib.slack import html_to_slack_markup, post_to_slack
from settings import SLACK_WEBHOOK_URL

def main(folder, comparison_folder):
    print(f"The folder is: {folder}")
    print(f"The comparison folder is: {comparison_folder}")

    fp_ind_now = os.path.join(folder, "indicators.csv")
    fp_ind_then = os.path.join(comparison_folder, "indicators.csv")
    diff = compare_csv_files(fp_ind_then, fp_ind_now)

    for (then, now) in  diff["updated"]:
        now = convert_values_to_float(now)
        then = convert_values_to_float(then)
        if then["outcomeLatestYear"] == now["outcomeLatestYear"]:
            continue
        
        html = generate_summary(now, then)
        slack_msg = html_to_slack_markup(html)
        post_to_slack(SLACK_WEBHOOK_URL, slack_msg, 
                      username="Nytt från Panorama", icon_emoji=":alarm_clock:", )
        
        break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process two folder paths.")
    
    # Add required positional arguments
    parser.add_argument("folder", type=str, help="The path of the folder.")
    parser.add_argument("comparison_folder", type=str, help="The path of the comparison folder.")
    
    args = parser.parse_args()
    
    main(args.folder, args.comparison_folder)
