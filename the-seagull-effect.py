'''A simple webapp2 server'''

from google.appengine.api import users
import webapp2
import cgi
import Image
import ImageDraw
import StringIO
import base64

def left(xa, xb):
	MainPage.xb = xb - 0.1
	MainPage.xa = xa - 0.1

def right(xa, xb):
	MainPage.xb = xb + 0.1
	MainPage.xa = xa + 0.1 

def up(ya, yb):
	MainPage.yb = yb + 0.1
	MainPage.ya = ya + 0.1

def down(ya, yb):
	MainPage.yb = yb - 0.1
	MainPage.ya = ya - 0.1

def zoomIn(xa, xb, ya, yb):
	MainPage.xa = xa + 0.5
	MainPage.xb = xb - 0.5
	MainPage.ya = ya + 0.5
	MainPage.yb = yb - 0.5	

def zoomOut(xa, xb, ya, yb):
	MainPage.xa = xa - 0.5
	MainPage.xb = xb + 0.5
	MainPage.ya = ya - 0.5
	MainPage.yb = yb + 0.5


class MainPage(webapp2.RequestHandler):
	
    xa = -2.0
    xb = 1.0
    ya = -1.5
    yb = 1.5

    def get(self):

	self.refreshImage()

    def post(self):
	command = cgi.escape(self.request.get('content'))

	mutate = {"left": left(self.xa, self.xb), "right": right(self.xa, self.xb), "up": up(self.ya, self.yb), "down": down(self.ya, self.yb), "in": zoomIn(self.xa, self.xb, self.ya, self.yb), "out": zoomOut(self.xa, self.xb, self.ya, self.yb)}

	mutate[command]

	print command, self.xa, self.xb, self.ya, self.yb

	self.refreshImage()	

    def refreshImage(self):
	user = users.get_current_user()
        
        if user:
            self.response.write('<!DOCTYPE html><html><head><script>function myFunction() {document.getElementById("demo").innerHTML = "Paragraph changed.";}</script></head><body><h1>My Web Page</h1><p id="demo">A Paragraph</p><button type="button" onclick="myFunction()">Try it</button></body></html>')
            self.response.write('The Seagull Effect<br>')
            self.response.write('Lets make some crazy fractals ' + user.nickname() + '<br><br>')
	    self.response.write('<form action="/" method="post"><div><textarea name="content" rows="1" cols="15"></textarea></div><div><input type="submit" value="BAM"></div></form>')
        else:
            self.redirect(users.create_login_url(self.request.uri))


	mm = MandelbrotMaker()
	fractal = mm.drawBrot(self.xa, self.xb, self.ya, self.yb)

	self.response.write(fractal)


class MandelbrotMaker():

	
	def drawBrot(self, xa, xb, ya, yb):

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
