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


def check_speeds(checks, download_total, upload_total):
	speedtester = speedtest.Speedtest()

	# returned as bits, converted to megabits
	download_speed = int(speedtester.download() / 1000000)
	upload_speed = int(speedtester.upload() / 1000000)

	download_total += download_speed
	upload_total += upload_speed
	checks += 1

	upload_avg = upload_total / checks
	download_avg = download_total / checks

	print("Download Speed: " + str(download_speed) + "Mbps")
	print("Upload Speed: " + str(upload_speed) + "Mbps")
	print("Download Average: " + str(download_avg) + "Mbps")
	print("Upload Average: " + str(upload_avg) + "Mbps")
	print("\n")

	if download_speed < download_avg * 0.75 or upload_speed < upload_avg * 0.75:
		tweet = "@XFinity My speeds are 25% slower than usual, any idea why? 😊"
		api.request("statuses/update", {"status": tweet})

	if download_speed < download_avg * 0.5 or upload_speed < upload_avg * 0.5:
		tweet = "@XFinity My speeds are 50 PERCENT slower than averge... Please fix this. 😒"
		api.request("statuses/update", {"status": tweet})

	if download_speed < download_avg * 0.2 or upload_speed < upload_avg * 0.2:
		tweet = "Using my phone as a hotspot because my @XFinity speeds are 80% slower than usual 😠"
		api.request("statuses/update", {"status": tweet})


scheduler = sched.scheduler(time.time, time.sleep)

def periodic_check(scheduler, interval, action, arguments=()):
	scheduler.enter(interval, 1, periodic_check, (scheduler, interval, action, arguments))
	action(arguments[0], arguments[1], arguments[2])


periodic_check(scheduler, 1, check_speeds, (1, 60.0, 2.0))
scheduler.run()
