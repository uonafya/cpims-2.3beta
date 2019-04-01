jQuery(document).ready(function()
{
	 //multi selects
    $('.goals_cell > div > select, .gaps_cell > div > select, .actions_cell > div > select, .services_cell > div > select').multiselect({
        selectAllValue: 'multiselect-all',
        includeSelectAllOption: true,
        enableCaseInsensitiveFiltering: true,
        numberDisplayed: 1,
        maxHeight: 300,
        buttonWidth: '100%',
        buttonClass: 'btn btn-white'
    });
    $('#CPT_DATE').datepicker({ format: 'dd-M-yyyy' });

    FormWizardValidation.init();
    
    // onDomainChange
    $('select[name=CPT_DOMAIN]').change(function (e) { 
        // e.preventDefault();
        var domain_val = $('select[name=CPT_DOMAIN] option:selected').val();
        if(domain_val === 'SCH'){
            $('.school_form').each(function () {
                $(this).removeClass('hidden');
            })
            $('.healthy_form, .stable_form, .safe_form').each(function () {
                $(this).addClass('hidden');
            })
        }else if(domain_val === 'STB'){
            $('.healthy_form, .safe_form, .school_form').each(function () {
                $(this).addClass('hidden');
            })
            $('.stable_form').each(function () {
                $(this).removeClass('hidden');
            })
        }else if(domain_val === 'SF'){
            $('.healthy_form, .school_form, .stable_form').each(function () {
                $(this).addClass('hidden');
            })
            $('.safe_form').each(function () {
                $(this).removeClass('hidden');
            })
        }else if(domain_val === 'HE'){
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

function stripHTML(strWithHTML) {
    var container = document.createElement('div');
    var text = document.createTextNode(strWithHTML);
    container.appendChild(text);
    return container.innerHTML;
  }

function AddRow() {    
    var randomID = randomNo();
    $('#submissions_table tbody').append('<tr id="row_'+randomID+'"> <td id="tbl_domain"></td> <td id="tbl_goal"><ul class="ul-flow"></ul></td> <td id="tbl_needs"><ul class="ul-flow"></ul></td> <td id="tbl_actions"><ul class="ul-flow"></ul></td> <td id="tbl_services"><ul class="ul-flow"></ul></td> <td id="tbl_repsonsible"></td> <td id="tbl_datecompleted"></td> <td id="tbl_results"></td> <td id="tbl_reasons"></td> <td id="tbl_acts"></td></tr>');
    
    let domain = $('#id_CPT_DOMAIN option:selected').val();
    
    // let goal = $('.goals_cell > div:not(.hidden) > select > option').val();
    let goal = []
    $('.goals_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
        var vlu = $(this).val();
        if(vlu !== 'multiselect-all'){
            goal.push(vlu);
        }
    })

    // let gaps = $('.gaps_cell > div:not(.hidden) > select > option:selected').val();
    let gaps = []
    $('.gaps_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
        var vlu2 = $(this).val();
        if(vlu2 !== 'multiselect-all'){
            gaps.push(vlu2);
        }
    })

    // let actions = $('.actions_cell > div:not(.hidden) > select > option:selected').val();
    let actions = []
    $('.actions_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
        var vlu3 = $(this).val();
        if(vlu3 !== 'multiselect-all'){
            actions.push(vlu3);
        }
    })

    // let services = $('.services_cell > div:not(.hidden) > select > option:selected').val();
    let services = []
    $('.services_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
        var vlu = $(this).val();
        if(vlu !== 'multiselect-all'){
            services.push(vlu);
        }
    })

    let responsibl = $('#id_CPT_RESPONSIBLE option:selected').val();
    let date = $('#CPT_DATE').val();
    let results = $('#id_CPT_RESULTS option:selected').val();
    let reasons = $('#id_CPT_REASONS').val();

    // domain
    $('#row_'+randomID+' > td#tbl_domain').html( $('select[name=CPT_DOMAIN] option[value='+domain+']').text() + '<input type="hidden" name="h_CPT_DOMAIN" value="'+domain+'" />');
    // -domain
    // goal
    $('#row_'+randomID+' > td#tbl_goal > ul.ul-flow').empty();
    $('.goals_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active label[class=checkbox]').each(function () {
        var txt = stripHTML($(this).text());
        if(txt !== 'Select all'){
            $('#row_'+randomID+' > td#tbl_goal > ul.ul-flow').append( '<li>'+txt+'</li>' );
        }
    })
    $('#row_'+randomID+' > td#tbl_goal').append('<input type="hidden" name="h_CPT_GOAL" value="'+goal+'" />');
    // -goal
    // gaps
    $('#row_'+randomID+' > td#tbl_needs > ul.ul-flow').empty();
    $('.gaps_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active label[class=checkbox]').each(function () {
        var txt2 = stripHTML($(this).text());
        if(txt2 !== 'Select all'){
            $('#row_'+randomID+' > td#tbl_needs > ul.ul-flow').append( '<li>'+txt2+'</li>' );
        }
    });
    $('#row_'+randomID+' > td#tbl_needs').append('<input type="hidden" name="h_CPT_GAPS" value="'+gaps+'" />');
    // -gaps
    // actions
    $('#row_'+randomID+' > td#tbl_actions > ul.ul-flow').empty();
    $('.actions_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active label[class=checkbox]').each(function () {
        var txt3 = stripHTML($(this).text());
        if(txt3 !== 'Select all'){
            $('#row_'+randomID+' > td#tbl_actions > ul.ul-flow').append( '<li>'+txt3+'</li>' );
        }
    });
    $('#row_'+randomID+' > td#tbl_actions').append('<input type="hidden" name="h_CPT_ACTIONS" value="'+actions+'" />');
    // -actions
    // services
    $('#row_'+randomID+' > td#tbl_services > ul.ul-flow').empty();
    $('.services_cell > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active label[class=checkbox]').each(function () {
        var txt4 = stripHTML($(this).text());
        if(txt4 !== 'Select all'){
            $('#row_'+randomID+' > td#tbl_services > ul.ul-flow').append( '<li>'+txt4+'</li>' );
        }
    });
    $('#row_'+randomID+' > td#tbl_services').append('<input type="hidden" name="h_CPT_SERVICES" value="'+services+'" />');
    // -services

    $('#row_'+randomID+' > td#tbl_repsonsible').html( $('select[name=CPT_RESPONSIBLE] option[value='+responsibl+']').text() + '<input type="hidden" name="h_CPT_RESPONSIBLE" value="'+responsibl+'" />');
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
            8: results,
            9: reasons
        })
    )
    $('#row_'+randomID+' > td#tbl_acts > .removerow').click(function (e) { 
        e.preventDefault();
        $('#row_'+randomID).empty();
        $('#row_'+randomID).remove();

        // $(this).closest('tr').empty();
        // $(this).closest('tr').remove();
    });

}