$(document).ready(function () {
var org_level='national';
fetchOvcServedStatusStats('national',"none","none","none","annual");
fetchAllOvc('national',"none","none","none","annual");
});


var totalMale=0;
var totalFemale=0;
var totalMaleServed=0;
var totalFemaleServed=0;

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
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            alert("error");
            console.log(response.responseText);
        }

    });
}


function fetchAllOvc(org_level,area_id,funding_partner,funding_part_id,period_type){
     $.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/get_all_ovcs/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/', // the url from server we that we want to use
        contentType: 'application/json; charset=utf-8',
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            displayAllOvc(data);
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            alert("error");
            console.log(response.responseText);
        }

    });
}


function displayAllOvc(data){

        // $.each(data, function (index, objValue) {
       var elementId="all_ovc";
       var the_x_axis= []
       var the_title = 'CBO Active ';

        var female={name: 'female',data: []};
        var male={name: 'male',data: []};
        var period;
        $.each(data, function (index, objValue) {
            period=objValue['period'];
            //the_x_axis.push(objValue['period']);
            if(objValue['gender']=='Male'){
                male['data'].push(objValue['cboactive']);
                totalMale=totalMale+objValue['cboactive'];
            }else {
                female['data'].push(objValue['cboactive']);
                totalFemale=totalFemale+objValue['cboactive'];
            }

        });
        the_title=the_title+period;
       displayNotServed();
       var the_series = [
                            female,
                            male
                        ];
        barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }


function displayOvcServedWith1or2Services(data){

        // $.each(data, function (index, objValue) {
           var elementId="ovc_served_with_1or2_services";
           var the_x_axis= []
           var the_title = 'OVC served with 1 or 2 services';

            var female={name: 'female',data: []};
            var male={name: 'male',data: []};
            var period;
            $.each(data, function (index, objValue) {
                period=objValue['period'];
                if(objValue['service']=='1or2 Services'){
                    the_x_axis.push(objValue['period']);
                    if(objValue['gender']=='Male'){

                        male['data'].push(objValue['cboactive']);
                        totalMaleServed=totalMaleServed+objValue['cboactive'];
                    }else{

                        female['data'].push(objValue['cboactive']);
                        totalFemaleServed=totalFemaleServed+objValue['cboactive'];
                    }

                }

            });
            the_title=the_title+period;
           displayNotServed()
           var the_series = [
                                female,
                                male
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }
    var period;
    function displayOvcServedWith3orMoreServices(data){

        // $.each(data, function (index, objValue) {
           var elementId="ovc_served_with_3_services";
           var the_x_axis= []
           var the_title = 'OVC served with 3 or more services ';

            var female={name: 'female',data: []};
            var male={name: 'male',data: []};

            $.each(data, function (index, objValue) {
                period=objValue['period'];
                if(objValue['service']=='3orMore Services'){
                    the_x_axis.push(objValue['period']);
                    if(objValue['gender']=='Male'){
                        male['data'].push(objValue['cboactive']);
                        totalMaleServed=totalMaleServed+objValue['cboactive'];
                    }
                    else {
                        female['data'].push(objValue['cboactive']);
                        totalFemaleServed=totalFemaleServed+objValue['cboactive'];
                    }
                }

            });
            the_title=the_title+period;
           displayNotServed();
           var the_series = [
                                female,
                                male
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }

    var counter=0;

    function displayNotServed(){

            if(counter<=1){
                counter=counter+1;

            }else{
               counter=0;

               var maleNotServed=totalMale-totalMaleServed;
               var femaleNotServed=totalFemale-totalFemaleServed;

               var elementId="not_served";
               var the_x_axis= []
               var the_title = 'Ovc Not Served '+period;

                var female={name: 'female',data: []};
                var male={name: 'male',data: []};

                male['data'].push(maleNotServed);
                female['data'].push(femaleNotServed);

               var the_series = [
                                    female,
                                    male
                                ];
                barChart(elementId,the_title,the_x_axis,the_series)

                totalMale=0;
                totalFemale=0;
                totalMaleServed=0;
                totalFemaleServed=0;

            }

    }



