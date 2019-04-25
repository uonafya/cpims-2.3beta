    $(document).ready(function () {
        var org_level='national';
        var months_arr=getMonths();
        // 1
        fetchTotalOVCsEver('national',"");
        fetchNewOVCRegs('national',"",months_arr);
        fetchActiveOVCs('national',"",months_arr);
        // 1

        // 2
        fetchTotalOVCsEverExited('national',"");
        fetchExitedOVCRegs('national',"",months_arr);
        fetchExitedHseld('national',"",months_arr);
        // 2

        // 3
        fetchWoBCertAtEnrol('national',"")
        fetchServedBCert('national',"",months_arr)
        fetchWithBCertToDate('national',"")
        fetchServedBCertAftEnrol('national',"")
        fetchU5ServedBcert('national',"",months_arr)
        // 3

    });

    $('#period').change(function (e) { 
        var per_val = $(this).find('option:selected').val();
        var months_arr2=getMonths(per_val);
        // 1
        fetchNewOVCRegs('national',"",months_arr2);
        fetchActiveOVCs('national',"",months_arr2);
        // 1
        // 2
        fetchExitedOVCRegs('national',"",months_arr2);
        fetchExitedHseld('national',"",months_arr2);
        // 2
        // 3
        fetchServedBCert('national',"",months_arr2);
        fetchU5ServedBcert('national',"",months_arr2);
        // 3        
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
                displayTotalOVCsEver(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }
    function fetchNewOVCRegs(org_level,area_id,months_arr){
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
            url: '/get_new_ovcregs_by_period/'+org_level+'/'+area_id+'/'+encodeURIComponent(JSON.stringify(month_year))+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                displayNewOVCRegs(data, months_arr);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }

    function fetchActiveOVCs(org_level,area_id,months_arr){
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
            url: '/get_active_ovcs_by_period/'+org_level+'/'+area_id+'/'+encodeURIComponent(JSON.stringify(month_year))+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                displayActiveOVCs(data,months_arr);
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
               displayTotalOVCsEverExited(data);
           },
           error: function (response, request) {
               console.log(response.responseText);
           }
       });
   }
   function fetchExitedOVCRegs(org_level,area_id,months_arr){
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
           url: '/get_exited_ovcs_by_period/'+org_level+'/'+area_id+'/'+encodeURIComponent(JSON.stringify(month_year))+'/',
           contentType: 'application/json; charset=utf-8',
           dataType: 'json',
           encode: true,
           success: function (data, textStatus, jqXHR) {
               displayExitedOVCRegs(data, months_arr);
           },
           error: function (response, request) {
               console.log(response.responseText);
           }
       });
   }
   function fetchExitedHseld(org_level,area_id,months_arr){
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
           url: '/get_exited_hsehlds_by_period/'+org_level+'/'+area_id+'/'+encodeURIComponent(JSON.stringify(month_year))+'/',
           contentType: 'application/json; charset=utf-8',
           dataType: 'json',
           encode: true,
           success: function (data, textStatus, jqXHR) {
               
               displayExitedHseld(data,months_arr);
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
                displayWoBCertAtEnrol(data);
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
                
                displayServedBCert(data,months_arr);
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
                displayWithBCertToDate(data);
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
                displayServedBCertAftEnrol(data);
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
                
                displayU5ServedBcert(data,months_arr);
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
    function displayNewOVCRegs(the_data, months_arr){
           var elementId="new_ovc_registrations";
           var the_x_axis= months_arr
           var the_title = 'New OVCs within period';
           var the_series = [
                                // { name: 'Female', data: [3896, 3979, 1798, 7687, 4565] },
                                // { name: 'Male', data: [1396, 1979, 7908, 4767, 5365] }
                                { name: 'OVCs', data: the_data }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series);
    }
    function displayActiveOVCs(the_data, months_arr){
           var elementId="active_ovc";
           var the_x_axis= months_arr;
           var the_title = 'Active OVCs within period';           
           var the_series = [
                                // { name: 'Female', data: [3896, 3979, 9798, 1687, 565] },
                                // { name: 'Male', data: [396, 979, 798, 767, 565] }
                                { name: 'OVCs', data: the_data }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series);
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
    function displayExitedOVCRegs(the_data, months_arr){
           var elementId="ovc_exits";
           var the_x_axis= months_arr;
           var the_title = 'OVC Exited from the program withn period';
           var the_series = [
                                // { name: 'Female', data: [3896, 3979, 1798, 7687, 4565] },
                                // { name: 'Male', data: [1396, 1979, 7908, 4767, 5365] }
                                { name: 'OVCs', data: the_data }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series)
    }
    function displayExitedHseld(data, months_arr){
        // $.each(data, function (index, objValue) {
           var elementId="hsehld_exits";
           var the_x_axis= months_arr
           var the_title = 'HouseHolds Exited from the program within period';
           var the_series = [
                                // { name: 'Female', data: [3896, 3979, 9798, 1687, 565] },
                                // { name: 'Male', data: [396, 979, 798, 767, 565] }
                                { name: 'Households', data: data }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
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
                                { name: 'OVCs', data: data }
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
                                { name: 'OVCs', data: data }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }
    //--3--
    // -----------------display-----------------
    
    
    //sleep function
    // function sleep(milliseconds) {
    // 	var start = new Date().getTime();
    // 	for (var i = 0; i < 1e7; i++) {
    // 		if ((new Date().getTime() - start) > milliseconds) {
    // 			break;
    // 		}
    // 	}
    // }