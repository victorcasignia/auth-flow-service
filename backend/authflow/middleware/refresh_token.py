from rest_framework_simplejwt.tokens import SlidingToken
from rest_framework_simplejwt.settings import api_settings

class RefreshToken(object):
    def get_token(self, header):
        PREFIX = 'Bearer '
        if not header.startswith(PREFIX):
            raise ValueError('Invalid token')

        return header[len(PREFIX):]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if(request.META):
            if(request.META.get('HTTP_AUTHORIZATION')):
                token_str = self.get_token(request.META.get('HTTP_AUTHORIZATION'))
                if token_str:
                    token = SlidingToken(token_str)
                    if token:
                        token.check_exp(api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

                        token.set_exp()
                        token.set_iat()

        response = self.get_response(request)
        return response
