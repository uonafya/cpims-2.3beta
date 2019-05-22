$(document).ready(function () {
var org_level='national';
fetchOvcServedStatusStats('national',"","","","annual");
});

function fetchOvcServedStatusStats(org_level,area_id,funding_partner,funding_part_id,period_type){
     $.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/get_ovc_served_stats/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/', // the url from server we that we want to use
        contentType: 'application/json; charset=utf-8',
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            displayOvcServedWith1or2Services(data);
            displayOvcServedWith3orMoreServices(data);
            displayNotServed(data);
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            alert("error");
            console.log(response.responseText);
        }

    });
}


function displayOvcServedWith1or2Services(data){

        // $.each(data, function (index, objValue) {
           var elementId="ovc_served_with_1or2_services";
           var the_x_axis= []
           var the_title = 'OVC served with 1 or 2 services';

            var female={name: 'female',data: []};
            var male={name: 'male',data: []};
            $.each(data, function (index, objValue) {

                if(objValue['service']=='1or2 Services'){
                    the_x_axis.push(objValue['period']);
                    if(objValue['gender']=='Male') male['data'].push(objValue['cboactive']);
                    else female['data'].push(objValue['cboactive']);
                }

            });

           var the_series = [
                                female,
                                male
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }

    function displayOvcServedWith3orMoreServices(data){

        // $.each(data, function (index, objValue) {
           var elementId="ovc_served_with_3_services";
           var the_x_axis= []
           var the_title = 'OVC served with 3 or more services';

            var female={name: 'female',data: []};
            var male={name: 'male',data: []};
            $.each(data, function (index, objValue) {

                if(objValue['service']=='3orMore Services'){
                    the_x_axis.push(objValue['period']);
                    if(objValue['gender']=='Male') male['data'].push(objValue['cboactive']);
                    else female['data'].push(objValue['cboactive']);
                }

            });

           var the_series = [
                                female,
                                male
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }

    function displayNotServed(data){

        // $.each(data, function (index, objValue) {
           var elementId="not_served";
           var the_x_axis= []
           var the_title = 'Ovc Not Served';

            var female={name: 'female',data: []};
            var male={name: 'male',data: []};
            $.each(data, function (index, objValue) {
                console.log("gone ");
                console.log(objValue['service']);
                if(objValue['service']=='Not Served'){
                    the_x_axis.push(objValue['period']);
                    if(objValue['gender']=='Male') male['data'].push(objValue['cboactive']);
                    else female['data'].push(objValue['cboactive']);
                }
            });

           var the_series = [
                                female,
                                male
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }



