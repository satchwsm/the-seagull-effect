'''A simple webapp2 server'''

from google.appengine.api import users
import webapp2
import cgi
import Image
import ImageDraw
import StringIO
import base64
import unicodedata

javascript = '<script> var container = document.querySelector("#fractal"); var displayPoint = document.querySelector("#point"); container.addEventListener("click", getClickPosition, false); function getClickPosition(e) { var xPosition = e.clientX - 8; var yPosition = e.clientY - 80; var xa = document.getElementById("xa").value; var xb = document.getElementById("xb").value; var ya = document.getElementById("ya").value; var yb = document.getElementById("yb").value; var xPosition = (xPosition / 256.0 * (xb - xa) + (xa - 0.0)); var yPosition = (-1 *((yPosition / 256.0) * (yb - ya) + (ya - 0.0))); displayPoint.innerHTML = xPosition+ " , " + yPosition;} </script>'

class MainPage(webapp2.RequestHandler):

    def get(self):

	self.refreshImage(-2.0, 1.0, -1.5, 1.5)

    def post(self):
	xa = cgi.escape(self.request.get('xa'))
	xb = cgi.escape(self.request.get('xb'))
	ya = cgi.escape(self.request.get('ya'))
	yb = cgi.escape(self.request.get('yb'))

	print xa, xb, ya, yb

	self.refreshImage(float(xa), float(xb), float(ya), float(yb))	

    def refreshImage(self, xa, xb, ya, yb):
	user = users.get_current_user()

	#mm = MandelbrotMaker()
	#fractal = mm.drawBrot(xa, xb, ya, yb)

	jj = JuliaJenerator()
	fractal = jj.drawJulia(0.1, 0.5, xa, xb, ya, yb)

	self.response.write(fractal)
        
        if user:
	    self.response.write('<br>The Seagull Effect<br>')
            self.response.write('Lets make some crazy fractals ' + user.nickname() + '<br><br>')
            self.response.write('left x-bound | right x-bound | lower y-bound | upper y-bound<br>')
            self.response.write(javascript)
	    self.response.write('<form action="/" method="post"><div><textarea id="xa" name="xa" rows="1" cols="5">'+str(xa)+'</textarea><textarea id="xb" name="xb" rows="1" cols="5">'+str(xb)+'</textarea><textarea id="ya" name="ya" rows="1" cols="5">'+str(ya)+'</textarea><textarea id="yb" name="yb" rows="1" cols="5">'+str(yb)+'</textarea></div><div><input type="submit" value="BAM"></div></form>')
        else:
            self.redirect(users.create_login_url(self.request.uri))



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

		return '<!doctype html><html><body><a id="fractal"><img src="data:image/png;base64, ' + img_b64 +  '"></a></body></html>'		
		
class JuliaJenerator():
	
	def drawJulia(self, initx, inity, xa, xb, ya, yb):

		maxIt = 128 # max iterations allowed
		# image size
		imgx = 256
		imgy = 256
		image = Image.new("RGB", (imgx, imgy))

		c = initx + inity * 1j
		
		for y in range(imgy):
    		    zy = y * (yb - ya) / (imgy - 1)  + ya
    		    for x in range(imgx):
        	        zx = x * (xb - xa) / (imgx - 1)  + xa
       		        z = zx + zy * 1j
        	        for i in range(maxIt):
            	            if abs(z) > 2.0:
               	                break 
            	            z = z * z + c
        	        image.putpixel((x, y), (i % 8 * 32, i % 16 * 16, i % 32 * 8))
		
		# PIL image can be saved as .png .jpg .gif or .bmp file\
		output = StringIO.StringIO()
		image.save(output, format='png')
		img_b64 = output.getvalue().encode('base64', 'strict')

		return '<!doctype html><html><body><br><p id="point"></p><a><img id="fractal" src="data:image/png;base64, ' + img_b64 +  '"></a><div id="point"></div></body></html>'



application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
