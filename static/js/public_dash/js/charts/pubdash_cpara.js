function ouChange(levl,ouid,fcc,fcc_val) {
    showLoad(true);
    if(levl == undefined || levl == null || levl == ''){ levl = 'national'; }
    if(ouid == undefined || ouid == null || ouid == ''){ ouid = '0'; }
    if(fcc == undefined || fcc == null || fcc == ''){ fcc = 'none'; }
    if(fcc_val == undefined || fcc_val == null || fcc_val == ''){ fcc_val = 'none'; }

    var periodVal = $('#period option:selected').val();
    var months_array=getMonths();
    if(periodVal == undefined || periodVal == null){ periodVal = 12; }
    months_array=getMonths(periodVal);

    console.log('running ouChange() -> levl='+levl+' & ouid='+ouid+' & fcc='+fcc+' & fcc_val='+fcc_val);

    }



$(document).ready(function () {
    ouChange('national',"0",'none','none');
    fetchCPARAResults('national',"none","none","none","annual");
    fetchPerBenchmarkPerformance('national',"none","none","none","annual");
    fetchHHScoringCat('national',"none","none","none","annual");
    fetchPerBenchmarkDomainPerformance('national',"none","none","none","annual");
    //undone
    //
    //fetchDomainPerformance('national',"none","none","none","annual");
});


    function getMonths(periodType) {
        if(periodType == undefined || periodType == null || periodType == ''){
            periodType = 12;
        }
        cur_year = new Date().getFullYear();
        cur_month = new Date().getMonth();
        var months_arr = [];
        if(periodType == 12){
            if(parseFloat(cur_month) < 9){
                months_arr.push('10/'+(parseFloat(cur_year)-1));
                months_arr.push('11/'+(parseFloat(cur_year)-1));
                months_arr.push('12/'+(parseFloat(cur_year)-1));
                months_arr.push('1/'+parseFloat(cur_year));
                months_arr.push('2/'+parseFloat(cur_year));
                months_arr.push('3/'+parseFloat(cur_year));
                months_arr.push('4/'+parseFloat(cur_year));
                months_arr.push('5/'+parseFloat(cur_year));
                months_arr.push('6/'+parseFloat(cur_year));
                months_arr.push('7/'+parseFloat(cur_year));
                months_arr.push('8/'+parseFloat(cur_year));
                months_arr.push('9/'+parseFloat(cur_year));
            }else{
                months_arr.push('10/'+parseFloat(cur_year));
                months_arr.push('11/'+parseFloat(cur_year));
                months_arr.push('12/'+parseFloat(cur_year));
                months_arr.push('1/'+(parseFloat(cur_year)+1));
                months_arr.push('2/'+(parseFloat(cur_year)+1));
                months_arr.push('3/'+(parseFloat(cur_year)+1));
                months_arr.push('4/'+(parseFloat(cur_year)+1));
                months_arr.push('5/'+(parseFloat(cur_year)+1));
                months_arr.push('6/'+(parseFloat(cur_year)+1));
                months_arr.push('7/'+(parseFloat(cur_year)+1));
                months_arr.push('8/'+(parseFloat(cur_year)+1));
                months_arr.push('9/'+(parseFloat(cur_year)+1));
            }
        }else if(periodType == 6){
            if(parseFloat(cur_month) < 2){
                months_arr.push('10/'+(parseFloat(cur_year)-1));
                months_arr.push('11/'+(parseFloat(cur_year)-1));
                months_arr.push('12/'+(parseFloat(cur_year)-1));
                months_arr.push('1/'+parseFloat(cur_year));
                months_arr.push('2/'+parseFloat(cur_year));
                months_arr.push('3/'+parseFloat(cur_year));
            } else{
                months_arr.push('4/'+parseFloat(cur_year));
                months_arr.push('5/'+parseFloat(cur_year));
                months_arr.push('6/'+parseFloat(cur_year));
                months_arr.push('7/'+parseFloat(cur_year));
                months_arr.push('8/'+parseFloat(cur_year));
                months_arr.push('9/'+parseFloat(cur_year));
            }
        }

        // return JSON.stringify(months_arr)
        return months_arr
    }


    // -----------------fetches-----------------
    //--1--
    function fetchTotalOVCsEver(org_level,area_id){
         $.ajax({
            type: 'GET',
            url: '/get_total_ovc_ever/'+org_level+'/'+area_id+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
             //   displayTotalOVCsEver(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }
    function fetchCPARAResults(org_level,area_id,funding_partner,funding_part_id,period_type){

        var the_url = '/get_cpara_results/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/';
        $.ajax({
            type: 'GET',
            url: the_url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                var score_is_17 = 0;
                var score_not = 0;
                var period;

                $.each(data, function (indexx, one_res) {
                    // alert(one_res);
                    if(one_res.cpara_score == 17){
                        score_is_17 += one_res.cboactive
                    }else{
                        score_not += one_res.cboactive
                    }
                    period=one_res.period
                })
                var data_p = [];
                data_p['x'] = score_is_17;
                data_p['y'] = score_not;
                data_p['period']=period;
                displayCPARAResults(data_p);
                console.log('score_is_17='+score_is_17 + ' ||| && score_not=' + score_not);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }

    function fetchHHScoringCat(org_level,area_id,funding_partner,funding_part_id,period_type){

        var the_url = '/get_hh_categorization/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/';
        $.ajax({
            type: 'GET',
            url: the_url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
            displayHHScoringCat(data);
            console.log("the data is: ========>");
            console.log(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }


    //--1--



   function fetchPerBenchmarkDomainPerformance(org_level,area_id,funding_partner,funding_part_id,period_type){

        var the_url = '/get_per_domain_results/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/';
        $.ajax({
            type: 'GET',
            url: the_url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
            displayPerBenchmarkDomainPerformance(data);

            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }




    function fetchPerBenchmarkPerformance(org_level,area_id,funding_partner,funding_part_id,period_type){

        var the_url = '/get_benchmark_results/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/';
        $.ajax({
            type: 'GET',
            url: the_url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
            console.log("the data is: ========>");
            console.log(data);
            displayDomainPerformance(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
   }


    //--2--
    function fetchTotalOVCsEverExited(org_level,area_id){
        $.ajax({
           type: 'GET',
           url: '/get_total_ovc_ever_exited/'+org_level+'/'+area_id+'/',
           contentType: 'application/json; charset=utf-8',
           dataType: 'json',
           encode: true,
           success: function (data, textStatus, jqXHR) {
             //  displayTotalOVCsEverExited(data);
           },
           error: function (response, request) {
               console.log(response.responseText);
           }
       });
   }
   function fetchDomainPerformance(org_level,area_id,funding_partner,funding_part_id,period_type){

        var the_url = '/get_exited_ovcs_by_period/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/';
        $.ajax({
            type: 'GET',
            url: the_url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
            console.log("the data is: ========>");
            console.log(data);
            displayDomainPerformance(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
   }

   //--2--

   //--3--
   function fetchWoBCertAtEnrol(org_level,area_id){
        $.ajax({
            type: 'GET',
            url: '/get_total_wout_bcert_at_enrol/'+org_level+'/'+area_id+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
             //   displayWoBCertAtEnrol(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }
   function fetchServedBCert(org_level,area_id,months_arr){
        var month_year = [];
        $.each(months_arr, function (indx, monthyr) {
            var m_y_array = [];
            var dateparts = monthyr.split('/', 2);
            var the_month = dateparts[0];
            if(parseFloat(the_month) < 10){the_month = '0'+the_month;}
            var the_year = dateparts[1];
            m_y_array.push(the_month);
            m_y_array.push(the_year);
            month_year.push(m_y_array);
        });
        $.ajax({
            type: 'GET',
            url: '/get_served_bcert_by_period/'+org_level+'/'+area_id+'/'+encodeURIComponent(JSON.stringify(month_year))+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                
             //   displayServedBCert(data,months_arr);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }

        });
    }
    function fetchWithBCertToDate(org_level,area_id){
        $.ajax({
            type: 'GET',
            url: '/get_total_w_bcert_2date/'+org_level+'/'+area_id+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
             //   displayWithBCertToDate(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }
    function fetchServedBCertAftEnrol(org_level,area_id){
        $.ajax({
            type: 'GET',
            url: '/get_total_s_bcert_aft_enrol/'+org_level+'/'+area_id+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
             //   displayServedBCertAftEnrol(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }
    function fetchU5ServedBcert(org_level,area_id,months_arr){
        var month_year = [];
        $.each(months_arr, function (indx, monthyr) {
            var m_y_array = [];
            var dateparts = monthyr.split('/', 2);
            var the_month = dateparts[0];
            if(parseFloat(the_month) < 10){the_month = '0'+the_month;}
            var the_year = dateparts[1];
            m_y_array.push(the_month);
            m_y_array.push(the_year);
            month_year.push(m_y_array);
        });
         $.ajax({
            type: 'GET',
            url: '/get_u5_served_bcert_by_period/'+org_level+'/'+area_id+'/'+encodeURIComponent(JSON.stringify(month_year))+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                
               // displayU5ServedBcert(data,months_arr);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
    
        });
    }
   //--3--
    // -----------------fetches-----------------
    
    
    

    // -----------------display-----------------
    //--1--
    function displayCPARAResults(data, months_arr){

            var elementId="cpara_results";
            var the_title = 'Case Plan Achievement Assessment Results '+data['period'];
            var on_path = data['y'];
            var achieved_cp = data['x'];
            var the_data = { name: 'Result', data: [{name: 'On path to CPA',y: on_path}, {name: 'Caseplan achieved',y: achieved_cp}] };
            var the_series = [the_data];
            pieChart(elementId,the_title,the_series)

    }
    function displayHHScoringCat(data, months_arr){

            var elementId="hh_scoring_categorization";
            var the_title = 'Categorization of HHs scoring 0-16 ';

            var score_8_16;
            var score_0_7;

            var period;
            for(let i = 0; i < data.length; i++){
                period = data[i].period;

               let value = data[i].graduationpath;
                console.log(data[i].count);
               if(value=="8-16"){
                    score_8_16 =  parseInt(data[i].count);
               }else if(value=="0-7"){
                    score_0_7 =  parseInt(data[i].count);
               }

            }
           the_title=the_title+period;
            var total=score_8_16+score_0_7;
            score_8_16=(score_8_16*100)/total;
            score_0_7=(score_0_7*100)/total;
            var the_data = { name: 'Result', data: [{name: 'Score 0-7',y: score_0_7}, {name: 'Score 8-16',y: score_8_16}] };
            var the_series = [the_data];
            pieChart(elementId,the_title,the_series)

    }


    function displayPerBenchmarkDomainPerformance(data){

        var elementId_overall="dmn_perf_overall";
        var the_title_overall = 'Overall domains performance '+data[0].period;
        var o_healthy_data=data[0].HEALTHY;
        var o_stable_data=data[0].SAFE;
        var o_safe_data=data[0].SCHOOLED;
        var o_schooled_data=data[0].STABLE;
        var o_x_values={name: 'Domain',data: [o_healthy_data, o_stable_data, o_safe_data, o_schooled_data]};
        var o_x_axis = ['Healthy','Stable','Safe','Schooled'];
        var the_series_overall = [o_x_values];
        barChart(elementId_overall,the_title_overall,o_x_axis,the_series_overall)
        //overall
        }


    function displayDomainPerformance(data){

        //healthy
        var elementId_healthy="dmn_perf_Healthy";
        var the_title_healthy = 'Healthy domain performance '+data[0].period;
        var health_x_axis = [
            "BM1: HIV Risk assessment done and HIV testing referrals completed",
            "BM2: Caregivers know the HIV+ status of the children they care as well as their own",
            "BM3: HIV+ persons in the household have been on ART for last 12 months",
            "BM4: Enrolled women/ adolescent girls who are/become pregnant receive HIV testing",
            "BM5: Adolescents and their caregivers have knowledge to decrease their HIV risk",
            "BM6: Children living with chronic illness/disability receive treatment"
        ];
        console.log("data access ========>");
        console.log(data[0].BMRK1);
        var health_x_values = {name: 'Healthy', data: [parseInt(data[0].BMRK1),
                                parseInt(data[0].BMRK2), parseInt(data[0].BMRK3),
                                parseInt(data[0].BMRK4), parseInt(data[0].BMRK5),
                                parseInt(data[0].BMRK6)] }
        var the_series_healthy = [health_x_values];
        columnChart(elementId_healthy,the_title_healthy,health_x_axis,the_series_healthy)
        //healthy
        
        //stable
        var elementId_stable="dmn_perf_Stable";
        var the_title_stable = 'Stable domain performance '+data[0].period;
        var stable_x_axis = [
            "BM7: HH able to provide a minimum of two meals/day",
            "BM8: HH able to pay for child(ren)’s basic needs",
            "BM9: HH able to pay for emergency expenses.",
            "BM10:The caregiver has demonstrated knowledge on access to critical services"
        ];
        var stable_x_values = {name: 'Stable', data: [parseInt(data[0].BMRK7), parseInt(data[0].BMRK8), parseInt(data[0].BMRK9), parseInt(data[0].BMRK10)]}
        var the_series_stable = [stable_x_values];
        barChart(elementId_stable,the_title_stable,stable_x_axis,the_series_stable)
        //stable

        //safe
        var elementId_safe="dmn_perf_Safe";
        var the_title_safe = 'Safe domain performance '+data[0].period;
        var safe_x_axis = [
            "BM11: Child-headed HHs have received child and social protection services",
            "BM12: All children in the HH able to participate in daily activities and engage with others",
            "BM13: Children at risk of abuse have been referred to and are receiving appropriate services",
            "BM14: Caregivers can identify individual or group providing social or emotional support",
            "BM15: Caregivers have completed a parenting skills or able to clearly articulate positive parenting"
        ];
        var safe_x_values = {name: 'Safe', data: [parseInt(data[0].BMRK11), parseInt(data[0].BMRK12),
                                                  parseInt(data[0].BMRK13), parseInt(data[0].BMRK14), parseInt(data[0].BMRK15)]}
        var the_series_safe = [safe_x_values];
        columnChart(elementId_safe,the_title_safe,safe_x_axis,the_series_safe)
        //safe
        
        //schooled
        var elementId_schooled="dmn_perf_Schooled";
        var the_title_schooled = 'Schooled domain performance '+data[0].period;
        var schooled_x_axis = [
            "BM16: All 6-17 children enrolled and attend school regularly",
            "BM17: Adolescents enrolled in vocational attend regularly"
        ];
        var schooled_x_values = {name: 'Schooled', data: [parseInt(data[0].BMRK16), parseInt(data[0].BMRK17)]}
        var the_series_schooled = [schooled_x_values];
        barChart(elementId_schooled,the_title_schooled,schooled_x_axis,the_series_schooled)
        //schooled

            

    }

    // -----------------display-----------------
