jQuery(document).ready(function()
{
	 //multi selects
    $('.responsible_cell > select, .services_cell > div > select').multiselect({
    // $('.services_cell > div > select').multiselect({
        selectAllValue: 'multiselect-all',
        includeSelectAllOption: true,
        enableCaseInsensitiveFiltering: true,
        numberDisplayed: 1,
        maxHeight: 300,
        buttonWidth: '100%',
        buttonClass: 'btn btn-white'
    });
    $('input, select').attr('required', true);
    $('.goals_cell > div > select, .gaps_cell > div > select, .actions_cell > div > select, .domain_cell > select, #id_CPT_RESPONSIBLE').prepend('<option value="" selected>Pick an item</option>');
    $('#CPT_DATE').datepicker({ format: 'yyyy-mm-dd' });
    $('#CPT_ACTUAL_DATE_COMPLETION').removeAttr('required');
    $('#CPT_ACTUAL_DATE_COMPLETION').datepicker({ format: 'yyyy-mm-dd' });
    $('input[name=CPT_DATE_CASEPLAN]').datepicker({ format: 'yyyy-mm-dd' });
    $('input[name=date_first_cpara]').datepicker({ format: 'yyyy-mm-dd' });

    FormWizardValidation.init();
    
    // onDomainChange
    $('select[name=CPT_DOMAIN]').change(function (e) { 
        e.preventDefault();
        var domain_val = $('select[name=CPT_DOMAIN] option:selected').val();
        if(domain_val === 'DEDU'){
            $('.school_form').each(function () {
                $(this).removeClass('hidden');
            })
            $('.healthy_form, .stable_form, .safe_form').each(function () {
                $(this).addClass('hidden');
            })
        }else if(domain_val === 'DHES'){
            $('.healthy_form, .safe_form, .school_form').each(function () {
                $(this).addClass('hidden');
            })
            $('.stable_form').each(function () {
                $(this).removeClass('hidden');
            })
        }else if(domain_val === 'DPRO'){
            $('.healthy_form, .school_form, .stable_form').each(function () {
                $(this).addClass('hidden');
            })
            $('.safe_form').each(function () {
                $(this).removeClass('hidden');
            })
        }else if(domain_val === 'DHNU'){
            $('.stable_form, .safe_form, .school_form').each(function () {
                $(this).addClass('hidden');
            })
            $('.healthy_form').each(function () {
                $(this).removeClass('hidden');
            })
        }
    });
    // onDomainChange
});

function randomNo() {
    var min=101; 
    var max=1999;  
    var random = Math.random() * (+max - +min) + +min; 
    random = random.toFixed(0);
    return random;
}

function cancelBtn() {
    window.location.reload();
}
function stripHTML(strWithHTML) {
    var container = document.createElement('div');
    var text = document.createTextNode(strWithHTML);
    container.appendChild(text);
    return container.innerHTML;
  }
var final_input = {};
final_input['domain'] = [];
final_input['goal'] = [];
final_input['gaps'] = [];
final_input['actions'] = [];
final_input['services'] = [];
final_input['responsible'] = [];
final_input['date'] = [];
final_input['actual_completion_date'] = [];
final_input['results'] = [];
final_input['reasons'] = [];
final_input['if_first_cpara'] = [];
final_input['date_first_cpara'] = [];
final_input['CPT_DATE_CASEPLAN'] = [];

$('input[name="CPT_DATE_CASEPLAN"]').click(function (e) { 
    $('.waleert').remove();
    $('input, select, .multiselect.dropdown-toggle.btn.btn-white').css({'border-color':'#ccd0d4'});
});


function submitCPT() {

        // e.preventDefault();
        var row_count = 0;
        $('#submissions_table tbody tr').each(function (index, element) {
            row_count = row_count + 1;
        });

        if(row_count < 1){
            var msg = "Please add some rows of data to be submitted first";
            console.error('ERROR: no rows of data entered');
            $('#js_error span.mesgg').html(msg);
            $('#js_error').removeClass('hidden');
            $(window).scrollTop(0);
            return false;
        }else{
            var msg = "";
            $('#js_error span.mesgg').html(msg);
            $('#js_error').addClass('hidden');
        }

        // console.log("final_input: "+JSON.stringify(final_input));
        var date_of_caseplan = $('input[name=CPT_DATE_CASEPLAN]').val();
    
            $.each(final_input['domain'], function (indexDomain, oneDomain) {
                var answrs = {};
    
                answrs['domain'] = [];
                answrs['goal'] = [];
                answrs['gaps'] = [];
                answrs['actions'] = [];
                answrs['services'] = [];
                answrs['responsible'] = [];
                answrs['date'] = [];
                answrs['actual_completion_date'] = [];
                answrs['results'] = [];
                answrs['reasons'] = [];
                answrs['if_first_cpara'] = [];
                answrs['date_first_cpara'] = [];
                answrs['CPT_DATE_CASEPLAN'] = [];
    
                answrs['domain'] = final_input['domain'][indexDomain];
                answrs['goal'] = final_input['goal'][indexDomain];
                answrs['gaps'] = final_input['gaps'][indexDomain];
                answrs['actions'] = final_input['actions'][indexDomain];
                answrs['services'] = final_input['services'][indexDomain];
                answrs['responsible'] = final_input['responsible'][indexDomain];
                answrs['date'] = final_input['date'][indexDomain];
                answrs['actual_completion_date'] = final_input['actual_completion_date'][indexDomain];
                answrs['results'] = final_input['results'][indexDomain];
                answrs['reasons'] = final_input['reasons'][indexDomain];
                answrs['if_first_cpara'] = final_input['if_first_cpara'][indexDomain];
                answrs['date_first_cpara'] = final_input['date_first_cpara'][indexDomain];
                answrs['CPT_DATE_CASEPLAN'] = final_input['CPT_DATE_CASEPLAN'][indexDomain];
    
                fd2.push(answrs);
            });
            console.log("answrs: "+JSON.stringify(fd2));
            $('input[name=final_submission').val(JSON.stringify(fd2));
            $('#new_f1a').submit();
    
}


function AddRow() {    
    var randomID = randomNo();
    
    
    let domain = $('#id_CPT_DOMAIN option:selected').val();
    
    let goal = $('.goals_cell > div:not(.hidden) > select > option:selected').val();
    // let goal = []
    // $('.goals_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
    //     var vlu = $(this).val();
    //     if(vlu !== 'multiselect-all'){
    //         goal.push(vlu);
    //     }
    // })

    let gaps = $('.gaps_cell > div:not(.hidden) > select > option:selected').val();
    // let gaps = []
    // $('.gaps_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
    //     var vlu2 = $(this).val();
    //     if(vlu2 !== 'multiselect-all'){
    //         gaps.push(vlu2);
    //     }
    // })

    let actions = $('.actions_cell > div:not(.hidden) > select > option:selected').val();
    // let actions = []
    // $('.actions_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
    //     var vlu3 = $(this).val();
    //     if(vlu3 !== 'multiselect-all'){
    //         actions.push(vlu3);
    //     }
    // })

    // let services = $('.services_cell > div:not(.hidden) > select > option:selected').val();
    let services = []
    $('.services_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
        var vlu = $(this).val();
        if(vlu !== 'multiselect-all'){
            services.push(vlu);
        }
    })

    let responsibl = []
    $('.responsible_cell div.btn-group ul.multiselect-container.dropdown-menu li.active a label.checkbox input[type=checkbox]').each(function () {
        var vlue = $(this).val();
        if(vlue !== 'multiselect-all'){
            responsibl.push(vlue);
        }
    })

    let results = $('#id_CPT_RESULTS option:selected').val();
    let results2 = $('#id_CPT_RESULTS').val();
    let reasons = $('#id_CPT_REASONS').val();
    
    // let responsibl = $('#id_CPT_RESPONSIBLE option:selected').val();

    let date = $('#CPT_DATE').val();
    let actual_completion_date = $('#CPT_ACTUAL_DATE_COMPLETION').val();
    let if_first_cpara = $('input[name=if_first_cpara]:checked').val();
    let date_first_cpara = $('input[name=date_first_cpara]').val();
    let CPT_DATE_CASEPLAN = $('input[name=CPT_DATE_CASEPLAN]').val();
    $('.waleert').remove();

    $('input, select').change(function (e) { 
        // $(this).attr('data-change', 1)
        $(this).addClass('d-c-1')
    });

    //if (CPT_DATE_CASEPLAN == null || CPT_DATE_CASEPLAN == '' || actual_completion_date == null || actual_completion_date == '' || domain == 
    if (CPT_DATE_CASEPLAN == null || CPT_DATE_CASEPLAN == '' || domain == null || domain == '' || goal == '' || goal == null || actions == '' || actions == null || gaps == '' || gaps == null || services.length < 1 || results == '' || results2 == null || results2 == '' || reasons == '' ){
        // $('input[name=CPT_DATE_CASEPLAN]').css('border', '1px solid red');
        $('input:not(.d-c-1), select:not(.d-c-1), .multiselect.dropdown-toggle.btn.btn-white').not('a[tabindex] label.checkbox input[type=checkbox]').css('border', '1px solid red');
        console.error('ERROR: can\'t add rows with empty fields')
        // $('#CPT_DATE_CASEPLAN_state').empty();
        // $('input[name=CPT_DATE_CASEPLAN]').after("<small id='CPT_DATE_CASEPLAN_state' style='color: red'>This field is required</small>");
        $('input:not(.d-c-1), select:not(.d-c-1)').not('a[tabindex] label.checkbox input[type=checkbox]').before("<small id='CPT_DATE_CASEPLAN_state' class='waleert' style='color: red'>This field is required</small>");
        var proceed = false;
    }else{
        var proceed = true;
    }
    $('input, select').focus(function (e) { 
        // $('input[name=CPT_DATE_CASEPLAN]').css('border', '1px solid #9fa2a5');
        $('input, select, .multiselect.dropdown-toggle.btn.btn-white').css('border', '1px solid #9fa2a5');
        // $('#CPT_DATE_CASEPLAN_state').empty();
        $('.waleert').remove();
    });
    

    if(proceed){
        $('#submissions_table tbody').append('<tr id="row_'+randomID+'"> <td id="tbl_domain"></td> <td id="tbl_goal"><ul class="ul-flow"></ul></td> <td id="tbl_needs"><ul class="ul-flow"></ul></td> <td id="tbl_actions"><ul class="ul-flow"></ul></td> <td id="tbl_services"><ul class="ul-flow"></ul></td> <td id="tbl_responsible"><ul class="ul-flow"></ul></td> <td id="tbl_datecompleted"></td> <td id="tbl_results"></td> <td id="tbl_reasons"></td> <td id="tbl_acts"></td></tr>');
        // domain
        $('#row_'+randomID+' > td#tbl_domain').html( $('select[name=CPT_DOMAIN] option[value='+domain+']').text() + '<input type="hidden" name="h_CPT_DOMAIN" value="'+domain+'" />');
        // -domain

        // goal
        $('#row_'+randomID+' > td#tbl_goal').html( $('.goals_cell > div:not(.hidden) > select option:selected').text() + '<input type="hidden" name="h_CPT_GOAL" value="'+goal+'" />');
        // -goal

        // gaps
        $('#row_'+randomID+' > td#tbl_needs').html( $('.gaps_cell > div:not(.hidden) > select option:selected').text() + '<input type="hidden" name="h_CPT_GAPS" value="'+gaps+'" />');
        // -gaps

        // actions
        $('#row_'+randomID+' > td#tbl_actions').html( $('.actions_cell > div:not(.hidden) > select option[value='+actions+']').text() + '<input type="hidden" name="h_CPT_ACTIONS" value="'+actions+'" />');
        // -actions

        // services
        $('#row_'+randomID+' > td#tbl_services > ul.ul-flow').empty();
        $('.services_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active label[class=checkbox]').each(function () {
            var txt5 = stripHTML($(this).text());
            if(txt5 === 'Select all'){}else{
                $('#row_'+randomID+' > td#tbl_services > ul.ul-flow').append( '<li>'+txt5+'</li>' );
            }
        });
        $('#row_'+randomID+' > td#tbl_services').append('<input type="hidden" name="h_CPT_SERVICES" value="'+services+'" />');
        // -services

        // responsible
        $('#row_'+randomID+' > td#tbl_responsible > ul.ul-flow').empty();
        // $('.responsible_cell > div.btn-group > ul.multiselect-container > li.active label[class=checkbox]').each(function () {
        $('.responsible_cell div.btn-group ul.multiselect-container.dropdown-menu li.active a label.checkbox').each(function () {
            var txt4 = stripHTML($(this).text());
            if(txt4 === 'Select all'){}else{
                $('#row_'+randomID+' > td#tbl_responsible > ul.ul-flow').append( '<li>'+txt4+'</li>' );
            }
        });
        $('#row_'+randomID+' > td#tbl_responsible').append('<input type="hidden" name="h_CPT_RESPONSIBLE" value="'+responsibl+'" />');
        // -responsible

        // $('#row_'+randomID+' > td#tbl_responsible').html( $('select[name=CPT_RESPONSIBLE] option[value='+responsibl+']').text() + '<input type="hidden" name="h_CPT_RESPONSIBLE" value="'+responsibl+'" />');

        $('#row_'+randomID+' > td#tbl_datecompleted').html(date + '<input type="hidden" name="h_CPT_DATE" value="'+date+'" />');
        $('#row_'+randomID+' > td#tbl_results').html( $('select[name=CPT_RESULTS] option[value='+results+']').text() + '<input type="hidden" name="h_CPT_RESULTS" value="'+results+'" />');
        $('#row_'+randomID+' td#tbl_reasons').html('<div>'+reasons+'</div>' + '<input type="hidden" name="h_CPT_REASONS" value="'+reasons+'" />');
        $('#row_'+randomID+' td#tbl_acts').html('<a href="#" class="removerow btn btn-xs btn-danger"><i class="fa fa-trash"></i> Remove</a>');

        console.log(
            'LOG: '+JSON.stringify({
                1: domain,
                2: goal,
                3: gaps,
                4: actions,
                5: services,
                6: responsibl,
                7: date,
                8: actual_completion_date,
                9: results,
                10: reasons
            })
        )

        final_input['domain'].push(domain);
        final_input['goal'].push(goal);
        final_input['gaps'].push(gaps);
        final_input['actions'].push(actions);
        final_input['services'].push(services);
        final_input['responsible'].push(responsibl);
        final_input['date'].push(date);
        final_input['actual_completion_date'].push(actual_completion_date);
        final_input['results'].push(results);
        final_input['reasons'].push(reasons);
        final_input['if_first_cpara'].push(if_first_cpara);
        final_input['date_first_cpara'].push(date_first_cpara);
        final_input['CPT_DATE_CASEPLAN'].push(CPT_DATE_CASEPLAN);

        $('#row_'+randomID+' > td#tbl_acts > .removerow').click(function (e) {
            e.preventDefault();
            $('#row_'+randomID).empty();
            $('#row_'+randomID).remove();

            // $(this).closest('tr').empty();
            // $(this).closest('tr').remove();
        });
    }

}

var fd2 = [];
// function submitCPT() {

//     // e.preventDefault();
//     console.log('hoo');
//     var row_count = 0;
//     $('#cpt_table tbody row').each(function (index, element) {
//         row_count = row_count + 1;
//     });
//     if(row_count < 1){
//         var msg = "Please add some rows of data to be submitted first";
//         console.error('ERROR: no rows of data entered');
//         $(window).scrollTop(0);
//         $('#warning_message').removeClass('hidden');
//         $('#warning_message span.mesagg').html(msg);
//         return false;
//     }else{
//         $('#warning_message').addClass('hidden');
//         $('#warning_message span.mesagg').html('');
//     }
//     // console.log("final_input: "+JSON.stringify(final_input));
//     var date_of_caseplan = $('input[name=CPT_DATE_CASEPLAN]').val();

//         $.each(final_input['domain'], function (indexDomain, oneDomain) {
//             var answrs = {};

//             answrs['domain'] = [];
//             answrs['goal'] = [];
//             answrs['gaps'] = [];
//             answrs['actions'] = [];
//             answrs['services'] = [];
//             answrs['responsible'] = [];
//             answrs['date'] = [];
//             answrs['actual_completion_date'] = [];
//             answrs['results'] = [];
//             answrs['reasons'] = [];
//             answrs['if_first_cpara'] = [];
//             answrs['date_first_cpara'] = [];
//             answrs['CPT_DATE_CASEPLAN'] = [];

//             answrs['domain'] = final_input['domain'][indexDomain];
//             answrs['goal'] = final_input['goal'][indexDomain];
//             answrs['gaps'] = final_input['gaps'][indexDomain];
//             answrs['actions'] = final_input['actions'][indexDomain];
//             answrs['services'] = final_input['services'][indexDomain];
//             answrs['responsible'] = final_input['responsible'][indexDomain];
//             answrs['date'] = final_input['date'][indexDomain];
//             answrs['actual_completion_date'] = final_input['actual_completion_date'][indexDomain];
//             answrs['results'] = final_input['results'][indexDomain];
//             answrs['reasons'] = final_input['reasons'][indexDomain];
//             answrs['if_first_cpara'] = final_input['if_first_cpara'][indexDomain];
//             answrs['date_first_cpara'] = final_input['date_first_cpara'][indexDomain];
//             answrs['CPT_DATE_CASEPLAN'] = final_input['CPT_DATE_CASEPLAN'][indexDomain];

//             fd2.push(answrs);
//         });
//         console.log("answrs: "+JSON.stringify(fd2));
//         $('input[name=final_submission').val(JSON.stringify(fd2));
//         $('#new_f1a').submit();


// }
