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


// ----------------CORE----------------
function validBench(arrayOfInputsToCheck, arrayOfExpectedValues, idOfBenchmarkQn) {
    // $('input[name='+idOfBenchmarkQn+']').attr('disabled', true);
    $('input[name='+idOfBenchmarkQn+']').change(function() {
        var vf = $(this).val();
        if(vf == 'AYES'){
            $('input[name='+idOfBenchmarkQn+'][value=ANNO]').prop("checked", true);
        }else if(vf =='ANNO'){
            $('input[name='+idOfBenchmarkQn+'][value=ANNO]').prop("checked", true);
        }
    });

    var valToMatch = arrayOfInputsToCheck.length;
    var actualValNo = 1;
    $.each(arrayOfInputsToCheck, function (inde, inputName) {
        $('input[name='+inputName+']').change(function() {
            var thisval = $(this).val();
            if(thisval !== arrayOfExpectedValues[inde]){
                $('input[name='+idOfBenchmarkQn+']').removeAttr('disabled');
                $('input[name='+idOfBenchmarkQn+'][value=ANNO]').prop("checked", true);
                // console.log('first NOone works');
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
                    console.log('2nd YESone works');
                    //update benchmark score
                    benchmarkScore = benchmarkScore + 1
                    $('input[name=cp74q]').val(benchmarkScore);
                    console.log("added benchmark + 1 = "+benchmarkScore);
                    //update benchmark score
                }else{
                    $('input[name='+idOfBenchmarkQn+']').removeAttr('disabled');
                    $('input[name='+idOfBenchmarkQn+'][value=ANNO]').prop("checked", true);
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