$(document).ready(function () {
var org_level='national';
fetchHivStatsFromServer('national',"");
fetchActiveOvcHivStats('national',"");
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



