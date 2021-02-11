import os
import urllib
import mimetypes

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.http import HttpResponse
from .models import OVCDownloads, OVCFAQ


@login_required
def help_home(request):
    """Method to do pivot reports."""
    try:
        return render(request, 'help/home.html', {'form': {}})
    except Exception, e:
        raise e
    else:
        pass


@login_required
def help_downloads(request):
    """Method to do pivot reports."""
    try:
        docs = OVCDownloads.objects.filter(is_void=False)
        return render(request, 'help/downloads.html',
                      {'docs': docs, 'form': {}})
    except Exception, e:
        raise e
    else:
        pass


@login_required
def help_faq(request):
    """Method to do pivot reports."""
    try:
        faqs = OVCFAQ.objects.filter(is_void=False)
        return render(request, 'help/faq.html', {'form': {}, 'faqs': faqs})
    except Exception, e:
        raise e
    else:
        pass


@login_required
def doc_download(request, name):
    """Method to do pivot reports."""
    try:
        try:
            doc_id = request.GET["id"]
            doc = OVCDownloads.objects.get(id=doc_id, is_void=False)
            doc.downloads = doc.downloads + 1
            doc.save()
        except Exception:
            pass
        file_path = '%s/documents/%s' % (settings.MEDIA_ROOT, name)
        fp = open(file_path, 'rb')
        response = HttpResponse(fp.read())
        fp.close()
        mime_type, encoding = mimetypes.guess_type(name)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        response['Content-Type'] = mime_type
        response['Content-Length'] = str(os.stat(file_path).st_size)
        if encoding is not None:
            response['Content-Encoding'] = encoding
        # new_name = uuid.uuid3(uuid.NAMESPACE_DNS, file_name)
        # To inspect details for the below code, see
        # http://greenbytes.de/tech/tc2231/
        if u'WebKit' in request.META['HTTP_USER_AGENT']:
            # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string
            # directly.
            fheader = 'filename=%s' % name.encode('utf-8')
        elif u'MSIE' in request.META['HTTP_USER_AGENT']:
            # IE does not support internationalized filename at all.
            # It can only recognize internationalized URL, so we do the
            # trick via routing rules.
            fheader = ''
        else:
            # For others like Firefox, we follow RFC2231 (encoding
            # extension in HTTP headers).
            file_header = urllib.quote(name.encode('utf-8'))
            fheader = 'filename*=UTF-8\'\'%s' % file_header
        response['Content-Disposition'] = 'attachment; ' + fheader
    except Exception, e:
        raise e
    else:
        return response
