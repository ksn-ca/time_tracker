from datetime import datetime, timedelta

from pixella import post_to_pixella_since, post_to_pixella_yesterday

# OTHER
YESTERDAY = datetime.now().date() - timedelta(days=1)
SINCE = datetime.strptime('20231206', '%Y%m%d').date()
TEST_DAY = datetime.strptime('20231206', '%Y%m%d').date()









post_to_pixella_yesterday(YESTERDAY)
post_to_pixella_since(SINCE)
