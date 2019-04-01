"""Main CPIMS common views."""
import memcache
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from cpovc_registry.functions import dashboard, ovc_dashboard
from cpovc_main.functions import get_dict
from cpovc_access.functions import access_request
from django.contrib.auth.decorators import login_required

mc = memcache.Client(['127.0.0.1:11211'], debug=0)


@login_required(login_url='/login/')
def home(request):
    """Some default page for the home page / Dashboard."""
    try:
        vals = get_dashboard(request)
        return render(request, 'dashboard.html', vals)
    except Exception, e:
        print 'dashboard error - %s' % (str(e))
        raise e


def get_dashboard(request):
    """Some default page for the home page / Dashboard."""
    my_dates, my_cvals = [], []
    my_ovals, my_kvals = [], []
    my_dvals = []
    try:
        user_key = 'dash_%s' % (request.user.id)
        value = mc.get(user_key)
        if value:
            print 'In memcache Dashboard - %s' % (user_key)
            return value
        else:
            print 'Set new Dashboard - %s' % (user_key)
        dash = dashboard()
        start_date = datetime.now() - timedelta(days=21)
        summary = {}
        summary['org_units'] = '{:,}'.format(dash['org_units'])
        summary['children'] = '{:,}'.format(dash['children'])
        summary['guardians'] = '{:,}'.format(dash['guardian'])
        summary['workforce'] = '{:,}'.format(dash['workforce_members'])
        summary['cases'] = '{:,}'.format(dash['case_records'])
        summary['pending'] = '{:08}'.format(dash['pending_cases'])

        # OVC care
        odash = ovc_dashboard(request)
        ovc = {}
        ovc['org_units'] = '{:,}'.format(odash['org_units'])
        ovc['children'] = '{:,}'.format(odash['children'])
        ovc['children_all'] = '{:,}'.format(odash['children_all'])
        ovc['guardians'] = '{:,}'.format(odash['guardian'])
        ovc['workforce'] = '{:,}'.format(odash['workforce_members'])
        ovc['cases'] = '{:,}'.format(odash['case_records'])
        ovc['pending'] = '{:08}'.format(odash['pending_cases'])
        ovc['household'] = 0
        ovc['hiv_status'] = odash['hiv_status']
        ovc['domain_hiv_status'] = odash['domain_hiv_status']
        child_regs = odash['child_regs']
        ovc_regs = odash['ovc_regs']
        case_regs = odash['case_regs']
        case_cats = dash['case_cats']
        for date in range(0, 22, 2):
            end_date = start_date + timedelta(days=date)
            show_date = datetime.strftime(end_date, "%d-%b-%y")
            final_date = str(show_date).replace(' ', '&nbsp;')
            my_dates.append("[%s, '%s']" % (date, final_date))
        for vl in range(1, 22):
            t_date = start_date + timedelta(days=vl)
            s_date = datetime.strftime(t_date, "%d-%b-%y")
            k_count = child_regs[s_date] if s_date in child_regs else 0
            o_count = ovc_regs[s_date] if s_date in ovc_regs else 0
            c_count = case_regs[s_date] if s_date in case_regs else 0
            my_cvals.append("[%s, %s]" % (vl, c_count))
            my_kvals.append("[%s, %s]" % (vl, k_count))
            my_ovals.append("[%s, %s]" % (vl, o_count))
        dates = ', '.join(my_dates)
        kvals = ', '.join(my_kvals)
        cvals = ', '.join(my_cvals)
        ovals = ', '.join(my_ovals)
        my_dvals, cnt = [], 0
        colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00',
                  '#ffff33']
        reg_ovc = request.session.get('reg_ovc', 0)
        ovc_criterias = False
        total_ovc = odash['children_all']
        if reg_ovc and total_ovc > 0:
            # Eligibility criteria
            ovc_criterias = True
            other_case = 0
            cat_name = "Missing Criteria"
            cat_data = total_ovc
            cnt = 0
            my_data = '{label: "%s", data: %s, color: "%s"}' % (
                cat_name, cat_data, colors[cnt])
            my_dvals.append(my_data)
        else:
            # Case category names
            cnames = get_dict(field_name=['case_category_id'])
            other_case = 0
            for case_cat in case_cats:
                cat_id = case_cat['case_category']
                cat_data = case_cat['unit_count']
                if cnt > 4:
                    other_case += cat_data
                else:
                    cnm = cnames[cat_id] if cat_id in cnames else cat_id
                    cat_name = cnm[:16] + ' ...' if len(cnm) > 16 else cnm
                    my_data = '{label: "%s", data: %s, color: "%s"}' % (
                        cat_name, cat_data, colors[cnt])
                    my_dvals.append(my_data)
                cnt += 1
        if not case_cats and not ovc_criterias:
            my_dvals.append('{label: "No data", data: 0, color: "#fd8d3c"}')
        if other_case > 0:
            my_dvals.append(
                '{label: "Others", data: %s, color: "#fb9a99"}' % (other_case))
        dvals = ', '.join(my_dvals)
        ovc_params = odash['ovc_summary']
        om_data = '[0, {m0}], [1, {m1}], [2, {m2}], [3, {m3}], [4, {m4}]'
        of_data = '[0, {f0}], [1, {f1}], [2, {f2}], [3, {f3}], [4, {f4}]'
        omdata = om_data.format(**ovc_params)
        ofdata = of_data.format(**ovc_params)
        vals = {'status': 200, 'dates': dates, 'kvals': kvals,
                'dvals': dvals, 'cvals': cvals, 'data': summary,
                'ovals': ovals, 'ovc': ovc, 'omvals': omdata,
                'ofvals': ofdata}
        mc.set(user_key, vals, 6 * 60 * 60 )
    except Exception, e:
        print 'dashboard error - %s' % (str(e))
        raise e
    else:
        return vals


def access(request):
    """Some default page for access login."""
    try:
        if request.method == 'POST':
            response = access_request(request)
            return JsonResponse(response, content_type='application/json',
                                safe=False)
        return render(request, 'home.html', {'status': 200, })
    except Exception, e:
        raise e


def handler_400(request):
    """Some default page for Bad request error page."""
    try:
        return render(request, '400.html', {'status': 400})
    except Exception, e:
        raise e


def handler_404(request):
    """Some default page for the Page not Found."""
    try:
        return render(request, '404.html', {'status': 404})
    except Exception, e:
        raise e


def handler_500(request):
    """Some default page for Server Errors."""
    try:
        return render(request, '500.html', {'status': 500})
    except Exception, e:
        raise e
