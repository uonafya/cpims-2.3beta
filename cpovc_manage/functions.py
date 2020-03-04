import pandas as pd
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
from cpovc_reports.functions import get_styles, get_header, draw_page, Canvas
from reportlab.lib import colors
from .models import NOTTTravel, NOTTChaperon, NOTTChild


def get_travel(request, travel_id=0, params={}):
    """Method to get travels."""
    try:
        if travel_id > 0:
            travel = NOTTTravel.objects.get(pk=travel_id)
        else:
            travel = NOTTTravel.objects.filter(pk=travel_id)
    except Exception as e:
        raise e
    else:
        return travel


def get_travel_details(request, element, travel):
    """Method to get travel details."""
    try:
        data = [['Travel Details', '']]
        travel_id = travel.id
        summary = 'Applied (%s), ' % (travel.no_applied)
        summary += 'Cleared (%s), ' % (travel.no_cleared)
        summary += 'Returned (%s)' % (travel.no_returned)
        tdate = travel.travel_date
        rdate = travel.return_date
        data.append(['Institution Name', travel.institution_name])
        data.append(['Country of Travel', travel.country_name])
        data.append(['Date of Travel', tdate.strftime("%d-%B-%Y")])
        data.append(['Date of Return', rdate.strftime("%d-%B-%Y")])
        data.append(['Reason of Travel', travel.reason])
        data.append(['Summary of Children Traveling', summary])
        data.append(['Sponsor', travel.sponsor])
        df = pd.DataFrame.from_records(data)
        print(df)
        # dt_size = len(df.index)
        # col_size = len(df.columns)
        # ds = dt_size + 2
        style = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             # ('ALIGN', (1, 3), (-1, -1), 'RIGHT'),
             ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])
        d0 = 27.86 - 11.0
        cols = (11.0 * cm, d0 * cm)
        t1 = Table(data, colWidths=cols)
        t1.setStyle(style)
        element.append(t1)
        element.append(Spacer(0.1 * cm, .8 * cm))
        # Chaperons
        style = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('FONTNAME', (0, 0), (3, 1), 'Helvetica-Bold'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])
        cnt = 0
        chaps = [['', 'Chaperons', '', ''],
                 ['#', 'Names', 'Sex', 'Passport Number']]
        chaperons = NOTTChaperon.objects.filter(travel_id=travel_id)
        for chap in chaperons:
            cnt += 1
            first_name = chap.other_person.person_first_name
            surname = chap.other_person.person_surname
            other_names = chap.other_person.person_other_names
            sex_id = chap.other_person.person_sex
            passport_no = chap.other_person.person_identifier
            names = '%s %s %s' % (first_name, surname, other_names)
            sex = 'Male' if sex_id == 'SMAL' else 'Female'
            chaps.append([str(cnt), names, sex, passport_no])
        t2 = Table(chaps, colWidths=(1.0 * cm, 10.0 * cm, 7 * cm, 9.86 * cm))
        t2.setStyle(style)
        element.append(t2)
        element.append(Spacer(0.1 * cm, .8 * cm))
        # Children
        style = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('FONTNAME', (0, 0), (5, 1), 'Helvetica-Bold'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])
        chnt = 0
        ctitle = ['#', 'Names', 'Sex', 'Passport Number',
                  'Cleared', 'Returned']
        childls = [['', 'Children', '', '', '', ''], ctitle]
        children = NOTTChild.objects.filter(travel_id=travel_id)
        for child in children:
            chnt += 1
            first_name = child.person.first_name
            surname = child.person.surname
            other_names = child.person.other_names
            sex_id = child.person.sex_id
            passport_no = child.passport
            cleared = child.cleared
            returned = child.returned
            tcl = 'Yes' if cleared else 'No'
            tret = 'Yes' if returned else 'No'
            names = '%s %s %s' % (first_name, surname, other_names)
            sex = 'Male' if sex_id == 'SMAL' else 'Female'
            cdetails = [str(chnt), names, sex, passport_no, tcl, tret]
            childls.append(cdetails)
        ccol = (1.0 * cm, 10.0 * cm, 7 * cm, 5.86 * cm, 2 * cm, 2 * cm)
        t2 = Table(childls, colWidths=ccol)
        t2.setStyle(style)
        element.append(t2)
    except Exception as e:
        raise e
    else:
        pass


def travel_pdf(request, response, file_name):
    """Method to generate pdf."""
    try:
        rid = 5
        fnames = file_name.split('_')
        travel_id = int(fnames[2])
        tid = '{0:05d}'.format(travel_id)
        # Get some parameters
        travel = get_travel(request, travel_id)
        tarehe = travel.travel_date
        report_name = 'SNo. %s - Travel Authorization ' % (tid)
        region = 'National'
        dates = 'Date %s' % (tarehe.strftime("%d, %B %Y"))
        styles = get_styles()
        element = []
        get_header(element, report_name, region, dates, styles)
        # Write the data
        get_travel_details(request, element, travel)
        doc = SimpleDocTemplate(
            response, pagesize=A4, rightMargin=20,
            leftMargin=20, topMargin=30, bottomMargin=36.5,
            keywords="CPIMS, Child Protection in Kenya, UNICEF, DCS, <!NMA!>")
        if rid in [1, 3, 4, 5]:
            doc.pagesize = landscape(A4)
        element.append(Spacer(0.1 * cm, .2 * cm))
        # doc.build(element)
        doc.watermark = 'CPIMS'
        doc.fund_name = ''
        doc.report_info = ''
        doc.source = 'Child Protection Information Management System (CPIMS)'
        doc.build(element, onFirstPage=draw_page, onLaterPages=draw_page,
                  canvasmaker=Canvas)
    except Exception as e:
        raise e
    else:
        pass
