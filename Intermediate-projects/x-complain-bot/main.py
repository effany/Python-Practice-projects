from internet_speed_twitter_bot import SpeedTester, TwitterBot


# Run speed test
speed_tester = SpeedTester()
speed_tester.run_test()

# Check speeds and tweet if below promised
twitter_bot = TwitterBot()

if speed_tester.download_speed < speed_tester.promised_down:
    message = f"Hey @O2_CZ, why is my internet download speed {speed_tester.download_speed} Mbps when I pay for {speed_tester.promised_down} Mbps?"
    tweet_id = twitter_bot.post(message)
    # To reply to this tweet later: twitter_bot.post("Follow up message", reply_to_id=tweet_id)
elif speed_tester.upload_speed < speed_tester.promised_up:
    message = f"Hey @O2_CZ, why is my internet upload speed {speed_tester.upload_speed} Mbps when I pay for {speed_tester.promised_up} Mbps?"
    tweet_id = twitter_bot.post(message)
else:
    print("Everything in place!")
    