// QuestionSkipLogic
//format is:   triggerSkip(inputToCheck,rightValue,questionToGoTo,tabContainingDestinationQn);
    // Q5 -> Q10
    triggerSkip('WB_STA_5_1','Unemployed','WB_STA_10_1','2');

    // Q14 -> Q17
    triggerSkip('WB_HEL_14_1','NODISABILITY','WB_HEL_17_1','3');

    // Q17 -> Q31
    triggerSkip('WB_HEL_17_1','ANNO','WB_SAF_33_1','4');
    triggerSkip('WB_HEL_17_1','AREFUSE','WB_SAF_33_1','4');
    
    // Q19 -> Q21
    triggerSkip('WB_HEL_19_1','ANNO','WB_HEL_21_1','3');
    
    // Q21 -> Q23
    triggerSkip('WB_HEL_21_1','ANNO','WB_HEL_23_1','3');
    
    // Q24 -> Q26
    triggerSkip('WB_HEL_24_1','NO','WB_HEL_26_1','3');
    triggerSkip('WB_HEL_24_1','Refuse','WB_HEL_26_1','3');
    
    // Q31 -> Q33
    triggerSkip('WB_SAF_33_1','ANNO','WB_SAF_34_1','4');
    triggerSkip('WB_SAF_33_1','AREFUSE','WB_SAF_34_1','4');
    
    // Q33 -> Q35 *********** Not Implemented ************
      // triggerSkip('WB_SAF_34_1','ANNO','WB_SAF_36_1','4');
      // triggerSkip('WB_SAF_34_1','AREFUSE','WB_SAF_36_1','4');
    // END Q33 -> Q35 *********** Not Implemented ************

// endQuestionSkipLogic





// ------------------------CORE-------------------------
function triggerSkip(inputToCheck,rightValue,toQnID,toTabID) {
    $('input[name="'+inputToCheck+'"][value="'+rightValue+'"]').on('change', function () {
        
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
            if(valFromInput == rightValue){
                console.log("TICKED radio with Name: "+inputToCheck+" found");
                var unDo = false;
                skipToQn(inputToCheck,toQnID,toTabID,unDo);
            }else{
                var unDo = true;
                skipToQn(inputToCheck,toQnID,toTabID,unDo);
            }
        }
        //END cater for radio
    });
}
function skipToQn(inputToCheck,toQnID,toTabID,unDo) {
    $('a[href="#step'+toTabID+'"]').trigger("click");
    //hideQnsBtwn
    var destinationT = $('input[name="'+toQnID+'"]').closest("tr");
    if(!unDo){
            $("td").attr("tabindex", "-1");
            $('input[name="'+toQnID+'"]').closest("td").attr("tabindex", "1");
            $('input[name="'+toQnID+'"]').closest("td").focus();
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").addClass('hidden');
            $('input[name="'+toQnID+'"]').closest("td").css('outline', 'thick double #32a1ce');
            console.log("skipping to Qn: "+toQnID+" on Tab: "+toTabID);
        }else{
            $("td").attr("tabindex", "-1");
            $('input[name="'+inputToCheck+'"]').closest("td").attr("tabindex", "1");
            $('input[name="'+inputToCheck+'"]').closest("td").focus();
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").removeClass('hidden');
            $('input[name="'+inputToCheck+'"]').closest("td").css('outline', 'thick double #32a1ce');
            console.log("UNDO skipping to Qn: "+toQnID+" on Tab: "+toTabID);
        }
    //hideQnsBtwn
}
// ------------------------endCORE-------------------------