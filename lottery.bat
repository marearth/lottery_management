cd /d E:\Code\python\lottery_management
START "lottery" /wait /B python E:\Code\python\lottery_management\scrape_webpage.py > info.txt | type info.txt
START "lottery" /wait /B python E:\Code\python\lottery_management\evaluate_lottery.py >> info.txt | type info.txt
START "lottery" /wait /B python E:\Code\python\lottery_management\predict_lottery.py >> info.txt | type info.txt