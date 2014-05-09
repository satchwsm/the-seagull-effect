'''A simple webapp2 server'''

from google.appengine.api import users
import webapp2
import cgi
import Image
import ImageDraw
import StringIO
import base64

xa = -2.0
xb = 1.0
ya = -1.5
yb = 1.5

def left():
	global xa 
	global xb
	xb -= 0.1
	xa -= 0.1

def right():
	global xa 
	global xb
	xb += 0.1
	xa += 0.1 

def up():
	global ya 
	global yb
	yb += 0.1
	ya += 0.1

def down():
	global ya 
	global yb
	yb -= 0.1
	ya -= 0.1

def zoomIn():
	global xa
	global xb
	global ya
	global yb
	xa += 0.5
	xb -= 0.5
	ya += 0.5
	yb -= 0.5	

def zoomOut():
	global xa
	global xb
	global ya
	global yb
	xa -= 0.5
	xb += 0.5
	ya -= 0.5
	yb += 0.5


class MainPage(webapp2.RequestHandler):

    def get(self):

	self.refreshImage()

    def post(self):
	command = cgi.escape(self.request.get('content'))

	mutate = {"left": left(), "right": right(), "up": up(), "down": down(), "in": zoomIn(), "out": zoomOut()}

	mutate[command]

	print command, xa, xb, ya, yb

	self.refreshImage()	

    def refreshImage(self):
	user = users.get_current_user()
        
        if user:
            self.response.write('<!doctype html><html><body><br><br></body></html>')
            self.response.write('The Seagull Effect<br>')
            self.response.write('Lets make some crazy fractals ' + user.nickname() + '<br><br>')
	    self.response.write('<form action="/" method="post"><div><textarea name="content" rows="1" cols="15"></textarea></div><div><input type="submit" value="BAM"></div></form>')
        else:
            self.redirect(users.create_login_url(self.request.uri))


	mm = MandelbrotMaker()
	fractal = mm.drawBrot()

	self.response.write(fractal)


class MandelbrotMaker():
	
	def drawBrot(self):

		maxIt = 128 # max iterations allowed
		# image size
		imgx = 256
		imgy = 256
		image = Image.new("RGB", (imgx, imgy))

		for y in range(imgy):
		    zy = y * (yb - ya) / (imgy - 1)  + ya
		    for x in range(imgx):
		        zx = x * (xb - xa) / (imgx - 1)  + xa
		        z = zx + zy * 1j
		        c = z
		        for i in range(maxIt):
		            if abs(z) > 2.0: break 
		            z = z * z + c
		        image.putpixel((x, y), (i % 4 * 64, i % 8 * 32, i % 16 * 16))
	   		
	    	# PIL image can be saved as .png .jpg .gif or .bmp file\
		output = StringIO.StringIO()
		image.save(output, format='png')
		img_b64 = output.getvalue().encode('base64', 'strict')

		return '<!doctype html><html><body><a href=""><img src="data:image/png;base64, ' + img_b64 +  '"></a></body></html>'		
		
	



application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
