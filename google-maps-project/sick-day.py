import requests
import smtplib 

# API key
api_file = open("api-key.txt", "r")
api_key = api_file.readline()
api_file.close()

# home address input
home = input("Enter a home address\n") 
  
# work address input
work = input("Enter a work address\n") 
  
# base url
url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

# get response
r = requests.get(url + "origins=" + home + "&destinations=" + work + "&key=" + api_key) 
 
# return time as text and as seconds
time = r.json()["rows"][0]["elements"][0]["duration"]["text"]       
seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]
  
# print the travel time
print("\nThe total travel time from home to work is", time)

# check if travel time is more than 1 hour
if (seconds > 3600):
    # email constraints
    sender = "..."    
    recipient = "..."       
    subject = "Sick Day"   
    message = "Hi Team,\n\nSorry, but I can't make it into work today."
    
    # format email
    email = "Subject: {}\n\n{}".format(subject, message)
    
    # get sender password
    password_file = open("password.txt", "r")
    password = password_file.readline()
    password_file.close()
    
    # creates SMTP session 
    s = smtplib.SMTP("smtp.gmail.com", 587) 
      
    # start TLS for security 
    s.starttls() 
      
    # authentication 
    s.login(sender, password) 
      
    # sending the mail 
    s.sendmail(sender, recipient, email)
      
    # terminating the session 
    s.quit() 

    # success message
    print("\nSuccessfully sent a sick-day email to", recipient, "since the travel time was too long")
