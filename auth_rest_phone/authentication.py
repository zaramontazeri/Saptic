from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(BasicAuthentication):

    def enforce_csrf(self, request):
        print("heeeellllooooo")
        return  # To not perform the csrf check previously happening
