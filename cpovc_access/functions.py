"""Handling guests access requests."""
from .models import AccessRequest
from cpovc_registry.functions import get_client_ip


def access_request(request):
    """Method to save guest access requests."""
    response = {'status': 9}
    response['message'] = ('Request could not be saved because we '
                           'already have your details or there was an error. '
                           'Contact the administrator.')
    try:
        ip_address = get_client_ip(request)
        fname = request.POST.get('fname').strip()
        sname = request.POST.get('lname').strip()
        names = '%s %s' % (fname.title(), sname.title())
        email = request.POST.get('email').strip()
        phone_number = request.POST.get('tel').strip()
        access_req = AccessRequest(
            names=names, email_address=email, phone_number=phone_number,
            ip_address=ip_address).save()
        if access_req:
            response['status'] = 0
            response['message'] = 'Request saved successfully'
    except Exception:
        return response
