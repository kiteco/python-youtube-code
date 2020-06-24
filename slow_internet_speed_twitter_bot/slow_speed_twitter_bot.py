from TwitterAPI import TwitterAPI
import speedtest
import sched
import time
import os

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token_key = os.getenv("access_token_key")
access_token_secret = os.getenv("access_token_secret")

api = TwitterAPI(consumer_key,
                 consumer_secret,
                 access_token_key,
                 access_token_secret)


def check_speeds():
	speedtester = speedtest.Speedtest()

	advertised_download = 60
	advertised_upload = 2

	# returned as bits, converted to megabits
	download_speed = int(speedtester.download() / 1000000)
	upload_speed = int(speedtester.upload() / 1000000)

	print("Download Speed: " + str(download_speed) + "Mbps")
	print("Upload Speed: " + str(upload_speed) + "Mbps")
	print("\n")

    # # Uncomment code to create triaged messaging
    # thresholds = {'first':0.8, 'second':0.5}
    # messages = {'first':'[enter polite message]', 'second': '[enter stern message]'}
    # if download_speed < advertised_download * thresholds['first'] or upload_speed < advertised_upload * thresholds['first']:
    #     tweet = messages['first']
    #     api.request("statuses/update", {"status": tweet})
    # elif download_speed < advertised_download * thresholds['second'] or upload_speed < advertised_upload * thresholds['second']:
    #     tweet = messages['second']
    #     api.request("statuses/update", {"status": tweet})

    # If using triaged messaging, above, then comment out the conditional block, below.
	if download_speed < advertised_download * 0.8 or upload_speed < advertised_upload * 0.8:
		tweet = "@XFinity My speeds are 20% slower than advertised, any idea why? 😊"
		api.request("statuses/update", {"status": tweet})


scheduler = sched.scheduler(time.time, time.sleep)

def periodic_check(scheduler, interval, action, arguments=()):
	scheduler.enter(interval, 1, periodic_check, (scheduler, interval, action, arguments))
	action()


periodic_check(scheduler, 1, check_speeds)
scheduler.run()
