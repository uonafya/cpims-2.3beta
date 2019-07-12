
let TemplateUtils = (function () {
    return {
        ovcHomePage: $("#ovc_home"),

        viewOvcPage: $("#ovc_view"),

        form1aPage: $("#ovc_form1a"),

        showPage: function (page) {
            $(".offline_page").hide();
            page.show();
        }
    }
})();

// Handle all events on OvcHome template
let OvcHomeTemplate = (function (){
    'use strict';

    return {
        init: function () {
            let me = this;
            console.log("OvcHomeTemplate");
            window.viewOvcOffline = me.viewOvcOffline();
            // submit event
            $("#find_ovc_form_offline").submit(event => {
                let ovcName = $("#search_ovc_offline_name").val();

                console.log("Searching ovc : " + ovcName);
                me._drawOvcSearchResults(window.offlineModeClient.findOvc(ovcName));

                event.preventDefault();
                return false;
            });
        },

        viewOvcOffline: function () {
            let me = this;

            return (id) => {
                console.log("Viewing ovc : " , id);
                Object.entries(window.offlineModeClient.registrationData).some( entry => {
                    let key = entry[0] ;
                    let value = entry[1];

                    if (key === id) {
                        let ovcData = JSON.parse(Base64.decode(value));
                        window.offlineModeClient.currentSelectedOvc = ovcData;

                        me._fillOvcDetailsPage(ovcData);
                        TemplateUtils.showPage(TemplateUtils.viewOvcPage);
                        return true;
                    }
                });
            }
        },

        _fillOvcDetailsPage: function (ovc) {
            let me = this;

            Object.keys(ovc).forEach( key => {
                let ovcDetails = ovc[key];
                if (['facility', 'school'].includes(key)) {
                    // handle hiding particular rows, test this out
                    me._fillOvcDetailsPage(ovcDetails);
                } else if (key === 'household_members') {
                    me._fillOvcHouseholdDetails(ovcDetails);
                } else {
                    $(me._getOvcFieldSelector(key)).html(ovcDetails);
                }
            })
        },

        _getOvcFieldSelector: function(field) {
            return $("#ovc_offline_" + field);
        },

        _fillOvcHouseholdDetails: function (households) {
            $("#offline_ovc_household_table").bootstrapTable('destroy').bootstrapTable({
                'data': households,
                'pagination': true,
                'locale': 'en-Us',
                'columns': [
                    {
                        'field': 'first_name',
                        'title': 'First Name'
                    },
                    {
                        'field': 'surname',
                        'title': "Surname"
                    },
                    {
                        'field': 'age',
                        'title': 'Age'
                    },
                    {
                        'field': 'type',
                        'title': 'Type'
                    },
                    {
                        'field': 'phone_number',
                        'title': 'Telephone'
                    },
                    {
                        'field': 'alive',
                        'title': 'Alive'
                    },
                    {
                        'field': 'hiv_status',
                        'title': 'HIV Status'
                    },
                    {
                        'field': 'household_head',
                        'title': 'Head'
                    }
                ]
            })
        },

        _viewOvcButton: function () {
            return (value, row, index) => {
                return [
                    '<button id="' + value + '" class="view_ovc btb btn-primary" title="View Ovc" onclick="window.viewOvcOffline(\'' + value + '\')">',
                    '<i class="fa fa-eye"></i>',
                    'View Ovc',
                    '</button>'
                ].join('')

            };
        },

        _drawOvcSearchResults: function (ovcs) {
            let me = this;
            let ovcListTable = $("#offline_ovc_table");

            ovcListTable.bootstrapTable('destroy').bootstrapTable({
                'data': ovcs,
                'id-field': 'id',
                'pagination': true,
                'select-item-name': 'id',
                'locale': 'en-US',
                'columns': [
                    {
                        field: 'person_id',
                        title: 'ID'
                    },
                    {
                        field: 'org_unique_id',
                        title: 'CBOID'
                    },
                    {
                        field: 'first_name',
                        title: 'First Name'
                    },
                    {
                        field: 'surname',
                        title: 'Surname'
                    },
                    {
                        field: 'other_names',
                        title: 'Other Names'
                    },
                    {
                        field: 'sex_id',
                        title: 'Sex'
                    },
                    {
                        field: 'date_of_birth',
                        title: 'Date Of Birth'
                    },
                    {
                        field: 'child_chv_full_name',
                        title: 'CHW'
                    },
                    {
                        field: 'date_of_birth',
                        title: 'Date Of Birth'
                    },
                    {
                        field: 'caretake_full_name',
                        title: 'Care Giver'
                    },
                    {
                        field: 'org_unt_name',
                        title: 'LIP/CBO'
                    },
                    {
                        field: 'is_active',
                        title: 'Status'
                    },
                    {
                        field: 'id',
                        title: 'Actions',
                        align: 'center',
                        formatter: me._viewOvcButton()
                    },
                ]
            });
        }
    }
})();

// Handle all events on OvcView template
let OvcViewTemplate = (function (){
    return {
        init: function () {
            console.log("OvcViewTemplate");
            // click event
            $("#ovc_offline_form_1a").click((event) => {
                event.preventDefault();
                TemplateUtils.showPage(TemplateUtils.form1aPage);
                Form1ATemplate.init();
                return false;
            });
        }
    };
})();

// Handle all events on Form1A template
let Form1ATemplate = (function (){
    // todo:
    // ovc_offline_form_1a_names - set names, also age
    // f1a_events_data_table_offline add events
    // #step1 Todo - the steps are duplicating, dedupe and prune them

    let ASSESSMENT = 'ASSESSMENT';
    let EVENT = 'EVENT';
    let PRIORITY = 'PRIORITY';
    let SERVICE = 'SERVICE';

    return {
        init: function () {
            console.log("Form 1A");
            FormWizardValidation.init();
            this._setupMultiSelects();
            this._setupFormEvents();
        },

        _setupFormEvents: function() {
           window.addOfflineOvcService = this._addOfflineOvcService();
           window.saveForm1AOffline = this._saveForm1AOffline();
           window.resetForm1AOffline = this._resetForm1AOffline();
           window.addForm1ARowOffline = this._addForm1ARowOffline();
           window.removeForm1ARowOffline = this._removeForm1ARowOffline();
           window.goToOvcViewFromForm1aOffline = this._goToOvcViewFromForm1aOffline();
        },

        _addOfflineOvcService: function() {
            return (serviceType) => {
                console.log("_addOfflineOvcService", serviceType);
            }
        },

        _saveForm1AOffline: function() {
            return (serviceType) => {
                console.log("_saveForm1AOffline", serviceType);
            }
        },

        _resetForm1AOffline: function() {
            return (serviceType) => {
                console.log("_resetForm1AOffline", serviceType);
            }
        },

        _addForm1ARowOffline: function() {
            return (serviceType) => {
                console.log("_addForm1ARowOffline", serviceType);
            }
        },

        _removeForm1ARowOffline: function() {
            return (serviceType) => {
                console.log("_removeForm1ARowOffline", serviceType);
            }
        },

        _goToOvcViewFromForm1aOffline: function() {
            let me = this;
            return () => {
                console.log("_goToOvcViewFromForm1aOffline");
                if (window.offlineModeClient.currentSelectedOvc) {
                    OvcHomeTemplate._fillOvcDetailsPage(window.offlineModeClient.currentSelectedOvc);
                    TemplateUtils.showPage(TemplateUtils.viewOvcPage);
                    return;
                }

                TemplateUtils.showPage(TemplateUtils.ovcHomePage);
            };
        },

        _setupMultiSelects: function () {
            let me = this;
            let multiSelectInputs = [
                '#olmis_assessment_domain', '#olmis_assessment_coreservice', '#olmis_assessment_coreservice_status', '#olmis_domain',
                '#olmis_service_provider', '#olmis_service', '#olmis_priority_service', '#olmis_priority_domain', '#olmis_priority_health',
                '#olmis_priority_education', '#olmis_priority_shelter', '#olmis_priority_protection', '#olmis_priority_pss', '#olmis_priority_hes',
                '#olmis_critical_event'
            ];

            $(multiSelectInputs.join(','))
                .multiselect({
                    selectAllValue: 'multiselect-all',
                    includeSelectAllOption: true,
                    enableCaseInsensitiveFiltering: true,
                    numberDisplayed: 1,
                    maxHeight: 300,
                    buttonWidth: '100%',
                    buttonClass: 'btn btn-white'
                });

            me._populateServiceFromInputDomain();
            me._setupDateFields();
            me._displayOnInputChanged();
            me._hideOnInputChanged();
        },

        _setupDateFields: function() {
            let dateFields = [
                ["#date_of_assessment", "#date_errormsg0"],
                ["#date_of_cevent", "#date_errormsg1"],
                ['#date_of_priority', '#date_errormsg2'],
                ['#date_of_service', '#date_errormsg3'],
                ['#olmis_service_date', '#olmis_service_date_errormsg']
            ];

            let me = this;

            dateFields.forEach( (dateField) => {
                $(dateField[0]).datepicker({format: 'dd-M-yyyy'});
                $(dateField[0]).datepicker().on('change.dp', function (_) {
                    me._hideElement(dateField[1]);
                });
            });
        },

        _populateServiceFromInputDomain: function() {
            let me = this;
            let errorField = 'errorField';
            let serviceField = 'serviceField';
            let fieldName = 'fieldName';

            let inputDomainElements = {
                '#olmis_assessment_domain': {
                    fieldName: 'olmis_assessment_domain_id',
                    serviceField: '#olmis_assessment_coreservice',
                    errorField: '#olmis_assessment_domain_errormsg',
                    // 'onPopulate': () => $('#olmis_assessment_coreservice').trigger("change")
                    'onPopulate': () => ''
                },
                '#olmis_assessment_coreservice': {
                    fieldName: 'olmis',
                    serviceField: '#olmis_assessment_coreservice_status',
                    errorField: '#olmis_assessment_coreservice_status_errormsg',
                    'onPopulate': () => $('#sel_olmis_assessment_coreservice_status').html('')
                },
                '#olmis_domain': {
                    fieldName: 'olmis_domain_id',
                    serviceField: '#olmis_service',
                    errorField: '#olmis_domain_errormsg',
                    'onPopulate': () =>  $("#sel_olmis_service").html('')
                }
            };

            Object.entries(inputDomainElements).forEach( (entry) => {
                let field = entry[0];
                let fieldHandler = entry[1];

                $(field).change(function (event) {
                    let domain = $(field).val();
                    console.log(domain);
                    me._populateService(fieldHandler[fieldName], domain, fieldHandler[serviceField], fieldHandler[errorField]);
                    let fn = fieldHandler['onPopulate'];
                    fn();
                });
            });
        },

        _populateService: function (fieldName, domain, element, errorElement) {
            console.log(fieldName, domain, element, errorElement);
            let dataToPopulate = [
               {
                   'label': 'Please Select',
                   'value': ''
               }
           ];

           if (window.offlineModeClient.services === undefined) {
               console.log("Services not fetched");
               return;
           }

           let services = window.offlineModeClient.services[fieldName];

           if (services === undefined) {
               services = [];
           }

           let domainServices = services[domain];

           if (domainServices === undefined) {
               domainServices = [];
           }

           domainServices.forEach( (service) => {
               dataToPopulate.push({
                   label: service.item_sub_category,
                   value: service.item_sub_category_id
               });
           });

           $(element).multiselect('destroy');
           $(element).multiselect({
               selectAllValue: 'multiselect-all',
               enableCaseInsensitiveFiltering: true,
               numberDisplayed: 1,
               maxHeight: 300,
               buttonWidth: '100%',
               buttonClass: 'btn btn-white',
               nonSelectedText: 'Please Select'
           });
           $(element).multiselect('dataprovider', dataToPopulate);
           $(element).multiselect('refresh');
           this._hideElement(errorElement);
        },

        _displayOnInputChanged: function () {
            let me = this;
            let fieldsOnChange = {
                '#olmis_service': ['#sel_olmis_service', '#olmis_service_errormsg'],
                '#olmis_priority_health': ['#sel_olmis_priority_health', null],
                '#olmis_priority_shelter': ['#sel_olmis_priority_shelter', null],
                '#olmis_priority_protection': ['#sel_olmis_priority_protection', null],
                '#olmis_priority_pss': ['#sel_olmis_priority_pss', null],
                '#olmis_priority_education': ['#sel_olmis_priority_education', null],
                '#olmis_priority_hes': ['#sel_olmis_priority_hes', null]
            };

            Object.entries(fieldsOnChange).forEach((entry) => {
                let field = entry[0];
                let displayFields = entry[1];

                $(field).change(function (_) {
                    me._hideElement(displayFields[1]);

                    let selections = [];
                    $(field + " option:selected").each(function () {
                        let selectedInput = $(this);

                        if(selectedInput.length) {
                            selections.push(selectedInput.text());
                        }
                    });

                    $(displayFields[0]).html(selections.join(', '));
                });
            });
        },

        _hideOnInputChanged: function () {
            let me = this;
            let fieldsOnChange = {
                '#olmis_service_date': ['#olmis_service_date_errormsg'],
                '#olmis_service_provider': ['#olmis_place_of_service_errormsg'],
                '#olmis_place_of_service': ['#olmis_place_of_service_errormsg']
            };

           Object.entries(fieldsOnChange).forEach((entry) => {
               let field = entry[0];
               let fieldsToHide = entry[1];

               $(field).change(function (_) {
                   fieldsToHide.forEach(me._hideElement);
               });
           });
        },

        _hideElement: function (element) {
            if (element === null) {
                return;
            }

           $(element).css({'display': 'none'});
        }
    };
})();

let TemplatesEventsFactory = function () {
    'use strict';

    console.log('TemplatesEventsFactory');

    let eventsHandlers = {
        'ovc_home': OvcHomeTemplate,
        'ovc_view': OvcViewTemplate,
        'ovc_form1a': Form1ATemplate
    };

    return {
        handle: (templates) => {
            templates.forEach(tpl => {
                if (eventsHandlers[tpl] !== undefined) {
                    eventsHandlers[tpl].init();
                }
            })

        }
    }
};
