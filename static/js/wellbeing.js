var childrenQuestion={}
var childrenQuestion2={}
var safe_validQns = ['WB_SAF_37_1','WB_SAF_37_2','WB_SAF_38_1','WB_SAF_38_2','WB_SAF_39_1','WB_SAF_39_2','WB_SAF_40_1','WB_SAF_40_2'];
var school_validQns = ['WB_SCH_39_1','WB_SCH_40_1','WB_SCH_41_1','WB_SCH_41_2','WB_SCH_42_1','WB_SCH_42_2','WB_SCH_43_1','WB_SCH_43_2','WB_SCH_44_1','WB_SCH_45_1'];


$('#safetytab > .nav-pills.nav-stacked > li').on('click focus', function(event){
    $('.nav-pills.nav-stacked > li').removeClass('active');
    $(this).addClass('active');
    var childId=$(this).attr('data-child-id');
    var ansObj = {};
    $.each(safe_validQns, function(qindx, ans_name){
      var inpt = $('input[name='+ans_name+']');
      var inpt_type = inpt.attr('type');
      if(inpt_type == 'radio'){
        var answr = $('input[name='+ans_name+']:checked').val();
      }else{
        var answr = inpt.val();
      }
      ansObj[''+ans_name+''] = answr;
      // childrenQuestion[childId].push(qnObj);
    })

    //get values of inputs

    //END get values of inputs
    childrenQuestion[childId]=ansObj;
    console.log("the error log gone");
    console.log(JSON.stringify(childrenQuestion));
    $('#safeanswer').val(JSON.stringify(childrenQuestion));
});


$('#schooltab > .nav-pills.nav-stacked > li').on('click focus', function(event){
    $('.nav-pills.nav-stacked > li').removeClass('active');
    $(this).addClass('active');
    var childId=$(this).attr('data-child-id');
    var ansObj = {};
    
    $.each(school_validQns, function(qindx, ans_name){
        var inpt = $('input[name='+ans_name+']');
        var inpt_type = inpt.attr('type');

       // console.log(inpt);
        console.log(inpt_type);

        if(inpt_type == 'radio'){
            var answr = $('input[name='+ans_name+']:checked').val();
            ansObj[''+ans_name+''] = answr;
        }
        if(inpt_type == 'checkbox'){
            var answerList=[];
            var selectedCheckboxes = $('input[name='+ans_name+']:checked');
            $.each(selectedCheckboxes, function(indx, curElement){
                answerList.push($(curElement).val());
            });
            ansObj[''+ans_name+''] = answerList;
        }

        if(inpt_type == 'text' || inpt_type == 'number'){
            var answr = $('input[name='+ans_name+']').val();
            ansObj[''+ans_name+''] = answr;
        }

        childrenQuestion2[childId]=ansObj;
        $('#schooledanswer').val(JSON.stringify(childrenQuestion2));
    });

})




hideQn('WB_SAF_39_2');
$("input[name='WB_SAF_39_1']").on('change', function () {
    var ival = $("input[name='WB_SAF_39_1']:checked").val();
    if (ival == 'OTHER') {
        unhideQn('WB_SAF_39_2');
    } else {
        hideQn('WB_SAF_39_2');
    }
});

hideQn('WB_SAF_37_2');
$("input[name='WB_SAF_37_1']").on('change', function () {
    var ival = $("input[name='WB_SAF_37_1']:checked").val();
    if (ival == 'OTHER') {
        unhideQn('WB_SAF_37_2');
    } else {
        hideQn('WB_SAF_37_2');
    }
});

hideQn('WB_SAF_38_2');
$("input[name='WB_SAF_38_1']").on('change', function () {
    var ival = $("input[name='WB_SAF_38_1']:checked").val();
    if (ival == 'OTHER') {
        unhideQn('WB_SAF_38_2');
    } else {
        hideQn('WB_SAF_38_2');
    }
});

hideQn('WB_SAF_40_2');
$("input[name='WB_SAF_40_1']").on('change', function () {
    var ival = $("input[name='WB_SAF_40_1']:checked").val();
    if (ival == 'OTHER') {
        unhideQn('WB_SAF_40_2');
    } else {
        hideQn('WB_SAF_40_2');
    }
});

hideQn('WB_SAF_31_2');
$("input[name='WB_SAF_31_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_SAF_31_2');
    }else{
        hideQn('WB_SAF_31_2');
    }
});

hideQn('WB_SAF_34_2');
$("input[name='WB_SAF_34_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_SAF_34_2');
    }else{
        hideQn('WB_SAF_34_2');
    }
});

hideQn('WB_SAF_36_2');
$("input[name='WB_SAF_36_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_SAF_36_2');
    }else{
        hideQn('WB_SAF_36_2');
    }
});

hideQn('WB_SCH_41_2');
$("input[name='WB_SCH_41_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_SCH_41_2');
    }else{
        hideQn('WB_SCH_41_2');
    }
});

hideQn('WB_STA_1_2');
$("input[name='WB_STA_1_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_STA_1_2');
    }else{
        hideQn('WB_STA_1_2');
    }
});

hideQn('WB_STA_2_2');
$("input[name='WB_STA_2_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_STA_2_2');
    }else{
        hideQn('WB_STA_2_2');
    }
});

hideQn('WB_STA_3_2');
$("input[name='WB_STA_3_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_STA_3_2');
    }else{
        hideQn('WB_STA_3_2');
    }
});

hideQn('WB_STA_4_2');
$("input[name='WB_STA_4_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_STA_4_2');
    }else{
        hideQn('WB_STA_4_2');
    }
});

hideQn('WB_STA_5_2');
$("input[name='WB_STA_5_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_STA_5_2');
    }else{
        hideQn('WB_STA_5_2');
    }
});

hideQn('WB_STA_8_2');
$("input[name='WB_STA_8_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_STA_8_2');
    }else{
        hideQn('WB_STA_8_2');
    }
});

hideQn('WB_STA_9_2');
$("input[name='WB_STA_9_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_STA_9_2');
    }else{
        hideQn('WB_STA_9_2');
    }
});

hideQn('WB_HEL_14_2');
$("input[name='WB_HEL_14_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_HEL_14_2');
    }else{
        hideQn('WB_HEL_14_2');
    }
});

hideQn('WB_HEL_16_3');
$("input[name='WB_HEL_16_2'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_HEL_16_3');
    }else{
        hideQn('WB_HEL_16_3');
    }
});

hideQn('WB_HEL_20_2');
$("input[name='WB_HEL_20_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_HEL_20_2');
    }else{
        hideQn('WB_HEL_20_2');
    }
});

hideQn('WB_HEL_25_2');
$("input[name='WB_HEL_25_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_HEL_25_2');
    }else{
        hideQn('WB_HEL_25_2');
    }
});

hideQn('WB_HEL_27_2');
$("input[name='WB_HEL_27_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_HEL_27_2');
    }else{
        hideQn('WB_HEL_27_2');
    }
});

hideQn('WB_HEL_28_2');
$("input[name='WB_HEL_28_1'][value='Other']").on('change', function () {
    var ival = $(this).val();
    if (ival == 'Other' && $(this).prop('checked')) {
        unhideQn('WB_HEL_28_2');
    }else{
        hideQn('WB_HEL_28_2');
    }
});




hideQn('WB_SCH_42_1');
$("input[name='WB_SCH_42_2']").on('change', function () {
    if ($(this).prop('checked')) {
        unhideQn('WB_SCH_42_1');
    }else{
        hideQn('WB_SCH_42_1');
    }
});

hideQn('WB_SCH_43_1');
$("input[name='WB_SCH_43_2']").on('change', function () {
    if ($(this).prop('checked')) {
        unhideQn('WB_SCH_43_1');
    }else{
        hideQn('WB_SCH_43_1');
    }
});



function hideQn(qnID) {
    // $('#' + qnID).addClass('hidden');
    $('#' + qnID).attr("disabled", 'disabled');
    // check if multiselect
    var ms_attr = $('#' + qnID).attr('multiple');
    if (typeof ms_attr !== typeof undefined && ms_attr !== false) {
        $('#' + qnID).multiselect('disable');
    }
    // endCheck
    $('#' + qnID).prop("disabled", true);
    $('#' + qnID).val("");
    $('#' + qnID).removeAttr('required');
}
function unhideQn(qnID) {
    // $('#' + qnID).removeClass('hidden');
    // check if multiselect
    var ms_attr = $('#' + qnID).attr('multiple');
    if (typeof ms_attr !== typeof undefined && ms_attr !== false) {
        $('#' + qnID).multiselect('enable');
    }
    // endCheck
    $('#' + qnID).removeAttr('disabled');
    $('#' + qnID).attr('required');
}