import datetime
from main_scrape import scrape_and_gzip
from s3_upload import upload_to_aws

weekday = datetime.datetime.today().isoweekday()
# Sunday = 0 Saturday = 7
# If its thursday, run the program
if weekday == 5:
    sys.exit()
else:
    file_name = scrape_and_gzip()
    upload_to_aws(local_file=file_name, bucket='nyt-bestsellers', s3_file=file_name)