var handleBootstrapWizardsValidation = function() {
    "use strict";
    var error_msg = 'Please provide required ';
    $("#mysubmit").removeClass( "btn-primary" ).attr("disabled", "disabled");
    $("#mysubmit3").removeClass( "btn-primary" ).attr("disabled", "disabled");
    $("#mysubmit10").removeClass( "btn-primary" ).attr("disabled", "disabled");
    $("#mysubmit-csi").removeClass( "btn-primary" ).attr("disabled", "disabled");
    $("#mysubmit-f1a").removeClass( "btn-primary" ).attr("disabled", "disabled");
    $("#mysubmit-hhva").removeClass( "btn-primary" ).attr("disabled", "disabled");
    
    $("#wizard").bwizard({ validating: function (e, ui) {
        $(".alert").hide();
         if (ui.index == 0) {
            // step-1 validation
            if (false === $('form[name="form-wizard"]').parsley().validate('primary')) {
                $(".alert").show();
                $('.invalid-form-message').html(error_msg + 'details about the organisation.');
                return false;
            }
        } else if ((ui.index == 1) && (ui.nextIndex > ui.index)){
            // step-2 validation
              if (false === $('form[name="form-wizard"]').parsley().validate('primary1')) {
                $(".alert").show();
                $('.invalid-form-message').html(error_msg + 'organisation type details.');
                return false;
            }
        } else if ((ui.index == 2) && (ui.nextIndex > ui.index)) {
            // step-3 validation
            if (false === $('form[name="form-wizard"]').parsley().validate('primary2')) {
                $(".alert").show();
                $('.invalid-form-message').html(error_msg + 'location details.');
                return false;
            }
        } else if ((ui.index == 3) && (ui.nextIndex >= ui.index)) {
            // step-4 validation
            if (false === $('form[name="form-wizard"]').parsley().validate('primary3')) {
                $(".alert").show();
                $('.invalid-form-message').html(error_msg + 'contacts details.');
                return false;
            }
        }
        if (ui.nextIndex == 3) {
            $("#mysubmit").addClass( "btn-primary" ).removeAttr("disabled");
        }else{
            $("#mysubmit").removeClass( "btn-primary" ).attr("disabled", "disabled");
        }
    }});
    $("#wizard2").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard2"]').parsley().validate('group0')) {
                    return false;
                }
            } else if (ui.index == 1) {
                // step-2 validation
                
                $("#mysubmit2").addClass( "btn-primary" ).removeAttr("disabled");
                  if (false === $('form[name="form-wizard2"]').parsley().validate('group1')) {
                    return false;
                }
            }else if (ui.index == 2) {
                // step-3 validation
                 
                  if (false === $('form[name="form-wizard2"]').parsley().validate('group2')) {
                    return false;
                }
            } 
        } 
    });

   $("#wizard3").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard3"]').parsley().validate('group0')) {
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + 'case reporting details.');
                    return false;
                }
                else { $(".alert").hide(); }
            } else if (ui.index == 1) {
                // step-2 validation
                //$("#mysubmit3").addClass( "btn-primary" ).removeAttr("disabled");
                if (false === $('form[name="form-wizard3"]').parsley().validate('group1')) {
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + 'about the child details.');
                    return false;
                }
                else { $(".alert").hide(); }
            }else if (ui.index == 2) {
                // step-3 validation                 
                $("#mysubmit3").addClass( "btn-primary" ).removeAttr("disabled");
                if (false === $('form[name="form-wizard3"]').parsley().validate('group2')) {
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + 'medical details.');
                    return false;
                }
                else { $(".alert").hide(); }
            }else if (ui.index == 3) {
                // step-4 validation
                var refferalsPresent = $('#refferal_present').val();
                var rowCases = $('#casecategory_manager_table tr').length;
                var rowReferrals = $('#referralactors_table tr').length;

                if (rowCases == 3)
                { 
                    $('#div_casecategory_errormsgs').css({'display': 'block'})
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + 'case category details.');
                    return false;
                } 
                else if(rowReferrals == 3 && refferalsPresent =='AYES')
                {
                    $('#div_referralactors_errormsgs').css({'display': 'block'})
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + 'referral details.');
                    return false;
                }
                else
                {
                    if (false === $('form[name="form-wizard3"]').parsley().validate('group3')) {
                        $(".alert").show();
                        $('.invalid-form-message').html(error_msg + 'case data details.');
                        return false;
                    }
                }
                    
            } 
      }            
    });

    $("#wizard_placement").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard-placement"]').parsley().validate('group0')) {
                    return false;
                }
            } else if (ui.index == 1) {
                // step-2 validation
                $("#mysubmit10").addClass( "btn-primary" ).removeAttr("disabled");
                if (false === $('form[name="form-wizard-placement"]').parsley().validate('group1')) {
                    return false;
                }
            }
      }            
    });

    $("#wizard_familycare").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard-family-care"]').parsley().validate('group0')) {
                    return false;
                }
            } 
      }            
    });

    $("#wizard_education").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard-education"]').parsley().validate('group0')) {
                    return false;
                }
            } 
      }            
    });

    $("#wizard_school").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard-school"]').parsley().validate('group0')) {
                    return false;
                }
            } 
      }            
    });

    $("#wizard_bursary").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard-bursary"]').parsley().validate('group0')) {
                    return false;
                }
            } 
      }            
    });

    $("#wizard_placementfollowup").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard-placementfollowup"]').parsley().validate('group0')) {
                    return false;
                }
            } else if (ui.index == 1) {
                // step-2 validation
                if (false === $('form[name="form-wizard-placementfollowup"]').parsley().validate('group1')) {
                    return false;
                }
            }else if (ui.index == 2) {
                // step-2 validation
                //$("#mysubmit3").addClass( "btn-primary" ).removeAttr("disabled");
                if (false === $('form[name="form-wizard-placementfollowup"]').parsley().validate('group2')) {
                    return false;
                }
            }
      }            
    });
    
    $("#wizard_persons").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard"]').parsley().validate('group0')) {
                    return false;
                }
            } else if (ui.index == 1) {
                // step-2 validation 
                $("#mysubmit2").addClass( "btn-primary" ).removeAttr("disabled");
                  if (false === $('form[name="form-wizard"]').parsley().validate('group1')) {
                    return false;
                }
            }else if (ui.index == 2) {
                // step-3 validation  
                  if (false === $('form[name="form-wizard"]').parsley().validate('group2')) {
                    return false;
                }
            }else if (ui.index == 3) {
                // step-4 validation     
                  if (false === $('form[name="form-wizard"]').parsley().validate('group3')) {
                    return false;
                }
            }else if (ui.index == 4) {
                // step-5 validation     
                  if (false === $('form[name="form-wizard"]').parsley().validate('group4')) {
                    return false;
                }
            } 
        } 
    });

    $("#wizard-csi").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard-csi"]').parsley().validate('group0')) {
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + ' CSI domain evaluation details.');
                    return false;
                }
                $(".alert").hide();
            } else if (ui.index == 1) {
                // step-2 validation
                $("#mysubmit-csi").addClass( "btn-primary" ).removeAttr("disabled"); 
                var rows = $('#priority_manager_table tr').length;
                if (rows == 2)
                {
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + ' CSI priority details.Add one or more CSI priorities.');
                    return false;
                } 
                $(".alert").hide();
            }else if (ui.index == 2) {
                // step-3 validation
                if (false === $('form[name="form-wizard-csi"]').parsley().validate('group2')) {
                    return false;
                }
            }
        } 
    });

    $("#wizard-f1a").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                $(".alert").hide();
            } 
            else if (ui.index == 1) {
                // step-2 validation
                $(".alert").hide();
            }
            else if (ui.index == 2) {
                // step-3 validation
                $(".alert").hide();
            } 
            else if (ui.index == 3) {
                // step-4 validation
                $(".alert").hide();
            }
        }
    });

    $("#wizard-hhva").bwizard({ validating: function (e, ui) { 
            $(".alert").hide();
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group0')) {
                    return false;
                }
            } 
            else if (ui.index == 1) {
                // step-2 validation
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group1')) {
                    return false;
                }
            }
            else if (ui.index == 2) {
                // step-3 validation
                var rows = $('#ha10_manager_table tr').length;                 
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group2')) {
                    return false;
                }
                else if (rows == 2)
                {
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + ' bedding details.Add one or more bedding.');
                    return false;
                }
            } 
            else if (ui.index == 3) {
                // step-4 validation
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group3')) {
                    return false;
                }
            }
            else if (ui.index == 4) {
                // step-4 validation
                var rows = $('#ha15_manager_table tr').length;                 
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group4')) {
                    return false;
                }
                else if (rows == 2)
                {
                    $(".alert").show();
                    $('.invalid-form-message').html(error_msg + ' household asset details.Add one or more asset.');
                    return false;
                }
            }
            else if (ui.index == 5) {
                // step-4 validation
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group5')) {
                    return false;
                }
            }
            else if (ui.index == 6) {
                // step-4 validation
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group6')) {
                    return false;
                }
            }
            else if (ui.index == 7) {
                // step-4 validation
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group7')) {
                    return false;
                }
                $("#mysubmit-hhva").addClass( "btn-primary" ).removeAttr("disabled"); 
            }
            else if (ui.index == 8) {
                // step-4 validation
                if (false === $('form[name="form-wizard-hhva"]').parsley().validate('group8')) {
                    return false;
                }
            }            
        }
    });
};

var FormWizardValidation = function () {
    "use strict";
    return {
        //main function
        init: function () {
            handleBootstrapWizardsValidation();
        }
    };
}();