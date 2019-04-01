#import twilio
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC8644434162824128856211693c6cee7d"

# Your Auth Token from twilio.com/console
auth_token  = "7eac71f974b1d389809be63a4ad71777"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+12266004456", 
    from_="+12266028649",
    body="Alert! Alert! KWGeeseCam is dying!")

print(message.sid)
