$(document).ready(function () {
var org_level='national';
fetchHivStatsFromServer('national',"");
fetchActiveOvcHivStats('national',"");
displayOvcTestedWithinPeriod("");
displayHivPstvOvcTestedwithinperiod("");
});

var legend = {}
legend.verticalAlign='top';
legend.x=-30;
legend.y=25
legend.layout='horizontal';

function fetchHivStatsFromServer(org_level,area_id){
     $.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/hiv_stats_pub_data/'+org_level+'/'+area_id+'/', // the url from server we that we want to use
        contentType: 'application/json; charset=utf-8',
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            displayHivStatus(data);
            displayArtStatus(data);
            displayOVCEverTestedForHIV(data);
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            console.log(response.responseText);
        }

    });
}

function fetchActiveOvcHivStats(org_level,area_id){
     $.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/hiv_stats_ovc_active/'+org_level+'/'+area_id+'/', // the url from server we that we want to use
        contentType: 'application/json; charset=utf-8',
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
           displayActiveOvcHivStatus(data);
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            console.log(response.responseText);
        }
    });
}


function displayOvcTestedWithinPeriod(data){
        // $.each(data, function (index, objValue) {
           var elementId="Ovc_Tested_Within_Period";
           var the_x_axis= ['Oct 2018', 'Nov 2018', 'Dec 2018', 'Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019']
           var the_title = 'OVC TESTED WITHIN PERIOD';
           var the_series = [
                                { name: 'Demo Female', data: [3896, 3979, 1798, 7687, 4565,7908, 4767] },
                                { name: 'Demo Male', data: [1396, 1979, 7908, 4767, 5365, 3979, 1798] }
                            ];
            barChart(elementId,the_title,the_x_axis,the_series)
        // });
    }

function displayHivPstvOvcTestedwithinperiod(data){
        // $.each(data, function (index, objValue) {
           var elementId="Hiv_Pstv_Ovc_Tested_within_period";
           var the_x_axis= ['Oct 2018', 'Nov 2018', 'Dec 2018', 'Jan 2019', 'Feb 2019', 'Mar 2019', 'Apr 2019']
           var the_title = 'HIV+ OVC Tested within period';
           var the_series = [
                                { name: 'Demo Female', data: [3896, 3979, 1798, 7687, 4565,7908, 4767] },
                                { name: 'Demo Male', data: [1396, 1979, 7908, 4767, 5365, 3979, 1798] }
                            ];

            barChart(elementId,the_title,the_x_axis,the_series)
        // });
 }

function displayOVCEverTestedForHIV(data){
    $.each(data, function (index, objValue) {
       var elementId="ever_tested";
       var categoriee= ['Ever Tested for HIV']
       var titlee = 'OVC EVER TESTED FOR HIV';
       var female=objValue.hiv_positive_f+objValue.HIV_negative_f;
       var male=objValue.hiv_positive_m+objValue.HIV_negative_m;
       var serie = [{
                        name: 'Female',
                        data: [female]
                    }, {
                        name: 'Male',
                        data: [male]
                    }];

       stackedBar(elementId,titlee,categoriee,serie,'normal',legend);
    });
}


function displayActiveOvcHivStatus(data){
    $.each(data, function (index, objValue) {
       var elementId="active_ovc_hiv_status";
       var categoriee= ['Active Ovc with <br/> Known HIV Status','HIV+', 'HIV-','ACTIVE OVC HIV+ on ART', 'ACTIVE OVC HIV+ NOT on ART']
       var titlee = 'ACTIVE OVC HIV STATUS';
       var female=objValue.hiv_positive_f+objValue.HIV_negative_f;
       var male=objValue.hiv_positive_m+objValue.HIV_negative_m;
       var serie = [{
                        name: 'Female',
                        data: [female,objValue.hiv_positive_f, objValue.HIV_negative_f, objValue.HIV_positive_on_arv_f,objValue.HIV_positive_not_on_arv_f]
                    }, {
                        name: 'Male',
                        data: [male,objValue.hiv_positive_m, objValue.HIV_negative_m, objValue.HIV_positive_on_arv_m, objValue.HIV_positive_not_on_arv_m]
                    }];

       stackedBar(elementId,titlee,categoriee,serie,'normal',legend);
    });
}


function displayHivStatus(data){
    $.each(data, function (index, objValue) {
       var elementId="hiv_status_chart";
       var categoriee= ['HIV+', 'HIV-', 'HIV Status Not Known']
       var titlee = 'HIV STATUS';
       var serie = [{
                        name: 'Female',
                        data: [objValue.hiv_positive_f, objValue.HIV_negative_f, objValue.HIV_unknown_status_f]
                    }, {
                        name: 'Male',
                        data: [objValue.hiv_positive_m, objValue.HIV_negative_m, objValue.HIV_unknown_status_m]
                    }];

       stackedBar(elementId,titlee,categoriee,serie,'normal',legend);
    });
}

function displayArtStatus(data){
    $.each(data, function (index, objValue) {
       //var ward=new Ward(objValue.name);

       var elementId="art_status_chart";
       var categoriee= ['HIV+', 'HIV+ on ARV', 'HIV+ Not on ARV']
       var titlee = 'ART STATUS';
       var serie = [{
                        name: 'Female',
                        data: [objValue.hiv_positive_f, objValue.HIV_positive_on_arv_f, objValue.HIV_positive_not_on_arv_f]
                    }, {
                        name: 'Male',
                        data: [objValue.hiv_positive_m, objValue.HIV_positive_on_arv_m, objValue.HIV_positive_not_on_arv_m]
                    }];
       stackedBar(elementId,titlee,categoriee,serie,'normal',legend);
    });
}



