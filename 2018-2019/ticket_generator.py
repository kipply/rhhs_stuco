import requests
import qrcode 

token = open('token.txt', 'r').read()



response = requests.get(
    "https://www.eventbriteapi.com/v3/events/50627158193/attendees",
    headers = {
        "Authorization": "Bearer " + token,
    },
    verify = True,  # Verify SSL certificate
)
attendees = response.json()['attendees']

for i, attendee in enumerate(attendees): 
	order_id = attendee['order_id']
	id = attendee['id']
	seq_num = "{0:0=3d}".format(i + 1)
	name = ("%s_%s" % (attendee['profile']['first_name'].lower(), attendee['profile']['last_name'].lower()))

	qr = qrcode.QRCode(
	    version = 2,
	    error_correction = qrcode.constants.ERROR_CORRECT_H,
	    box_size = 10,
	    border = 2,
	)

	data = "%s%s%s" % (order_id, id, seq_num)
	qr.add_data(data)
	qr.make(fit=True)

	img = qr.make_image(back_color="transparent")
	img.save('qrcodes/%s.png' % name)