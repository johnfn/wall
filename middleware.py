from django.contrib import messages

class FirstTimeMessageMiddleware(object):
    def process_request(self, request):
        if "first" not in request.session:
        #if not request.user.is_authenticated():
            messages.warning(request, 'Connect with Facebook if you want to post comments or challenge a candidate!')
            request.session['first'] = 1
