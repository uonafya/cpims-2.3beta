var localityApi='/get_locality_data/';
var cboApi= '/fetch_cbo_list/'
var localityData='';
var cboData='';
var selectedCountySiblingsList='none'; //list of countituency in the selected county
var pages=['served','hivstats','registration','cpara']
var currentPage='';

var period='annual'
var currentDrillOption='locality' //weather drill by locality or by funding partner 'locality' or 'funding'
var localityLevel='national';
var fundingPartnerLevel='none';
var selectedPartner='none';
var selectedOrgId='none';

$(document).ready(function () {
    initOrganisationUnitChosenDropDown('funding mechanism','#funding-mechanism');
    initOrganisationUnitChosenDropDown('cluster','#cluster-unit',"150px");
    initOrganisationUnitChosenDropDown('CBO','#cbo-unit',"150px");

});


function resetFundingMechanismOptions(){
    $("#funding-mechanism").val('').trigger("chosen:updated");
    $("#cluster-unit").val('').trigger("chosen:updated");
    $("#cbo-unit").val('').trigger("chosen:updated");
}


function resetOrgUnitOptions(){
    $("#county-organisation-unit").val('').trigger("chosen:updated");
    $("#countituency-organisation-unit").val('').trigger("chosen:updated");
    $("#ward-organisation-unit").val('').trigger("chosen:updated");
}

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


level='national', area_id='',funding_partner='',funding_part_id='',period_typ='annual'

$('#period').on('change', function (event) {
    var periodVal = $("#period option:selected").attr('data-value');
    period=periodVal;
    if(currentDrillOption=='funding' && currentPage==pages[0]){
        fetchOvcServedStatusStats('none','0',fundingPartnerLevel,selectedPartner,period);
        fetchAllOvc('none','0',fundingPartnerLevel,selectedPartner,period);
    }else if(currentDrillOption=='funding' && currentPage==pages[2]){
        fetchNewOVCRegs('none','0',fundingPartnerLevel,selectedPartner,period);
        fetchExitedAndActiveOVCRegs('none','0',fundingPartnerLevel,selectedPartner,period);
        fetchExitedHseld('none','0',fundingPartnerLevel,selectedPartner,period);
        fetchTotalOVCsEverExited('none','0',fundingPartnerLevel,selectedPartner,period);
        fetchTotalOVCsEver('none','0',fundingPartnerLevel,selectedPartner,period);
        fetchWoBCertAtEnrol('none','0',fundingPartnerLevel,selectedPartner,period);

        fetchWithBCertToDate('none','0',fundingPartnerLevel,selectedPartner,period);

    }else if(currentDrillOption=='locality' && currentPage==pages[0]){
        fetchOvcServedStatusStats(localityLevel,selectedOrgId,'none','none',period);
        fetchAllOvc(localityLevel,selectedOrgId,'none','none',period);
    }else if(currentDrillOption=='locality' && currentPage==pages[2]){
        fetchNewOVCRegs(localityLevel,selectedOrgId,'none','none',period);
        fetchExitedAndActiveOVCRegs(localityLevel,selectedOrgId,'none','none',period);
        fetchExitedHseld(localityLevel,selectedOrgId,'none','none',period);

        fetchTotalOVCsEverExited(localityLevel,selectedOrgId,'none','none',period);

        fetchWoBCertAtEnrol(localityLevel,selectedOrgId,'none','none',period);

        fetchTotalOVCsEver(localityLevel,selectedOrgId,'none','none',period);

        fetchWithBCertToDate(localityLevel,selectedOrgId,'none','none',period);

    }else if(currentPage==pages[3]){
        fetchPerBenchmarkPerformance(localityLevel,selectedOrgId,'none','none',period);
        fetchCPARAResults(localityLevel,selectedOrgId,'none','none',period);
        fetchHHScoringCat(localityLevel,selectedOrgId,'none','none',period);
        fetchPerBenchmarkDomainPerformance(localityLevel,selectedOrgId,'none','none',period);
    }
});

//county event handler
$('#county-organisation-unit').on('change', function (event) {

    resetFundingMechanismOptions();
    currentDrillOption='locality';
    localityLevel='county';
    var localityDataToDisplay= cloneObject(localityData);
    var selectedCountyId = $("#county-organisation-unit option:selected").attr('data-id');
    selectedOrgId=selectedCountyId;
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

    if(currentPage==pages[1]){
        fetchHivStatsFromServer('county',selectedCountyId);
        fetchActiveOvcHivStats('county',selectedCountyId);
        fetchCascade90FromServer('county',selectedCountyId);
    }else if(currentPage==pages[0]){
        fetchOvcServedStatusStats(localityLevel,selectedCountyId,'none','none',period);
        fetchAllOvc(localityLevel,selectedCountyId,'none','none',period);
    }else if (currentPage==pages[2]){
        fetchNewOVCRegs(localityLevel,selectedCountyId,'none','none',period);
        fetchExitedAndActiveOVCRegs(localityLevel,selectedCountyId,'','',period);
        fetchExitedHseld(localityLevel,selectedCountyId,'none','none',period);

        fetchTotalOVCsEverExited(localityLevel,selectedCountyId,'none','none',period);

        fetchWoBCertAtEnrol(localityLevel,selectedCountyId,'none','none',period);

        fetchTotalOVCsEver(localityLevel,selectedCountyId,'none','none',period);
        fetchWithBCertToDate(localityLevel,selectedCountyId,'none','none',period);

    }else if(currentPage==pages[3]){
        fetchCPARAResults(localityLevel,selectedCountyId,'','',period);
        fetchPerBenchmarkPerformance(localityLevel,selectedCountyId,'','',period);
        fetchHHScoringCat(localityLevel,selectedCountyId,'','',period);
        fetchPerBenchmarkDomainPerformance(localityLevel,selectedCountyId,'','',period);
    }

});


//sub county event handler
$('#countituency-organisation-unit').on('change', function (event) {
    resetFundingMechanismOptions();
    currentDrillOption='locality';
    localityLevel='subcounty';
    // console.log($("#countituency-organisation-unit option:selected"));
    var selectedSubCountyId = $("#countituency-organisation-unit option:selected").attr('data-id');
    var selectedSubCountyName=$("#countituency-organisation-unit option:selected").attr('data-name');
    selectedOrgId=selectedSubCountyId;
    $('.org-unit-label').html(selectedSubCountyName);
    if(currentPage==pages[1]){
        fetchHivStatsFromServer('subcounty',selectedSubCountyId);
        fetchActiveOvcHivStats('subcounty',selectedSubCountyId);
        fetchCascade90FromServer('subcounty',selectedSubCountyId);
    }else if(currentPage==pages[0]){
        fetchOvcServedStatusStats(localityLevel,selectedSubCountyId,'none','none',period);
        fetchAllOvc(localityLevel,selectedSubCountyId,'none','none',period);
    }else if (currentPage==pages[2]){
        fetchNewOVCRegs(localityLevel,selectedSubCountyId,'none','none',period);
        fetchExitedAndActiveOVCRegs(localityLevel,selectedSubCountyId,'none','none',period);
        fetchExitedHseld(localityLevel,selectedSubCountyId,'none','none',period);

        fetchTotalOVCsEverExited(localityLevel,selectedSubCountyId,'none','none',period);

        fetchTotalOVCsEver(localityLevel,selectedSubCountyId,'none','none',period);
        fetchWoBCertAtEnrol(localityLevel,selectedSubCountyId,'none','none',period);

        fetchWithBCertToDate(localityLevel,selectedSubCountyId,'none','none',period);


    }else if(currentPage==pages[3]){
        fetchCPARAResults(localityLevel,selectedSubCountyId,'none','none',period);
        fetchPerBenchmarkPerformance(localityLevel,selectedSubCountyId,'none','none',period);
        fetchHHScoringCat(localityLevel,selectedSubCountyId,'none','none',period);
        fetchPerBenchmarkDomainPerformance(localityLevel,selectedSubCountyId,'none','none',period);
    }
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
    resetFundingMechanismOptions();
    currentDrillOption='locality';
    localityLevel='ward';
    // console.log($("#countituency-organisation-unit option:selected"));
    var selectedWardId = $("#ward-organisation-unit option:selected").attr('data-id');
    var selectedWardName=$("#ward-organisation-unit option:selected").attr('data-name');
    selectedOrgId=selectedWardId;
    $('.org-unit-label').html(selectedWardName);
    if(currentPage==pages[1]){
        fetchHivStatsFromServer('ward',selectedWardId);
        fetchActiveOvcHivStats('ward',selectedWardId);
        fetchCascade90FromServer('ward',selectedWardId);
    }else if(currentPage==pages[0]){
        fetchOvcServedStatusStats(localityLevel,selectedWardId,'none','none',period);
        fetchAllOvc(localityLevel,selectedWardId,'none','none',period);
    }else if (currentPage==pages[2]){

        fetchTotalOVCsEverExited(localityLevel,selectedWardId,'none','none',period);
        fetchNewOVCRegs(localityLevel,selectedWardId,'none','none',period);
        fetchExitedAndActiveOVCRegs(localityLevel,selectedWardId,'none','none',period);
        fetchExitedHseld(localityLevel,selectedWardId,'none','none',period);

        fetchWoBCertAtEnrol(localityLevel,selectedWardId,'none','none',period);

        fetchTotalOVCsEver(localityLevel,selectedWardId,'none','none',period);

        fetchWithBCertToDate(localityLevel,selectedWardId,'none','none',period);

    }else if(currentPage==pages[3]){
        fetchPerBenchmarkPerformance(localityLevel,selectedWardId,'none','none',period);
        fetchCPARAResults(localityLevel,selectedWardId,'none','none',period);
        fetchHHScoringCat(localityLevel,selectedWardId,'none','none',period);
        fetchPerBenchmarkDomainPerformance(localityLevel,selectedWardId,'none','none',period);
    }

});


//funding mechanism event handler
$('#funding-mechanism').on('change', function (event) {
    resetOrgUnitOptions();
    currentDrillOption='funding';
     var selectedPartnerId = $("#funding-mechanism option:selected").val();
     var selectedPartnerValue=$("#funding-mechanism option:selected").attr('data-value');
     if(selectedPartnerId.toLowerCase()==0){ //usaid
        destroyChosenDropDownList('#cluster-unit'); // to enable edit the raw html elements
        $('#cluster-unit').prop("disabled", false); // Element(s) are now enabled.
        initOrganisationUnitChosenDropDown('cluster','#cluster-unit',"150px");
        
        if(currentPage==pages[1]){
            fetchHivStatsFromServer(selectedPartnerValue,selectedPartnerId);
            fetchActiveOvcHivStats(selectedPartnerValue,selectedPartnerId);
            fetchCascade90FromServer(selectedPartnerValue,selectedPartnerId);
        }else if(currentPage==pages[0]){
            fundingPartnerLevel=selectedPartnerValue;
            selectedPartner=selectedPartnerId;
            fetchOvcServedStatusStats('none',0,fundingPartnerLevel,selectedPartner,period);
            fetchAllOvc('none',0,fundingPartnerLevel,selectedPartner,period);
        }else if (currentPage==pages[2]){
            fundingPartnerLevel=selectedPartnerValue;
            selectedPartner=selectedPartnerId;
            fetchNewOVCRegs('none',0,fundingPartnerLevel,selectedPartner,period);
            fetchExitedAndActiveOVCRegs('none',0,fundingPartnerLevel,selectedPartner,period);
            fetchExitedHseld('none',0,fundingPartnerLevel,selectedPartner,period);


            fetchWithBCertToDate('none',0,fundingPartnerLevel,selectedPartner,period);


            fetchWoBCertAtEnrol('none',0,fundingPartnerLevel,selectedPartner,period);

            fetchTotalOVCsEverExited('none',0,fundingPartnerLevel,selectedPartner,period);
            fetchTotalOVCsEver('none',0,fundingPartnerLevel,selectedPartner,period);
        }else if(currentPage==pages[3]){

            fundingPartnerLevel=selectedPartnerValue;
            selectedPartner=selectedPartnerId;
            fetchCPARAResults('none',0,fundingPartnerLevel,selectedPartner,period);
            fetchPerBenchmarkPerformance('none',0,fundingPartnerLevel,selectedPartner,period);
            fetchHHScoringCat('none',0,fundingPartnerLevel,selectedPartner,period);
            fetchPerBenchmarkDomainPerformance('none',0,fundingPartnerLevel,selectedPartner,period);
        }

     }else{
         destroyChosenDropDownList('#cluster-unit'); // to enable edit the raw html elements
         $('#cluster-unit').prop("disabled", true);
         initOrganisationUnitChosenDropDown('CBO','#cluster-unit',"150px");
     }
});

//cluster event handler
$('#cluster-unit').on('change', function (event) {
    resetOrgUnitOptions();
    currentDrillOption='funding';
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
    if(currentPage==pages[1]){
        fetchHivStatsFromServer(selectedClusterValue,selectedClusterId);
        fetchActiveOvcHivStats(selectedClusterValue,selectedClusterId);
        fetchCascade90FromServer(selectedClusterValue,selectedClusterId);
    }else if(currentPage==pages[0]){
        fundingPartnerLevel=selectedClusterValue;
        selectedPartner=selectedClusterId;
        fetchOvcServedStatusStats('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchAllOvc('none',0,fundingPartnerLevel,selectedPartner,period);
    }else if (currentPage==pages[2]){
        fundingPartnerLevel=selectedClusterValue;
        selectedPartner=selectedClusterId;
        fetchNewOVCRegs('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchExitedAndActiveOVCRegs('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchExitedHseld('none',0,fundingPartnerLevel,selectedPartner,period);


        fetchWithBCertToDate('none',0,fundingPartnerLevel,selectedPartner,period);


        fetchWoBCertAtEnrol('none',0,fundingPartnerLevel,selectedPartner,period);

        fetchTotalOVCsEver('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchTotalOVCsEverExited('none',0,fundingPartnerLevel,selectedPartner,period);


    }else if(currentPage==pages[3]){
        fundingPartnerLevel=selectedClusterValue;
        selectedPartner=selectedClusterId;
        fetchCPARAResults('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchPerBenchmarkPerformance('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchHHScoringCat('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchPerBenchmarkDomainPerformance('none',0,fundingPartnerLevel,selectedPartner,period);
    }

});


//cbo event handler
$('#cbo-unit').on('change', function (event) {
    resetOrgUnitOptions();
    currentDrillOption='funding';
     var selectedCboId = $("#cbo-unit option:selected").attr('data-id');
     var selectedCboValue=$("#cbo-unit option:selected").attr('data-value');

    if(currentPage==pages[1]){
        fetchHivStatsFromServer(selectedCboValue,selectedCboId);
        fetchActiveOvcHivStats(selectedCboValue,selectedCboId);
        fetchCascade90FromServer(selectedCboValue,selectedCboId);
    }else if(currentPage==pages[0]){
        fundingPartnerLevel=selectedCboValue;
        selectedPartner=selectedCboId;
        fetchOvcServedStatusStats('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchAllOvc('none',0,fundingPartnerLevel,selectedPartner,period);
    }else if (currentPage==pages[2]){
        fundingPartnerLevel=selectedCboValue;
        selectedPartner=selectedCboId;
        fetchNewOVCRegs('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchExitedAndActiveOVCRegs('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchExitedHseld('none',0,fundingPartnerLevel,selectedPartner,period);



        fetchWithBCertToDate('none',0,fundingPartnerLevel,selectedPartner,period);


        fetchWoBCertAtEnrol('none',0,fundingPartnerLevel,selectedPartner,period);

        fetchTotalOVCsEverExited('none',0,fundingPartnerLevel,selectedPartner,period);

        fetchTotalOVCsEver('none',0,fundingPartnerLevel,selectedPartner,period);
    }else if(currentPage==pages[3]){
        fundingPartnerLevel=selectedCboValue;
        selectedPartner=selectedCboId;
        fetchPerBenchmarkPerformance('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchCPARAResults('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchHHScoringCat('none',0,fundingPartnerLevel,selectedPartner,period);
        fetchPerBenchmarkDomainPerformance('none',0,fundingPartnerLevel,selectedPartner,period);
    }

});


function fetchOrganisationUnitData(){
    console.log("locality data fetching=====>");
    $.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: localityApi, // the url from server we that we want to use
        contentType: 'application/json; charset=utf-8',
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            console.log("locality data=====>");
            localityData=data;

            $.each(data, function( key, value ) {

                var elementToAppend = '<option data-id="' + key + '" data-name="' + value.name + '">' + value.name + '</option>';
                $("#county-organisation-unit").append(elementToAppend);

            });
            initOrganisationUnitChosenDropDown("County:","#county-organisation-unit");
            initOrganisationUnitChosenDropDown("Sub county:","#countituency-organisation-unit");
            initOrganisationUnitChosenDropDown("Ward:","#ward-organisation-unit");
            // console.log("localityData");
            // console.log(localityData);lic_d
        },
        error: function (response, request) {
            //    console.log("got an error fetching wards");
            var parsed_data = response.responseText;
            console.log(parsed_data);
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
