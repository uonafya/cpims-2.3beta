    $(document).ready(function () {
        var org_level='national';
        // 1
        fetchTotalOVCsEver('national',"");
        fetchNewOVCRegs('national',"");
        fetchActiveOVCs('national',"");
        // 1

        // 2
        fetchTotalOVCsEverExited('national',"");
        fetchExitedOVCRegs('national',"");
        fetchExitedHseld('national',"");
        // 2

        // 3
        fetchWoBCertAtEnrol('national',"")
        fetchServedBCert('national',"")
        fetchWithBCertToDate('national',"")
        fetchServedBCertAftEnrol('national',"")
        fetchU5ServedBcert('national',"")
        // 3
    });
    
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
    function fetchNewOVCRegs(org_level,area_id){
         $.ajax({
            type: 'GET',
            url: '/hiv_stats_pub_data/'+org_level+'/'+area_id+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                displayNewOVCRegs(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }
    function fetchActiveOVCs(org_level,area_id){
         $.ajax({
            type: 'GET',
            url: '/hiv_stats_pub_data/'+org_level+'/'+area_id+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                
                displayActiveOVCs(data);
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
   function fetchExitedOVCRegs(org_level,area_id){
        $.ajax({
           type: 'GET',
           url: '/hiv_stats_pub_data/'+org_level+'/'+area_id+'/',
           contentType: 'application/json; charset=utf-8',
           dataType: 'json',
           encode: true,
           success: function (data, textStatus, jqXHR) {
               displayExitedOVCRegs(data);
           },
           error: function (response, request) {
               console.log(response.responseText);
           }
       });
   }
   function fetchExitedHseld(org_level,area_id){
        $.ajax({
           type: 'GET',
           url: '/hiv_stats_pub_data/'+org_level+'/'+area_id+'/',
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
                displayWoBCertAtEnrol(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }
        });
    }
   function fetchServedBCert(org_level,area_id){
        $.ajax({
            type: 'GET',
            url: '/hiv_stats_pub_data/'+org_level+'/'+area_id+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                
                displayServedBCert(data);
            },
            error: function (response, request) {
                console.log(response.responseText);
            }

        });
    }
    function fetchWithBCertToDate(org_level,area_id){
        $.ajax({
            type: 'GET',
            url: '/get_total_ovc_ever/'+org_level+'/'+area_id+'/',
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
            url: '/get_total_ovc_ever/'+org_level+'/'+area_id+'/',
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
    function fetchU5ServedBcert(org_level,area_id){
         $.ajax({
            type: 'GET',
            url: '/hiv_stats_pub_data/'+org_level+'/'+area_id+'/',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            encode: true,
            success: function (data, textStatus, jqXHR) {
                
                displayU5ServedBcert(data);
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
    function displayNewOVCRegs(data){
        // $.each(data, function (index, objValue) {
           var elementId="new_ovc_registrations";
           var the_x_axis= ['Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018', 'May 2018']
           var the_title = 'New OVCs within period';
           var the_series = [
                                { name: 'Female', data: [3896, 3979, 1798, 7687, 4565] },
                                { name: 'Male', data: [1396, 1979, 7908, 4767, 5365] }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }
    function displayActiveOVCs(data){
        // $.each(data, function (index, objValue) {
           var elementId="active_ovc";
           var the_x_axis= ['Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018', 'May 2018']
           var the_title = 'Active OVCs within period';
           var the_series = [
                                { name: 'Female', data: [3896, 3979, 9798, 1687, 565] },
                                { name: 'Male', data: [396, 979, 798, 767, 565] }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
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
    function displayExitedOVCRegs(data){
        // $.each(data, function (index, objValue) {
           var elementId="ovc_exits";
           var the_x_axis= ['Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018', 'May 2018']
           var the_title = 'OVC Exited from the program withn period';
           var the_series = [
                                { name: 'Female', data: [3896, 3979, 1798, 7687, 4565] },
                                { name: 'Male', data: [1396, 1979, 7908, 4767, 5365] }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }
    function displayExitedHseld(data){
        // $.each(data, function (index, objValue) {
           var elementId="hsehld_exits";
           var the_x_axis= ['Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018', 'May 2018']
           var the_title = 'HouseHolds Exited from the program within period';
           var the_series = [
                                { name: 'Female', data: [3896, 3979, 9798, 1687, 565] },
                                { name: 'Male', data: [396, 979, 798, 767, 565] }
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
    function displayServedBCert(data){
        // $.each(data, function (index, objValue) {
           var elementId="ovc_s_bcert";
           var the_x_axis= ['Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018', 'May 2018']
           var the_title = 'OVC served with Birth Certificate within period';
           var the_series = [
                                { name: 'Female', data: [1196, 979, 3791, 3680, 3565] },
                                { name: 'Male', data: [2396, 3979, 7798, 2767, 7565] }
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
    function displayU5ServedBcert(data){
        // $.each(data, function (index, objValue) {
           var elementId="ovc_u5_s_bcert";
           var the_x_axis= ['Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018', 'May 2018']
           var the_title = 'OVC 5yrs and below served with Birth Certificate within period';
           var the_series = [
                                { name: 'Female', data: [1987, 2500, 2687, 1230, 4021] },
                                { name: 'Male', data: [4570, 2000, 6798, 3290, 5675] }
                            ];
    
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }
    //--3--
    // -----------------display-----------------
    
    