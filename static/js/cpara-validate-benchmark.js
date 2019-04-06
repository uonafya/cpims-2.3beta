// validBench(['cp3d','cp4d','cp5d','cp6d','if_ovc', 'cp1q', 'cp3q', 'cp4q'], ['AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES'], 'cp1b');


// validBench(['if_ovc', 'cp1q', 'cp3q', 'cp4q'], ['AYES','AYES','AYES','AYES'], 'cp1b');
validBench(['cp1q', 'cp3q', 'cp4q'], ['AYES','AYES','AYES'], 'cp1b');
validBench(['cp5q', 'cp6q', 'cp7q'], ['AYES','AYES','AYES'], 'cp2b');
// validBench(['u10_know_status', 'cp8q', 'cp9q', 'cp10q', 'cp11q', 'cp12q', 'o10_know_status', 'cp13q', 'cp14q', 'cp15q', 'cp16q', 'cp17q'], ['AYES','AYES','AYES', 'AYES','AYES','AYES', 'AYES','AYES','AYES', 'AYES','AYES','AYES'], 'cp3b');
validBench(['cp8q', 'cp9q', 'cp10q', 'cp11q', 'cp12q', 'o10_know_status', 'cp13q', 'cp14q', 'cp15q', 'cp16q', 'cp17q'], ['AYES','AYES', 'AYES','AYES','AYES', 'AYES','AYES','AYES', 'AYES','AYES','AYES'], 'cp3b');
// validBench(['adole_preg_hiv', 'cp19q', 'adole_preg_testpos', 'cp20q', 'cp21q', 'adole_wo_deliv','cp22q','cp23q','cp23qa','cp23qb','cp23qc','cp23qd'], ['AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES'], 'cp4b');
validBench(['cp19q', 'adole_preg_testpos', 'cp20q', 'cp21q', 'adole_wo_deliv','cp22q','cp23q','cp23qa','cp23qb','cp23qc','cp23qd'], ['AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES','AYES'], 'cp4b');
// validBench(['adole_gb_hse', 'cp24q', 'cp25q','cp26q','cp27q','cp28q','cp29q'], ['AYES','AYES','AYES','AYES','AYES','AYES','AYES'], 'cp5b');
validBench(['cp24q', 'cp25q','cp26q','cp27q','cp28q','cp29q'], ['AYES','AYES','AYES','AYES','AYES','AYES'], 'cp5b');
// validBench(['child_w_disab_hse', 'cp30q', 'cp31q'], ['AYES','AYES','AYES'], 'cp6b');
validBench(['cp30q', 'cp31q'], ['AYES','AYES'], 'cp6b');
validBench(['cp32q', 'cp33q', 'cp35q'], ['AYES','AYES','AYES'], 'cp7b');
validBench(['cp36q', 'cp37q', 'cp38q'], ['AYES','AYES','AYES'], 'cp8b');
validBench(['cp39q', 'cp40q'], ['AYES','AYES'], 'cp9b');
validBench(['cp41q', 'cp42q', 'cp43q'], ['AYES','AYES','AYES'], 'cp10b');
// validBench(['child_hd_hse', 'cp44q', 'cp45q','cp46q','cp47q','cp48q'], ['AYES','AYES','AYES','AYES','AYES','AYES'], 'cp11b');
validBench(['cp44q', 'cp45q','cp46q','cp47q','cp48q'], ['AYES','AYES','AYES','AYES','AYES'], 'cp11b');
validBench(['cp49q', 'cp50q', 'cp51q', 'o5y_cd_hse', 'cp52q', 'cp53q', 'cp54q'], ['AYES','AYES','AYES','AYES','AYES','AYES','AYES'], 'cp12b');
// validBench(['cld_rsk_abus', 'cp55q', 'cp56q', 'cp57q', 'cp58q', 'cp59q'], ['AYES','AYES','AYES','AYES','AYES','AYES'], 'cp13b');
validBench(['cp55q', 'cp56q', 'cp57q', 'cp58q', 'cp59q'], ['AYES','AYES','AYES','AYES','AYES'], 'cp13b');
validBench(['cp60q', 'cp61q'], ['AYES','AYES'], 'cp14b');
validBench(['cp62q', 'cp63q','cp64q','cp65q'], ['AYES','AYES','AYES','AYES'], 'cp15b');
validBench(['cp66q', 'cp67q','cp68q','cp69q','cp70q'], ['AYES','AYES','AYES','AYES','AYES'], 'cp16b');
// validBench(['adole_in_vc_train', 'cp71q','cp72q','cp73q'], ['AYES','AYES','AYES','AYES'], 'cp17b');
validBench(['cp71q','cp72q','cp73q'], ['AYES','AYES','AYES'], 'cp17b');


validDate('cp2d','cp1d','AYES','ANNO');
validDate('cp2q','cp1q','ANNO','AYES');

var benchmarkScore = 0;
$('input[name=cp74q]').attr('readonly', true);

// disable benchmark editing 
$('input[name=cp1b]').attr('disabled', true); $('input[name=cp2b]').attr('disabled', true); $('input[name=cp3b]').attr('disabled', true); $('input[name=cp4b]').attr('disabled', true); $('input[name=cp5b]').attr('disabled', true); $('input[name=cp6b]').attr('disabled', true); $('input[name=cp7b]').attr('disabled', true); $('input[name=cp8b]').attr('disabled', true); $('input[name=cp9b]').attr('disabled', true); $('input[name=cp10b]').attr('disabled', true); $('input[name=cp11b]').attr('disabled', true); $('input[name=cp12b]').attr('disabled', true); $('input[name=cp13b]').attr('disabled', true); $('input[name=cp14b]').attr('disabled', true); $('input[name=cp15b]').attr('disabled', true); $('input[name=cp16b]').attr('disabled', true); $('input[name=cp17b]').attr('disabled', true);
// disable benchmark editing

// benchmark score after change of last benchmark radio
$('input[name=cp17b], input[name=cp1b], input[name=cp2b], input[name=cp3b], input[name=cp4b], input[name=cp5b], input[name=cp6b], input[name=cp7b], input[name=cp8b], input[name=cp9b], input[name=cp10b], input[name=cp11b], input[name=cp12b], input[name=cp13b], input[name=cp14b], input[name=cp15b], input[name=cp16b], input[name=cp17b]').change(function (e) { 

    var cp1b = $('input[name=cp1b]:checked').val();
    if(cp1b === 'AYES'){cp1b = 1;}
    else if(cp1b === 'ANNO'){cp1b = 0;}
    
    var cp2b = $('input[name=cp2b]:checked').val();
    if(cp2b === 'AYES'){cp2b = 1;}
    else if(cp2b === 'ANNO'){cp2b = 0;}
    
    var cp3b = $('input[name=cp3b]:checked').val();
    if(cp3b === 'AYES'){cp3b = 1;}
    else if(cp3b === 'ANNO'){cp3b = 0;}
    
    var cp4b = $('input[name=cp4b]:checked').val();
    if(cp4b === 'AYES'){cp4b = 1;}
    else if(cp4b === 'ANNO'){cp4b = 0;}
    
    var cp5b = $('input[name=cp5b]:checked').val();
    if(cp5b === 'AYES'){cp5b = 1;}
    else if(cp5b === 'ANNO'){cp5b = 0;}
    
    var cp6b = $('input[name=cp6b]:checked').val();
    if(cp6b === 'AYES'){cp6b = 1;}
    else if(cp6b === 'ANNO'){cp6b = 0;}
    
    var cp7b = $('input[name=cp7b]:checked').val();
    if(cp7b === 'AYES'){cp7b = 1;}
    else if(cp7b === 'ANNO'){cp7b = 0;}
    
    var cp8b = $('input[name=cp8b]:checked').val();
    if(cp8b === 'AYES'){cp8b = 1;}
    else if(cp8b === 'ANNO'){cp8b = 0;}
    
    var cp9b = $('input[name=cp9b]:checked').val();
    if(cp9b === 'AYES'){cp9b = 1;}
    else if(cp9b === 'ANNO'){cp9b = 0;}
    
    var cp10b = $('input[name=cp10b]:checked').val();
    if(cp10b === 'AYES'){cp10b = 1;}
    else if(cp10b === 'ANNO'){cp10b = 0;}
    
    var cp11b = $('input[name=cp11b]:checked').val();
    if(cp11b === 'AYES'){cp11b = 1;}
    else if(cp11b === 'ANNO'){cp11b = 0;}
    
    var cp12b = $('input[name=cp12b]:checked').val();
    if(cp12b === 'AYES'){cp12b = 1;}
    else if(cp12b === 'ANNO'){cp12b = 0;}
    
    var cp13b = $('input[name=cp13b]:checked').val();
    if(cp13b === 'AYES'){cp13b = 1;}
    else if(cp13b === 'ANNO'){cp13b = 0;}
    
    var cp14b = $('input[name=cp14b]:checked').val();
    if(cp14b === 'AYES'){cp14b = 1;}
    else if(cp14b === 'ANNO'){cp14b = 0;}
    
    var cp15b = $('input[name=cp15b]:checked').val();
    if(cp15b === 'AYES'){cp15b = 1;}
    else if(cp15b === 'ANNO'){cp15b = 0;}
    
    var cp16b = $('input[name=cp16b]:checked').val();
    if(cp16b === 'AYES'){cp16b = 1;}
    else if(cp16b === 'ANNO'){cp16b = 0;}
    
    var cp17b = $('input[name=cp17b]:checked').val();
    if(cp17b === 'AYES'){cp17b = 1;}
    else if(cp17b === 'ANNO'){cp17b = 0;}

    benchmarkScore =  parseFloat(cp1b) + parseFloat(cp2b) + parseFloat(cp3b) + parseFloat(cp4b) + parseFloat(cp5b) + parseFloat(cp6b) + parseFloat(cp7b) + parseFloat(cp8b) + parseFloat(cp9b) + parseFloat(cp10b) + parseFloat(cp11b) + parseFloat(cp12b) + parseFloat(cp13b) + parseFloat(cp14b) + parseFloat(cp15b) + parseFloat(cp16b) + parseFloat(cp17b);

    $('input[name=cp74q]').val(benchmarkScore);
});

// benchmark score after change of last benchmark radio



// ----------------CORE----------------
function validBench(arrayOfInputsToCheck, arrayOfExpectedValues, idOfBenchmarkQn) {
    // $('input[name='+idOfBenchmarkQn+']').attr('disabled', true);

    // prevent manual benchmark ticking
    $('input[name='+idOfBenchmarkQn+']').change(function() {
        // var vf = $(this).val();
        // if(vf == 'AYES'){
        //     $('input[name='+idOfBenchmarkQn+'][value=ANNO]').prop("checked", true);
        // }else if(vf =='ANNO'){
        //     $('input[name='+idOfBenchmarkQn+'][value=ANNO]').prop("checked", true);
        // }
    });
    // prevent manual benchmark ticking

    var valToMatch = arrayOfInputsToCheck.length;
    var actualValNo = 1;
    $.each(arrayOfInputsToCheck, function (inde, inputName) {
        $('input[name='+inputName+']').change(function() {
            var thisval = $(this).val();
            if(thisval !== arrayOfExpectedValues[inde]){
                $('input[name='+idOfBenchmarkQn+']').removeAttr('disabled');
                $('input[name='+idOfBenchmarkQn+'][value=ANNO]').prop("checked", true);
                $('input[name='+idOfBenchmarkQn+']').attr('disabled', true);
                if(thisval === arrayOfExpectedValues[inde]){
                    actualValNo = actualValNo + 1;
                }else{
                    actualValNo = actualValNo;
                    if(actualValNo<1){
                        actualValNo = 1;
                    }
                }
            }else{

                if(actualValNo == valToMatch){
                    $('input[name='+idOfBenchmarkQn+']').removeAttr('disabled');
                    $('input[name='+idOfBenchmarkQn+'][value=AYES]').prop("checked", true);
                    $('input[name='+idOfBenchmarkQn+']').attr('disabled', true);
                    //update benchmark score
                    // benchmarkScore = benchmarkScore + 1
                    // $('input[name=cp74q]').val(benchmarkScore);
                    // console.log("added benchmark + 1 = "+benchmarkScore);
                    //update benchmark score
                }else{
                    $('input[name='+idOfBenchmarkQn+']').removeAttr('disabled');
                    $('input[name='+idOfBenchmarkQn+'][value=ANNO]').prop("checked", true);
                    $('input[name='+idOfBenchmarkQn+']').attr('disabled', true);
                    // console.log('2nd NOone works');
                    if(thisval === arrayOfExpectedValues[inde]){
                        actualValNo = actualValNo + 1;
                    }else{
                        actualValNo = actualValNo;
                        if(actualValNo<1){
                            actualValNo = 1;
                        }
                    }
                }
                // alert(actualValNo+'/'+valToMatch);
            }
        });
        
    });


}


function validDate(dateFieldName, radioToCheck, rightValue, wrongValue) {
    $('input[name='+dateFieldName+']').attr('disabled', true);
	$('input[name='+radioToCheck+']').change(function(){
		var valu = $(this).val();
		if(valu === rightValue){
			$('input[name='+dateFieldName+']').val('');
			$('input[name='+dateFieldName+']').attr('disabled', true);
			$('input[name='+dateFieldName+']').removeAttr('required');
			$('input[name='+dateFieldName+']').attr('data-parsley-required', false);
		}else if(valu === wrongValue){
			$('input[name='+dateFieldName+']').attr('data-parsley-required', true);
			$('input[name='+dateFieldName+']').val('');
			$('input[name='+dateFieldName+']').removeAttr('disabled');
		}
	});
}
// end----------------CORE----------------