$(document).ready(function () {
var org_level='national';
fetchOvcServedStatusStats('national',"","","","");
});

function fetchOvcServedStatusStats(org_level,area_id,funding_partner,funding_part_id,period_type){
     $.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/get_ovc_served_stats/'+org_level+'/'+area_id+'/'+funding_partner+'/'+funding_part_id+'/'+period_type+'/', // the url from server we that we want to use
        contentType: 'application/json; charset=utf-8',
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            displayOvcServedStatusStat(data);
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            alert("error");
            console.log(response.responseText);
        }

    });
}

function displayOvcServedStatusStat(cascadeData){
    var elementId="notKnownAtEnrolment";
    var categoriee= ['HIV Status', 'Art Status', 'Suppression']
    var titlee = 'CASCADE 90-90-90';
    $.each(cascadeData, function (index, objValue) {
            console.log(objValue.ovc_HSTP_rate);
             var serie = [  {
                                name: 'Unknown Status',
                                data: [[0,parseFloat(objValue.ovc_unknown_count_rate)]],
                                stack: 'one'
                            }, {
                                name: 'Negative',
                                data: [[0,parseFloat(objValue.ovc_HSTN_rate)]],
                                stack: 'one'
                            }, {
                                name: 'Positive',
                                data: [[0,parseFloat(objValue.ovc_HSTP_rate)]],
                                stack: 'one'
                            }, {
                                name: 'Not on ART',
                                data: [[1,parseFloat(objValue.not_on_art_rate)]],
                                stack: 'two'
                            }, {
                                name: 'On ART',
                                data: [[1,parseFloat(objValue.on_art_rate)]],
                                stack: 'two'
                            }, {
                                name: 'Suppressed',
                                data: [[3,parseFloat(objValue.suppresed_rate) ]],
                                stack: 'two'
                            }, {
                                name: 'Not Suppressed',
                                data: [[3,parseFloat(objValue.not_suppresed_rate)]],
                                stack: 'two'
                            }];
           var legend = {}
           legend.verticalAlign='bottom';
           legend.x=-5;
           legend.y=15
           legend.layout='vertical';
           stackedBar(elementId,titlee,categoriee,serie,'percent',legend);

     });
}


