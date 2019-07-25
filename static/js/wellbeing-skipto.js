// QuestionSkipLogic
//format is:   triggerSkip(inputToCheck,rightValue,questionToGoTo,tabContainingDestinationQn);
    // Q5 -> Q10
    triggerSkip('WB_STA_5_1','Unemployed','WB_STA_10_1','2');

    // Q14 -> Q17
    triggerSkip('WB_HEL_14_1','NODISABILITY','WB_HEL_17_1','3');

    // Q16 -> Q17
    triggerSkip('WB_HEL_16_1','NODISABILITY','WB_HEL_17_1','3');

    // Q17 -> Q29
    // triggerSkip('WB_HEL_17_1','ANNO','WB_SAF_31_1','4');
    triggerSkip('WB_HEL_17_1','AREFUSE','WB_SAF_31_1','4');
    $('input[name=WB_HEL_17_1][value="ANNO"]').click(function (e) { 
        triggerSkip('WB_HEL_17_1','ANNO','WB_SAF_31_1','4');
    });
    $('input[name=WB_HEL_17_1][value="AREFUSE"]').click(function (e) { 
        triggerSkip('WB_HEL_17_1','AREFUSE','WB_SAF_31_1','4');
    });

    // Q18 -> Q29
    triggerSkip('WB_HEL_18_1','ANNO','WB_SAF_31_1','4');
    triggerSkip('WB_HEL_18_1','AREFUSE','WB_SAF_31_1','4');
    
    // Q19 -> Q24
    triggerSkip('WB_HEL_19_1','ANNO','WB_HEL_21_1','3');
    
    // Q21 -> Q23
    triggerSkip('WB_HEL_21_1','ANNO','WB_HEL_23_1','3');
    
    // Q24 -> Q26
    triggerSkip('WB_HEL_24_1','NO','WB_HEL_26_1','3');
    triggerSkip('WB_HEL_24_1','Refuse','WB_HEL_26_1','3');
    
    // Q31 -> Q33
    triggerSkip('WB_SAF_33_1','ANNO','WB_SAF_34_1','4');
    triggerSkip('WB_SAF_33_1','AREFUSE','WB_SAF_34_1','4');
    
    // Q33 -> Q35 *********** Implemented ************
      triggerSkip('WB_SAF_34_1','ANNO','WB_SAF_36_1','4');
      triggerSkip('WB_SAF_34_1','AREFUSE','WB_SAF_36_1','4');
    // END Q33 -> Q35 *********** Implemented ************

// endQuestionSkipLogic





// ------------------------CORE-------------------------
function triggerSkip(inputToCheck,rightValue,toQnID,toTabID) {
    $('input[name="'+inputToCheck+'"]').on('change', function () {
        
        // textbox, numbers, dates etc
        if($('input[name="'+inputToCheck+'"]').attr('type') == 'date' || $('input[name="'+inputToCheck+'"]').attr('type') == 'text' || $('input[name="'+inputToCheck+'"]').attr('type') == 'number'){
            var valFromInput = $('input[name="'+inputToCheck+'"]').val();
            if(valFromInput == rightValue){
                var unDo = false
                skipToQn(inputToCheck,toQnID,toTabID,unDo);
            }else{
                var unDo = true;
                skipToQn(inputToCheck,toQnID,toTabID,unDo);
            }
        }
        // END textbox, numbers, dates etc

        // cater for checkbox
        if($('input[name="'+inputToCheck+'"]').attr('type') == 'checkbox'){
            console.log("checkbox with Name: "+inputToCheck+" found");
            var valFromInput = '';
            $.each($(this), function (chind, eachbx) {
                if($(this).is(':checked')){
                    console.log("TICKED checkbox with Name: "+inputToCheck+" found");
                    var unDo = false;
                    skipToQn(inputToCheck,toQnID,toTabID,unDo);
                }else{
                    console.log("UNDO ticked checkbox with Name: "+inputToCheck);
                    var unDo = true;
                    skipToQn(inputToCheck,toQnID,toTabID,unDo);
                }
            });
        }
        // END cater for checkbox

        // cater for radio
        if($('input[name="'+inputToCheck+'"]').attr('type') == 'radio'){
            console.log("radio with Name: "+inputToCheck+" found");
            var valFromInput = $('input[name="'+inputToCheck+'"]:checked').val();
            console.log("valFromInput======> "+valFromInput);
            if(valFromInput === rightValue){
                console.log("TICKED radio with Name: "+inputToCheck+" found");
                var unDo = false;
                skipToQn(inputToCheck,toQnID,toTabID,unDo);
            }else if(valFromInput !== rightValue){
                console.log("UNDO tick radio with Name: "+inputToCheck+" found");
                var unDo = true;
                skipToQn(inputToCheck,toQnID,toTabID,unDo);
            }
        }
        //END cater for radio
    });
}
function skipToQn(inputToCheck,toQnID,toTabID,unDo) {
    //hideQnsBtwn
    var destinationT = $('input[name="'+toQnID+'"]').closest("tr");
    if(!unDo){
            $('a[href="#step'+toTabID+'"]').trigger("click");
            $("td").attr("tabindex", "-1");
            $('input[name="'+toQnID+'"]').closest("td").attr("tabindex", "1");
            $('input[name="'+toQnID+'"]').closest("td").focus();
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").find('.skyp').remove();
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").find('td').not('.skyp').addClass('hidden');
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").append('<td colspan="3" class="skyp text-center"><i style="color: grey;">Skipped question</i></td>');
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").find('input, select, textarea').attr('data-parsley-required', false).removeAttr('required');
            $('input[name="'+toQnID+'"]').closest("td").css('outline', '1px solid #32a1ce');
            console.log("skipping to Qn: "+toQnID+" on Tab: "+toTabID);
        }
        if(unDo){
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").find('td.hidden').removeClass('hidden');
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").find('.skyp').remove();

            $("td").attr("tabindex", "-1");
            $('input[name="'+inputToCheck+'"]').closest("td").attr("tabindex", "1");
            $('input[name="'+inputToCheck+'"]').closest("td").focus();
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").removeClass('hidden');
            $('input[name="'+inputToCheck+'"]').closest("td").css('outline', '1px solid #32a1ce');
            console.log("UNDO skipping to Qn: "+toQnID+" on Tab: "+toTabID);
        }
    //hideQnsBtwn
}
// ------------------------endCORE-------------------------





//raw
// Tab 1 Qn 9
$('input[name=WB_GEN_05]').change(function (e) { 
    var this_val = $(this).val();
    if(this_val == 'ANNO'){
        $('input[name=WB_GEN_06], input[name=WB_GEN_07]').attr('disabled', true).val(0);
    }else{
        $('input[name=WB_GEN_06], input[name=WB_GEN_07]').removeAttr('disabled').val('');
    }
});
// Tab 1 Qn 9

// Tab 3 Qn 18

$('input[name=WB_HEL_18_2]').attr('disabled', true);
$('input[name=WB_HEL_18_2][value="Unknown"]').prop('checked', true);
$('input[name=WB_HEL_18_1]').change(function () {
    var the_val = $(this).val();
    if(the_val == 'AYES'){
        $('input[name=WB_HEL_18_2]').removeAttr('disabled');
        $('input[name=WB_HEL_18_2]').prop('checked', false);
    }else{
        $('input[name=WB_HEL_18_2][value="Unknown"]').prop('checked', true);
        $('input[name=WB_HEL_18_2]').attr('disabled', true);
    }
});
// Tab 3 Qn 18

// Tab 4 Qn 39
$('input[data-parsley-multiple="WB_SCH_40_1"]').attr('disabled', true);
$('input[data-parsley-multiple="WB_SCH_40_1"]').parent('label').css('color', '#acacac');
$('input[data-parsley-multiple="WB_SCH_39_1"]').change(function (e) { 
    var valu = $(this).val();
    if(valu == 'ANNO'){
        $('input[data-parsley-multiple="WB_SCH_40_1"]').removeAttr('disabled');
        $('input[data-parsley-multiple="WB_SCH_40_1"]').attr('checked', false);
        $('input[data-parsley-multiple="WB_SCH_40_1"]').parent('label').css('color', 'initial');
    }else{
        $('input[data-parsley-multiple="WB_SCH_40_1"]').attr('disabled', true);
        $('input[data-parsley-multiple="WB_SCH_40_1"][value="AYES"]').attr('checked', true);
        $('input[data-parsley-multiple="WB_SCH_40_1"]').parent('label').css('color', '#acacac');
    }
        
});
// Tab 4 Qn 39
//raw