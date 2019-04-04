"""CPIMS terms and policies views."""
from django.shortcuts import render
from django.conf import settings

DOC_ROOT = settings.DOCUMENT_ROOT


def terms(request, id):
    """Page for terms, policy and cookie stuff."""
    pages = {1: 'CPIMS Terms and Conditions',
             2: 'CPIMS Data Policy',
             3: 'CPIMS Cookie Use'}
    try:
        req_id = int(id)
        term_text = open_terms()
        term_id = req_id if req_id in pages else 1
        term_detail = '<p>%s</p>' % (term_text)
        return render(request, 'terms.html',
                      {'term_title': pages[term_id],
                       'term_detail': term_detail})
    except Exception, e:
        raise e


def open_terms(fname='terms'):
    """Read terms from a text file."""
    try:
        terms_name = '%s/%s.txt' % (DOC_ROOT, fname)
        with open(terms_name, 'r') as myfile:
            data = myfile.read().replace('\n', '</p><p>')
            return data
    except Exception:
        return ''
