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


//    fetchActiveOVCs(levl,ouid,months_array,fcc,fcc_val);
//    fetchTotalOVCsEver('national',"0");
//
//    fetchExitedOVCRegs(levl,ouid,months_array,fcc,fcc_val);
//    fetchExitedHseld(levl,ouid,months_array,fcc,fcc_val);
//    fetchTotalOVCsEverExited('national',"0");
//
//    fetchServedBCert(levl,ouid,months_array);
//    fetchU5ServedBcert(levl,ouid,months_array);
//    fetchWoBCertAtEnrol('national',"0")
//    fetchServedBCert('national',"0",months_array)
//    fetchWithBCertToDate('national',"0")
//    fetchServedBCertAftEnrol('national',"0")
//    fetchU5ServedBcert('national',"0",months_array)

    }



$(document).ready(function () {
    //ouChange('national',"0",'none','none');
    fetchNewOVCRegs('national',"","","","annual");
    fetchExitedAndActiveOVCRegs('national',"","","","annual");
    fetchExitedHseld('national',"","","","annual");
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
    function fetchNewOVCRegs(org_level,area_id,funding_partner,funding_part_id,period_type){

        var the_url = '/get_new_ovcregs_by_period/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/';
        $.ajax({
            type: 'GET',
            url: the_url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
            console.log("the data is: ========>");
            console.log(data);
            displayNewOVCRegs(data);

            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }


    //--1--

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
   function fetchExitedAndActiveOVCRegs(org_level,area_id,funding_partner,funding_part_id,period_type){

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
            displayExitedOVCRegs(data);
            displayActiveOVCs(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
   }

   function fetchExitedHseld(org_level,area_id,funding_partner,funding_part_id,period_type){
        var the_url = '/get_exited_hsehlds_by_period/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/';
        $.ajax({
            type: 'GET',
            url: the_url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {

            displayExitedHseld(data);
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
    function displayTotalOVCsEver(data){
        var val = data;
        var elementId="all_ovc_reg";
        // $.each(data, function (index, objValue) {
        //    val += objValue;
        // });
        $('#'+elementId).html(val);
    }
    function displayNewOVCRegs(data, months_arr){

           var elementId="new_ovc_registrations";
           var the_x_axis= []
           var the_title = 'New OVCs within period';

            var female={name: 'female',data: []};
            var male={name: 'male',data: []};
            $.each(data, function (index, objValue) {
                console.log(objValue);
                the_x_axis.push(objValue['period']);
                if(objValue['gender']=='Male') male['data'].push(objValue['count']);
                else female['data'].push(objValue['count']);
            });

           var the_series = [
                                female,
                                male
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)

    }

    function displayActiveOVCs(data){

           var elementId="active_ovc";
           var the_x_axis= []
           var the_title = 'Active OVCs within period';

            var female={name: 'female',data: []};
            var male={name: 'male',data: []};
            $.each(data, function (index, objValue) {
                console.log("The service =====>");
                console.log(objValue);
                the_x_axis.push(objValue['period']);
                if(objValue['active']==true){
                    if(objValue['gender']=='Male') male['data'].push(objValue['count']);
                    else female['data'].push(objValue['count']);
                }
            });

           var the_series = [
                                female,
                                male
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)

    }

    //--1--

    //--2--
    function displayTotalOVCsEverExited(data){
        var val = data;
        var elementId="all_ovc_exit";
        // $.each(data, function (index, objValue) {
        //    val += objValue;
        // });
        $('#'+elementId).html(val);
    }
    function displayExitedOVCRegs(data, months_arr){
           var elementId="ovc_exits";
           var the_x_axis= []
           var the_title = 'OVC Exited from the program within period';

            var female={name: 'female',data: []};
            var male={name: 'male',data: []};
            $.each(data, function (index, objValue) {
                console.log(objValue);
                the_x_axis.push(objValue['period']);
                if(objValue['active']==false){
                    if(objValue['gender']=='Male') male['data'].push(objValue['count']);
                    else female['data'].push(objValue['count']);
                }

            });

           var the_series = [
                                female,
                                male
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)
    }

    function displayExitedHseld(data, months_arr){
       var elementId="hsehld_exits";
       var the_x_axis= []
       var the_title = 'HouseHolds Exited from the program within period';

        var graph_data={name: 'House Hold',data: []};
        $.each(data, function (index, objValue) {
            the_x_axis.push(objValue['period']);
                graph_data['data'].push(objValue['count']);
        });

       var the_series = [
                            graph_data
                        ];
        barChart(elementId,the_title,the_x_axis,the_series);

    }
    //--2--

    //--3--
    function displayWoBCertAtEnrol(data){
        var val = data;
        var elementId="all_ovc_wout_bcert";
        // $.each(data, function (index, objValue) {
        //    val += objValue;
        // });
        $('#'+elementId).html(val);
    }
    function displayServedBCert(data,months_arr){
        // $.each(data, function (index, objValue) {
           var elementId="ovc_s_bcert";
           var the_x_axis= months_arr
           var the_title = 'OVC served with Birth Certificate within period';
           var the_series = [
                                // { name: 'Female', data: [1196, 979, 3791, 3680, 3565] },
                                // { name: 'Male', data: [2396, 3979, 7798, 2767, 7565] }
                                { name: 'DEMO', data: data }
                            ];

            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }
    function displayWithBCertToDate(data){
        var val = data;
        var elementId="all_ovc_w_bcert_2date";
        // $.each(data, function (index, objValue) {
        //    val += objValue;
        // });
        $('#'+elementId).html(val);
    }
    function displayServedBCertAftEnrol(data){
        var val = data;
        var elementId="all_ovc_s_bcert_aft_enrol";
        // $.each(data, function (index, objValue) {
        //    val += objValue;
        // });
        $('#'+elementId).html(val);
    }
    function displayU5ServedBcert(data,months_arr){
        // $.each(data, function (index, objValue) {
           var elementId="ovc_u5_s_bcert";
           var the_x_axis= months_arr
           var the_title = 'OVC 5yrs and below served with Birth Certificate within period';
           var the_series = [
                                // { name: 'Female', data: [1987, 2500, 2687, 1230, 4021] },
                                // { name: 'Male', data: [4570, 2000, 6798, 3290, 5675] }
                                { name: 'DEMO', data: data }
                            ];

            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }
    //--3--
    // -----------------display-----------------
