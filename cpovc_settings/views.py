import os
import csv
import time
import pandas as pd
from datetime import datetime
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SettingsForm
from django.conf import settings
from cpovc_ovc.models import OVCFacility, OVCSchool
from cpovc_access.views import open_terms
from cpovc_reports.queries import QUERIES
from cpovc_reports.functions import run_sql_data, get_variables

MEDIA_ROOT = settings.MEDIA_ROOT


# Create your views here.
@login_required
def settings_home(request):
    """Method to do pivot reports."""
    try:
        return render(request, 'settings/home.html', {'form': {}})
    except Exception, e:
        raise e
    else:
        pass


@login_required
def settings_reports(request):
    """Method to do pivot reports."""
    # mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime
    try:
        reports = []
        user_in = '%s-' % (request.user.id)
        directory = '%s/xlsx/' % (MEDIA_ROOT)
        for filename in os.listdir(directory):
            is_admin = True if request.user.is_superuser else False
            is_allowed = True if filename.startswith(user_in) else is_admin
            if (filename.endswith(".xlsx") or filename.endswith(".xlsm") ) and is_allowed:
                rname = os.path.join(directory, filename)
                cdate = os.stat(rname)
                (md, ino, dev, nnk, uid, gid, size, atm, mtime, ctime) = cdate
                create_date = time.ctime(mtime)
                report_name = rname.split('-')[-1]
                report = [report_name, create_date, filename]
                reports.append(report)
        return render(request, 'settings/reports.html', {'reports': reports})
    except Exception, e:
        raise e
    else:
        pass


@login_required
def archived_reports(request, file_name):
    """Method to do pivot reports."""
    try:
        directory = '%s/xlsx/' % (MEDIA_ROOT)
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                return response
    except Exception, e:
        raise e
    else:
        pass


@login_required
def remove_reports(request, file_name):
    """Method to do pivot reports."""
    try:
        directory = '%s/xlsx/' % (MEDIA_ROOT)
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            msg = "File named %s removed Successfully" % (file_name)
            messages.info(request, msg)
        return HttpResponseRedirect(reverse(settings_reports))
    except Exception, e:
        msg = "COuld not remove %s: %s." % (file_name, str(e))
        messages.error(request, msg)
        return HttpResponseRedirect(reverse(settings_reports))
    else:
        pass


@login_required
def settings_facilities(request):
    """Method to do pivot reports."""
    # mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime
    try:
        if request.method == 'POST':
            search_param = str(request.POST.get('facility'))
            if search_param.isdigit():
                facilities = OVCFacility.objects.filter(
                facility_code=search_param)
            else:
                facilities = OVCFacility.objects.filter(
                    facility_name__icontains=search_param)
        else:
            facilities = OVCFacility.objects.all().order_by('-id')[:1000]
        return render(request, 'settings/facilities.html', {'facilities': facilities})
    except Exception, e:
        raise e
    else:
        pass


@login_required
def settings_schools(request):
    """Method to do pivot reports."""
    # mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime
    try:
        if request.method == 'POST':
            search_param = str(request.POST.get('school'))
            schools = OVCSchool.objects.filter(
                school_name__icontains=search_param)
        else:
             schools = OVCSchool.objects.all().order_by('-id')[:1000]
        return render(request, 'settings/schools.html', {'schools': schools})
    except Exception, e:
        raise e
    else:
        pass


def write_excel(data, csv_file, xlsx_file):
    """method to write excel file."""
    try:
        with open(csv_file, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"',
                                   quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerows(data)
        df_new = pd.read_csv(csv_file)
        writer = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
        df_new.to_excel(writer, sheet_name='Sheet1', index=False)
        # This is it       
        workbook = writer.book
        workbook.add_worksheet('Sheet2')
        workbook.add_worksheet('Sheet3')
        writer.save()
        writer.close()
    except Exception as e:
        raise e
    else:
        pass


def qstorows(desc, rows):
    try:
        data, titles = [], []
        columns = rows[0]
        # columns = [col.lower() for col in cols]
        titles = []
        if rows:
            for res in rows[0]:
                titles.append(res)
        data = [titles]
        for res in rows:
            vals = []
            for n, i in enumerate(columns):
                val = res[i]
                if type(val) is unicode:
                    val = val.encode('ascii', 'ignore').decode('ascii')
                vals.append(val)
            data.append(vals)
    except Exception as e:
        print 'error getting rows - %s' % (str(e))
        return []
    else:
        return data


@login_required
def settings_rawdata(request):
    """Method to do pivot reports."""
    # mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime
    try:
        file_name = ""
        ts = time.time()
        reports, results = [], {}
        dts = {1: "MasterList", 2: "AssessmentList",
               3: "PrioritiesList", 4: "ServicesList"}
        dqs = {1: "registration_list", 2: "ovc_assessed_list",
               3: "ovc_priority_list", 4: "ovc_served_list"}
        st = datetime.fromtimestamp(ts).strftime('%Y%m%d%H')
        form = SettingsForm(request.user)
        user_in = '%s-' % (request.user.id)
        directory = '%s/xlsx/' % (MEDIA_ROOT)
        for filename in os.listdir(directory):
            is_admin = True if request.user.is_superuser else False
            is_allowed = True if filename.startswith(user_in) else is_admin
            if (filename.endswith(".xlsx") or filename.endswith(".xlsm") ) and is_allowed:
                print filename
                rname = os.path.join(directory, filename)
                cdate = os.stat(rname)
                (md, ino, dev, nnk, uid, gid, size, atm, mtime, ctime) = cdate
                create_date = time.ctime(mtime)
                report_name = rname.split('-')[-1]
                report = [report_name, create_date, filename]
                reports.append(report)
        if request.method == 'POST':
            form = SettingsForm(request.user, data=request.POST)
            params = get_variables(request)
            print 'PARAMS', params
            raw_data = request.POST.get('raw_data')
            org_unit = request.POST.get('org_unit')
            cluster = request.POST.get('cluster')
            if not org_unit and not cluster:
                 msg = "You must provide either Org Unit or Cluster"
                 messages.error(request, msg)
                 return render(request, 'settings/data.html',
                      {'reports': reports, 'form': form, 'results': results,
                       'file_name': file_name})
            rid = int(raw_data) if raw_data else 1
            query_name = dqs[rid]
            sql = QUERIES[query_name].replace(';', '')
            fname = '%s-%s.%s00' % (request.user.id, dts[rid], st)
            csv_file = '%s.csv' % (fname)
            csv_file_name = '%s/csv/%s' % (MEDIA_ROOT, csv_file)
            xlsx_file = '%s.xlsx' % (fname)
            final_sql = sql.format(**params)
            print 'SQL', final_sql
            # rows = my_custom_sql(final_sql)
            rows, desc = run_sql_data(request, final_sql)
            # print '99999', desc
            if rows:
                file_name = xlsx_file
                data = qstorows(desc, rows)
                xlsx_file_name = '%s/xlsx/%s' % (MEDIA_ROOT, xlsx_file)
                write_excel(data, csv_file_name, xlsx_file_name)
                msg = "Report Generated Successfully"
                messages.info(request, msg)
            else:
                msg = "Query returned 0 Results"
                messages.error(request, msg)   
        return render(request, 'settings/data.html',
                      {'reports': reports, 'form': form, 'results': results,
                       'file_name': file_name})
    except Exception, e:
        raise e
    else:
        pass


def change_notes(request):
    """Method to track system changes from a txt file."""
    try:
        term_text = open_terms('changes')
        term_detail = '<p>%s</p>' % (term_text)
        return render(request, 'settings/changes.html',
                      {'term_title': 'Change Notes',
                       'term_detail': term_detail})
    except Exception, e:
        raise e
    else:
        pass
