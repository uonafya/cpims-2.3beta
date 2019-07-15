
let TemplateUtils = (function () {
    return {
        ovcHomePage: $("#ovc_home"),

        viewOvcPage: $("#ovc_view"),

        form1aPage: $("#ovc_form1a"),

        showPage: function (page) {
            $(".offline_page").hide();
            page.show();
        },
        selectedTextForElement: function (element) {
           let selections = [];
           $("#elem option:selected".replace("elem", element)).each(function () {
             let me = $(this);

             if (me.length) {
                selections.push(me.text())
             }
           });
           return selections;
        },

        saveFormData: function(form_type, data) {
            console.log("Save data form form: " + form_type + " to be submitted later");
            if (window.offlineModeClient.currentSelectedOvc === undefined) {
                console.log("No ovc selected, cannot save user data for form: " + form_type);
                return;
            }
            // Todo - filter out null values
            let dataToSubmit = {
                'person': window.offlineModeClient.currentSelectedOvc.person_id,
                'form_type': 'Form1A',
                'form_data': data
            };
            window.offlineModeClient.saveFormData(dataToSubmit, '/offline_mode/submit/');
            // Todo - add some user feedback to show it's been saved offline
        },

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
    let EVENTS = 'EVENTS';
    let PRIORITY = 'PRIORITY';
    let SERVICE = 'SERVICE';
    let ADD = 'ADD';
    let REMOVE = 'REMOVE';
    let RESET = 'RESET';
    let SAVE = 'SAVE';
    let ADD_ROW = 'ADD_ROW';

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

        assessmentData: [],

        _formEventsFactory: function() {
            let me = this;
            let _resetFormInputs = function(refreshFields, valClearFields, htmlClearFields) {
                refreshFields.forEach((element) => {
                    element.multiselect("clearSelection");
                    element.multiselect('refresh');
                });

                valClearFields.forEach( element => {
                    element.val('');

                });
                htmlClearFields.forEach(element => {
                  element.html('');
                });
            };

            return {
                ASSESSMENT: {
                    ADD: () => {
                        console.log('Adding assessment');
                        let formValues = [
                            [$("#olmis_assessment_domain").val(),$("#olmis_assessment_domain_errormsg")],
                            [$("#olmis_assessment_coreservice").val(), $("#olmis_assessment_coreservice_errormsg")],
                            [$("#olmis_assessment_coreservice_status").val(), $("#olmis_assessment_coreservice_status_errormsg")]
                        ];

                        let formValuesNonEmpty = formValues.map( (entry) => {
                          if (entry[0] === undefined)   {
                              entry[1].css({'display': 'block'});
                          }
                          return entry[0];
                        }).filter(item => item !== undefined);


                        if (formValuesNonEmpty.length !== 3) {
                            console.log("Some form values not filled");
                            return null;
                        }

                        let createInputElement = (id, value) => {
                            return "<input id='element_id' type='hidden'  value='element_value' />"
                                .replace('element_id', id)
                                .replace('element_value', value);
                        };
                        let table = $('#assessment_manager_table')[0];
                        let rowsLength = table.rows.length;
                        let row = table.insertRow(rowsLength);
                        let index = rowsLength - 2;
                        row.id = 'rowid_' + index;
                        let btnRemoveSvcId = 'btnRemoveSvc' + index;

                        let rowCells = [
                            [
                                "td_style",
                                () => "#"
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_assessment_domain").join(", <br/>") +
                                    createInputElement("holmis_assessment_domain", formValuesNonEmpty[0])
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_assessment_coreservice").join(", <br/>") +
                                    createInputElement("holmis_assessment_coreservice", formValuesNonEmpty[1])
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_assessment_coreservice_status").join(", <br/>") +
                                    createInputElement("holmis_assessment_coreservice_status", formValuesNonEmpty[2])
                            ],
                            [
                                'dialog_paragraph',
                                () => "<a id='btn_id' class='btn btn-sm btn-link m-r-5' href='#'>Remove </a>".replace('btn_id', btnRemoveSvcId)
                            ]
                        ];

                        rowCells.forEach( (cell, index) => {
                          let insertedCell = row.insertCell(index);
                          insertedCell.innerHTML = "<h6 class='element_class' >display_value</h6>"
                              .replace("element_class", cell[0])
                              .replace('display_value', cell[1]());
                        });

                        let grabValuesAndRefreshInputs = function () {
                            // Reset form inputs
                            [
                                $("#olmis_assessment_domain"),
                                $("#olmis_assessment_coreservice"),
                                $("#olmis_assessment_coreservice_status")
                            ].forEach((element) => {
                                element.multiselect("clearSelection");
                                element.multiselect('refresh');
                            });


                            // Grab form inputs and store it
                            $("#assessment_manager_table tr").each(function (row, tr) {
                                me.assessmentData[row] = {
                                    'olmis_assessment_domain': $(tr).find('input[id="holmis_assessment_domain"]').val(),
                                    'olmis_assessment_coreservice': $(tr).find('input[id="holmis_assessment_coreservice"]').val(),
                                    'olmis_assessment_coreservice_status': $(tr).find('input[id="holmis_assessment_coreservice_status"]').val()
                                };

                                me.assessmentData.shift();  // remove first row (headers)
                                me.assessmentData.shift();  // remove second row (controls)
                            });

                        };

                        grabValuesAndRefreshInputs();

                        $("#" + btnRemoveSvcId + "").click(function (e) {
                            $("#" + row.id).remove();
                            grabValuesAndRefreshInputs();
                        });

                    },
                    ADD_ROW: () => console.log('Adding assessment row'),
                    REMOVE: () => console.log("Removing assessment"),
                    RESET: () => {
                        console.log("Reset assessment");
                        _resetFormInputs(
                            [
                                $("#olmis_assessment_domain"),
                                $("#olmis_assessment_coreservice"),
                                $("#olmis_assessment_coreservice_status")
                            ], [
                                $("#date_of_assessment"),
                                $("#olmis_assessment_provided_list")

                            ], [
                                $('#sel_olmis_assessment_coreservice_status')
                            ]
                        );
                    },
                    SAVE: () => {
                        console.log("Save assessment");
                        let data = {
                            'date_of_assessment':  $('#date_of_assessment').val(),
                            'assessment': me.assessmentData
                        };
                        TemplateUtils.saveFormData("Form1A", data);
                        me.assessmentData = [];

                        _resetFormInputs(
                            [
                                $("#olmis_assessment_domain"),
                                $("#olmis_assessment_coreservice"),
                                $("#olmis_assessment_coreservice_status")
                            ], [
                                $("#date_of_assessment"),
                                $("#olmis_assessment_provided_list")

                            ], [
                                $('#sel_olmis_assessment_coreservice_status')
                            ]
                        );
                    }
                },
                EVENTS: {
                    ADD: () => console.log('Adding event'),
                    ADD_ROW: () => console.log('Adding event row'),
                    REMOVE: () => console.log("Removing event"),
                    RESET: () => console.log("Reset event"),
                    SAVE: () => console.log("Save event")

                },
                SERVICE: {
                    ADD: () => console.log('Adding service'),
                    ADD_ROW: () => console.log('Adding service row'),
                    REMOVE: () => console.log("Removing service"),
                    RESET: () => console.log("Reset service"),
                    SAVE: () => console.log("Save service")
                }
            }
        },

        _handleEvent: function(eventType, event){
            let eventTypeHandlers = this._formEventsFactory()[eventType];

            if (eventTypeHandlers === undefined) {
                console.log("No event type handler found for event type: ", eventType);
                return null;
            }

            let eventHandler = eventTypeHandlers[event];

            if (eventHandler === undefined) {
                console.log("No event handler found for event type: ", eventType, " and event ", event);
                return null;
            }

            // handle event

            eventHandler();
        },

        _addOfflineOvcService: function() {
            let me = this;
            return (serviceType) => {
                console.log("_addOfflineOvcService", serviceType);
                me._handleEvent(serviceType, ADD);
            }
        },

        _saveForm1AOffline: function() {
            let me = this;
            return (serviceType) => {
                console.log("_saveForm1AOffline", serviceType);
                me._handleEvent(serviceType, SAVE);
            }
        },

        _resetForm1AOffline: function() {
            let me = this;
            return (serviceType) => {
                console.log("_resetForm1AOffline", serviceType);
                me._handleEvent(serviceType, RESET);
            }
        },

        _addForm1ARowOffline: function() {
            let me = this;
            return (serviceType) => {
                console.log("_addForm1ARowOffline", serviceType);
                me._handleEvent(serviceType, ADD_ROW);
            }
        },

        _removeForm1ARowOffline: function() {
            let me = this;
            return (serviceType) => {
                console.log("_removeForm1ARowOffline", serviceType);
                me._handleEvent(serviceType, REMOVE);
            }
        },

        _goToOvcViewFromForm1aOffline: function() {
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
                    me._populateService(fieldHandler[fieldName], domain, fieldHandler[serviceField], fieldHandler[errorField]);
                    let fn = fieldHandler['onPopulate'];
                    fn();
                });
            });
        },

        _populateService: function (fieldName, domain, element, errorElement) {
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
