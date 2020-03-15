from TwitterAPI import TwitterAPI
import speedtest
import sched
import time

consumer_key= ""
consumer_secret= ""
access_token_key= ""
access_token_secret= ""


internet_package = "Performance"
# in megabits
expected_download = 60
expected_upload = 2


api = TwitterAPI(consumer_key,
                 consumer_secret,
                 access_token_key,
                 access_token_secret)


def check_speeds():
	speedtester = speedtest.Speedtest()

	# returned as bits, converted to megabits
	download_speed = speedtester.download() / 1000000.0
	upload_speed = speedtester.upload() / 1000000.0

	print(download_speed)
	print(upload_speed)
	print("\n")
	if download_speed < expected_download:
		difference = expected_download - download_speed
		tweet = "@XFinity Why is my internet being slow? I'm supposed to be getting " + expected_download + "Mbps download and " + expected_upload + "Mbps upload, but I'm only getting " + download_speed + "Mbps download and " + upload_speed + "Mbps upload."
		api.request("statuses/update", {'status': tweet})


scheduler = sched.scheduler(time.time, time.sleep)

def periodic_check(scheduler, interval, action, arguments=()):
	scheduler.enter(interval, 1, periodic_check, (scheduler, interval, action, arguments))
	action()


periodic_check(scheduler, 1, check_speeds)
scheduler.run()