import requests
import qrcode 
import random 

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


# Get eventbrite token
token = open('token.txt', 'r').read()
event_id = "50627158193" # Extracted from event url

response = requests.get(
    "https://www.eventbriteapi.com/v3/events/%s/attendees" % event_id,
    headers = {
        "Authorization": "Bearer " + token,
    },
    verify = True,  # Verify SSL certificate
)
attendees = response.json()['attendees']

for i, attendee in enumerate(attendees): 

	# TICKET TEMPLATE
	ticket_template = Image.open('ticket_template.png')

	# QR CODE GENERATION 
	order_id = attendee['order_id']
	id = attendee['id']
	seq_num = "{0:0=3d}".format(i + 1)
	first_name = attendee['profile']['first_name']
	last_name = attendee['profile']['last_name']
	name = ("%s_%s" % (first_name, last_name)).lower()
	qr = qrcode.QRCode(
	    version = 2,
	    error_correction = qrcode.constants.ERROR_CORRECT_H,
	    box_size = 20, # Adjust size for output onto image
	    border = 0,
	)

	table_number = str(5)
	flight_number = "%s%d" % (random.choice(["AC", "BRU", "A", "AF"]))
	gate = random.randint(1, 99)

	qr_data = "%s%s%s" % (order_id, id, seq_num)
	qr.add_data(qr_data)
	qr.make(fit=True)
	qr_img = qr.make_image(back_color="transparent")


	ticket_template.paste(qr_img, (2675, 35), qr_img)
	ticket = ImageDraw.Draw(ticket_template)
	font = ImageFont.truetype("Montserrat.otf", 90)
	name_font = ImageFont.truetype("Montserrat.otf", 60)
	ticket.text((2600, 728), table_number, (102, 102, 102), font=font)
	ticket.text((2600, 975), flight_number, (102, 102, 102), font=font)
	ticket.text((3000, 975), gate, (102, 102, 102), font=font)

	ticket.text((80, 325), first_name + " " + last_name, (255,255,255), font=name_font)

	ticket_template.save("tickets/%s.png" % name)



