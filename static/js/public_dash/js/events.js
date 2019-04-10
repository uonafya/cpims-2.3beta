$(document).ready(function () {

    var chartsContext = {
        currentOrgLevel: "national"
    };

    $( ".dropdown-menu li" ).click(function(event) {
        if( $(this).attr("id") == 'national' && chartsContext.currentOrgLevel !='national'){
            fetchHivStatsFromServer('national');
            chartsContext.currentOrgLevel ='national'
        }else if( $(this).attr("id") == 'county' && chartsContext.currentOrgLevel !='county'){
            fetchHivStatsFromServer('county');
            chartsContext.currentOrgLevel ='county';
        }else if( $(this).attr("id") == 'constituency' && chartsContext.currentOrgLevel !='constituency'){
            fetchHivStatsFromServer('constituency');
            chartsContext.currentOrgLevel ='constituency';
        }else if( $(this).attr("id") == 'ward' && chartsContext.currentOrgLevel !='ward'){
            fetchHivStatsFromServer('ward');
            chartsContext.currentOrgLevel ='ward';
        }else {
        }

    });
});