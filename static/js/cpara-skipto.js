// QuestionSkipLogic
//format is:   triggerSkip(inputToCheck,rightValue,questionToGoTo,tabContainingDestinationQn);
    // Q1 -> Q2
    triggerSkip('if_ovc','ANNO','cp5q','2');
    triggerSkip('u10_know_status','ANNO','o10_know_status','2');
    triggerSkip('o10_know_status','ANNO','adole_preg_hiv','2');
    triggerSkip('adole_preg_hiv','ANNO','cp24q','2');
    triggerSkip('adole_preg_testpos','ANNO','cp24q','2');
    triggerSkip('adole_wo_deliv','ANNO','cp24q','2');
    triggerSkip('adole_gb_hse','ANNO','cp30q','2');
    triggerSkip('child_w_disab_hse','ANNO','cp32q','3');
    //<TODOne just test
    triggerSkip('cp5d','ANNO','cp32q','3');
    triggerSkip('cp3d','ANNO','cp49q','4');
    triggerSkip('adole_gb_hse2','ANNO','cp30q','2');
    //>TODOne just test
    triggerSkip('child_abv_10y','ANNO','cp36q','3');
    triggerSkip('u_chd_sck','ANNO','cp43q','3');
    triggerSkip('chd_ovr_10','ANNO','child_hd_hse','4');
    triggerSkip('chd_ovr_10y','ANNO','cp49q','4');
    triggerSkip('child_hd_hse','ANNO','cp49q','4');
    triggerSkip('o5y_cd_hse','ANNO','cp55q','4');
    triggerSkip('o10y_cd_hse_Qn','ANNO','cp60q','4');
    triggerSkip('cld_rsk_abus','ANNO','cp60q','4');
    triggerSkip('chd_ovr_10ys','ANNO','cp62q','4');
    triggerSkip('adole_in_vc_train','ANNO','cp74q','5');
    
    // triggerSkip('cp49q','AYES','q12p4','4');
    triggerSkip('cp49q','AYES','o5y_cd_hse','4');
    triggerSkip('cp50q','ANNO','q12p4','4');
    triggerSkip('child_bwn_4t5y_Qn','ANNO','cp70q','5');
    triggerSkip('clw_hiv_o5','ANNO','cp8q','2');
    triggerSkip('cp23qa','ANNO','cp24q','2'); triggerSkip('cp23qb','ANNO','cp24q','2'); triggerSkip('cp23qc','ANNO','cp24q','2'); triggerSkip('cp23qd','ANNO','cp24q','2');

// endQuestionSkipLogic





// ------------------------CORE-------------------------
function triggerSkip(inputToCheck,rightValue,toQnID,toTabID) {
    // $('input[name="'+inputToCheck+'"][value="'+rightValue+'"]').on('change', function () {
    $('input[name="'+inputToCheck+'"]').on('change', function () {
        // console.log('onchanging,,,');
        
        var theval = $('input[name="'+inputToCheck+'"]').val();
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
            // console.log("checkbox with Name: "+inputToCheck+" found");
            var valFromInput = '';
            $.each($(this), function (chind, eachbx) {
                if($(this).is(':checked')){
                    // console.log("TICKED checkbox with Name: "+inputToCheck+" found");
                    var unDo = false;
                    skipToQn(inputToCheck,toQnID,toTabID,unDo);
                }else{
                    // console.log("UNDO ticked checkbox with Name: "+inputToCheck);
                    var unDo = true;
                    skipToQn(inputToCheck,toQnID,toTabID,unDo);
                }
            });
        }
        // END cater for checkbox

        // cater for radio
        if($('input[name="'+inputToCheck+'"]').attr('type') == 'radio'){
            var valFromInput = $('input[name="'+inputToCheck+'"]:checked').val();
            // console.log("radio with Name: "+inputToCheck+" found");
            // console.log("valFromInput======> "+valFromInput);
            if(valFromInput === rightValue){
                // console.log("TICKED radio with Name: "+inputToCheck+" found. rightValue="+rightValue+" & valFromInput="+valFromInput);
                // console.log("valFromInput: "+valFromInput+" & rightValue: "+rightValue);
                var unDo = false;
                skipToQn(inputToCheck,toQnID,toTabID,unDo);
            }else if(valFromInput !== rightValue){
                // console.log("undoing... ");
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
            $(".form-group").attr("tabindex", "-1");
            $('input[name="'+toQnID+'"]').closest("td").attr("tabindex", "1");
            $('input[name="'+toQnID+'"]').closest(".form-group").attr("tabindex", "1");
            $('input[name="'+toQnID+'"]').closest("td").focus();
            $('input[name='+toQnID+']').removeAttr('required');
			$('input[name='+toQnID+']').attr('data-parsley-required', false);
            $('input[name="'+toQnID+'"]').closest(".form-group").focus();
            // $('input[name="'+inputToCheck+'"]').closest(".form-group").nextUntil(destinationT, "tr").addClass('hidden');
            
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('input').attr('data-parsley-required', false).removeAttr('required');
            
            //tick AYES for skipped qns
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('input[value=AYES]').prop("checked", true);
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('tr').not(':last-of-type').find('td').not(':first-of-type').css('background', '#dddddd');
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('td input[type=radio]').attr('disabled', 'disabled').attr('data-parsley-required', false).removeAttr('required');
            //tick AYES for skipped qns

            $('input[name="'+inputToCheck+'"]').closest(".col-md-12:not(.containsTable)").nextUntil(destinationT, ".col-md-12:not(.containsTable)").find('.form-group').not('.note-info').addClass('hidden').after('<span id="skyp"><br><i style="color: grey;">Skipped question</i><br/></span>');
            
            //tick Benchmark
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('.note-info').find('input[value=AYES]').prop('checked', true).trigger('click').css('color', 'green');
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('.form-group.note-info input[value="AYES"]').prop('checked',true);
            //tick Benchmark

            $('input[name="'+toQnID+'"]').closest("td").css('outline', '3px solid #32a1ce');
            $('input[name="'+toQnID+'"]').closest(".form-group").css('outline', '3px solid #32a1ce');
            console.log("skipping to Qn: "+toQnID+" on Tab: "+toTabID);
        }
        if(unDo){
            // console.log("undoing2... ");
            $("td").attr("tabindex", "-1");
            $(".form-group").attr("tabindex", "-1");
            $('input[name="'+inputToCheck+'"]').closest("td").attr("tabindex", "1");
            $('input[name="'+inputToCheck+'"]').closest(".form-group").attr("tabindex", "1");
            $('input[name="'+inputToCheck+'"]').closest("td").focus();
            $('input[name="'+inputToCheck+'"]').closest(".form-group").focus();
            $('input[name="'+inputToCheck+'"]').closest("tr").nextUntil(destinationT, "tr").removeClass('hidden');

            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('.form-group').removeClass('hidden').after('');
            //UNtick AYES for skipped qns
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('input[value=AYES]').prop("checked", false);
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('tr').not(':last-of-type').find('td').not(':first-of-type').css('background', '##ffffff');
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('td input[type=radio]').removeAttr('disabled');
            //UNtick AYES for skipped qns
            //benchmark=no for skipped qns
            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('.form-group.note-info input[value="ANNO"]').prop('checked',true);
            //benchmark=no for skipped qns

            $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".col-md-12").find('#skyp').remove();

            // $('input[name="'+inputToCheck+'"]').closest(".col-md-12").nextUntil(destinationT, ".form-group").find('input').attr('required');
            
            $('input[name="'+inputToCheck+'"]').closest("td").css('outline', '1px solid #32a1ce');
            $('input[name="'+inputToCheck+'"]').closest(".form-group").css('outline', '1px solid #32a1ce');
            
            $('input[name="'+destinationT+'"]').closest("td").css('outline', 'none');
            $('input[name="'+destinationT+'"]').closest(".form-group").css('outline', 'none');
            console.log("UNDO skipping to Qn: "+toQnID+" on Tab: "+toTabID);
        }
    //hideQnsBtwn
}
// ------------------------endCORE-------------------------
