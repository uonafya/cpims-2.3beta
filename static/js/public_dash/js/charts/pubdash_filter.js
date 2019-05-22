var localityApi='/get_locality_data/';
var cboApi= '/fetch_cbo_list/'
var localityData='';
var cboData='';
var selectedCountySiblingsList=''; //list of countituency in the selected county

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


$(document).ready(function () {
    initOrganisationUnitChosenDropDown('funding mechanism','#funding-mechanism');
    initOrganisationUnitChosenDropDown('cluster','#cluster-unit',"150px");
    initOrganisationUnitChosenDropDown('CBO','#cbo-unit',"150px");

});


function destroyChosenDropDownList(elementId) {
    try {
        $(elementId).chosen("destroy");
    } catch (err) {
        // console.log(err);
    }
}


function populateOrgunitList(data,elementId,empyList) {
    if(empyList){
        $(elementId).empty();
    }
    $(elementId).append("<option></option>");
    $.each(data, function (key, objValue) {
        var elementToAppend = '<option data-id="' + key + '" data-name="' + objValue.name + '">' + objValue.name + '</option>';
        $(elementId).append(elementToAppend);
    });
}


var initOrganisationUnitChosenDropDown = function initOrganisationUnitChosenDropDown(label,id, _width) {
    $(id).chosen({
        placeholder_text_single: "Select " + label + ": ",
        no_results_text: "No results found!",
        width: _width
    });
};



function cloneObject(obj) {
    var clone = {};
    for (var i in obj) {
        if (obj[i] != null && typeof (obj[i]) == "object")
            clone[i] = cloneObject(obj[i]);
        else
            clone[i] = obj[i];
    }
    return clone;
}


//county event handler
$('#county-organisation-unit').on('change', function (event) {
    var localityDataToDisplay= cloneObject(localityData);
    var selectedCountyId = $("#county-organisation-unit option:selected").attr('data-id');
    var selectedCountyName=$("#county-organisation-unit option:selected").attr('data-name');
    $('.org-unit-label').html(selectedCountyName);
    destroyChosenDropDownList('#countituency-organisation-unit');
    destroyChosenDropDownList('#ward-organisation-unit');

    $.each(localityData, function (key, objValue) {  // filter out countituency int that county
        if(key!=selectedCountyId){
            delete localityDataToDisplay[key];
        }
    });

    //enable sub county & ward list element; Load siblings subcounty and ward based on selected county
    $('#countituency-organisation-unit').prop("disabled", false); // Element(s) are now enabled.
    $('#ward-organisation-unit').prop("disabled", false); // Element(s) are now enabled.
    $.each(localityDataToDisplay, function( key, value ) {
        populateOrgunitList(value.siblings,'#countituency-organisation-unit',true);
        selectedCountySiblingsList=value.siblings;
        $.each(value.siblings, function( constituencyKey, constituencyValue ) {
            populateOrgunitList(constituencyValue.siblings,'#ward-organisation-unit',false);
        });
    });

    initOrganisationUnitChosenDropDown("ward","#ward-organisation-unit","200px");
    initOrganisationUnitChosenDropDown("sub county","#countituency-organisation-unit","200px");
    // fetchHivStatsFromServer('county',selectedCountyId);
    // fetchActiveOvcHivStats('county',selectedCountyId);
    // fetchCascade90FromServer('county',selectedCountyId);

    //-----reg-----
    ouChange('county',selectedCountyId,'none','none');    
    //-----reg-----
});


//sub county event handler
$('#countituency-organisation-unit').on('change', function (event) {
    // console.log($("#countituency-organisation-unit option:selected"));
    var selectedSubCountyId = $("#countituency-organisation-unit option:selected").attr('data-id');
    var selectedSubCountyName=$("#countituency-organisation-unit option:selected").attr('data-name');
    $('.org-unit-label').html(selectedSubCountyName);
    // fetchHivStatsFromServer('subcounty',selectedSubCountyId);
    // fetchActiveOvcHivStats('subcounty',selectedSubCountyId);
    // fetchCascade90FromServer('subcounty',selectedSubCountyId);

    //-----reg-----
        ouChange('subcounty',selectedSubCountyId,'none','none')
    //-----reg-----

    //change ward list based on selected counstiuency
    $.each(selectedCountySiblingsList, function( constituencyKey, constituencyValue ) {
        if(selectedSubCountyId==constituencyKey){
            destroyChosenDropDownList('#ward-organisation-unit');
            // console.log("county siblings to show wards ");
        // console.log(constituencyValue.siblings);
            populateOrgunitList(constituencyValue.siblings,'#ward-organisation-unit',true);
        }
    });
    initOrganisationUnitChosenDropDown("ward","#ward-organisation-unit","200px");
});

// ward event handler
$('#ward-organisation-unit').on('change', function (event) {
    // console.log($("#countituency-organisation-unit option:selected"));
    var selectedWardId = $("#ward-organisation-unit option:selected").attr('data-id');
    var selectedWardName=$("#ward-organisation-unit option:selected").attr('data-name');
    $('.org-unit-label').html(selectedWardName);
    // fetchHivStatsFromServer('ward',selectedWardId);
    // fetchActiveOvcHivStats('ward',selectedWardId);
    // fetchCascade90FromServer('ward',selectedWardId);

    //-----reg-----
        ouChange('ward',selectedWardId,'none','none');    
    //-----reg-----
});


$('#period').change(function (e) { 
    ouChange('national',"0",'none','none');
});

//funding mechanism event handler
$('#funding-mechanism').on('change', function (event) {
     var selectedPartnerId = $("#funding-mechanism option:selected").val();
     var selectedPartnerValue=$("#funding-mechanism option:selected").attr('data-value');
     if(selectedPartnerId.toLowerCase()==0){ //usaid
        destroyChosenDropDownList('#cluster-unit'); // to enable edit the raw html elements
        $('#cluster-unit').prop("disabled", false); // Element(s) are now enabled.
        initOrganisationUnitChosenDropDown('cluster','#cluster-unit',"150px");

        ouChange('national','0',selectedPartnerValue,selectedPartnerId); 

     }else{
         destroyChosenDropDownList('#cluster-unit'); // to enable edit the raw html elements
         $('#cluster-unit').prop("disabled", true);
         initOrganisationUnitChosenDropDown('CBO','#cluster-unit',"150px");
     }
});

//cluster event handler
$('#cluster-unit').on('change', function (event) {
     var selectedClusterId = $("#cluster-unit option:selected").val();
     var selectedClusterValue=$("#cluster-unit option:selected").attr('data-value');

     destroyChosenDropDownList('#cbo-unit');
     $('#cbo-unit').prop("disabled", false); // Element(s) are now enabled.
     $('#cbo-unit').empty();
     $('#cbo-unit').append("<option></option>");
     $.each(cboData, function( index, cboObject ) {
        if(cboObject['cluster_id']==selectedClusterId){
            console.log("match");
            var elementToAppend = '<option data-value="cbo_unit" data-id="' + cboObject['id'] + '" data-name="' + cboObject['name'] + '">' + cboObject['name'] + '</option>';
            $("#cbo-unit").append(elementToAppend);
        }
     });
     initOrganisationUnitChosenDropDown('CBO','#cbo-unit',"200px");

    ouChange('national','0',selectedClusterValue,selectedClusterId); 
    
});


//cbo event handler
$('#cbo-unit').on('change', function (event) {
    var selectedCboId = $("#cbo-unit option:selected").attr('data-id');
    var selectedCboValue=$("#cbo-unit option:selected").attr('data-value');

    
    ouChange('national','0',selectedCboValue,selectedCboId); 
    

});


function fetchOrganisationUnitData(){
    $.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: localityApi, // the url from server we that we want to use
        contentType: 'application/json; charset=utf-8',
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            localityData=data;
            // console.log(data);
            $.each(data, function( key, value ) {

                var elementToAppend = '<option data-id="' + key + '" data-name="' + value.name + '">' + value.name + '</option>';
                $("#county-organisation-unit").append(elementToAppend);

            });
            initOrganisationUnitChosenDropDown("County:","#county-organisation-unit");
            initOrganisationUnitChosenDropDown("Sub county:","#countituency-organisation-unit");
            initOrganisationUnitChosenDropDown("Ward:","#ward-organisation-unit");
            // console.log("localityData");
            // console.log(localityData);
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            var parsed_data = response.responseText;
        }

    });
}


function fetchCBOData(){
    $.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: cboApi, // the url from server we that we want to use
        contentType: 'application/json; charset=utf-8',
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            cboData=data;
            // console.log("cbo data");
            // console.log(data);
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            var parsed_data = response.responseText;
        }
    });

}

fetchOrganisationUnitData();
fetchCBOData();

// CUSTOM
$('#period').chosen({
    placeholder_text_single: "Select period ",
    no_results_text: "No results found",
    width: "200px"
});
// CUSTOM