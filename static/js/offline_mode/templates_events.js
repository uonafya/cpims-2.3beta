
let TemplateUtils = (function () {
    return {
        ovcHomePage: $("#ovc_home"),

        viewOvcPage: $("#ovc_view"),

        form1aPage: $("#ovc_form1a"),

        form1bPage: $("#ovc_form1b"),

        casePlanTemplate: $("#case_plan_template"),

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
                alert("No ovc selected, cannot save user data for form: " + form_type);
                return;
            }
            let dataToSubmit = {
                'person': window.offlineModeClient.currentSelectedOvc.person_id,
                'form_type': form_type,
                'form_data': data
            };
            window.offlineModeClient.saveFormData(dataToSubmit, '/offline_mode/submit/');
            this.alertDialog('Form saved and will be submitted once the internet is back');
            window.goToOvcViewFromForm1aOffline()
        },

        validateFormValues: function (formValues) {
            let formValuesNonEmpty = formValues.map( (entry) => {
                if (entry[0] === undefined)   {
                    entry[1].css({'display': 'block'});
                }
                return entry[0];
            }).filter(item => item !== undefined);

            if (formValuesNonEmpty.length !== formValues.length) {
                console.log("Some form values not filled");
                return null;
            }

            return formValuesNonEmpty;
        },

        createInputElement: function(id, value) {
            return "<input id='element_id' type='hidden'  value='element_value' />"
                .replace('element_id', id)
                .replace('element_value', value);
        },

        createTable: function (tableElement, rowCells, afterRowRemovedHandler) {
           let table = tableElement[0];
            let rowsLength = table.rows.length;
            let row = table.insertRow(rowsLength);
            let index = rowsLength - 2;
            row.id = 'rowid_' + index;
            let btnRemoveSvcId = 'btnRemoveSvc' + index;

            // Append the add button
            rowCells.push([
                'dialog_paragraph',
                    () => "<a id='btn_id' class='btn btn-sm btn-link m-r-5' href='#'>Remove </a>".replace('btn_id', btnRemoveSvcId)
                ]
            );

            rowCells.forEach( (cell, index) => {
                let insertedCell = row.insertCell(index);
                insertedCell.innerHTML = "<h6 class='element_class' >display_value</h6>"
                    .replace("element_class", cell[0])
                    .replace('display_value', cell[1]());
            });

            $("#" + btnRemoveSvcId + "").click(function (e) {
                $("#" + row.id).remove();
                afterRowRemovedHandler();
            });
        },

        alertDialog: function (alertMessage) {
            $('#csi-warning-dialog-offline').modal('show');
            $('#span_csi_alert-offline').html(alertMessage);
        },

        initFormWizard: function (wizardId, wizardStepsCount) {
            // Only initialize a form wizard if none exists
            try {
                $("#" + wizardId).bwizard('count');
                console.log("Wizard : ", wizardId , " already initialized");
            } catch (e) {
                console.log("Initializing wizard: ", wizardId);

                $("#" + wizardId).bwizard({validating: function (e, ui) {
                    for(let i = 0; i < wizardStepsCount; i++) {
                        if (ui.index === i) {
                            $(".alert").hide();
                        }
                    }
                }});
            }
        },

        formatDateFields: function (fields) {
            fields.forEach(field => {
                field.attr('data-parsley-required', 'true');
                field.datepicker({format: 'dd-M-yyyy'});
            });
        },
        randomNumber: function () {
            let min=101;
            let max=1999;
            let random = Math.random() * (+max - +min) + +min;
            random = random.toFixed(0);
            return random;
        },
        selectElement: function (parentDiv, elements) {
            return $(elements.split(",")
                .map( element => parentDiv + ' ' + element)
                .join(", "));
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
                        Form1BTemplate.setOvc(ovcData);
                        CasePlanTemplate.setOvc(ovcData);
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
            let formEventHandlers = {
                '#ovc_offline_form_1a': [Form1ATemplate, TemplateUtils.form1aPage],
                '#ovc_offline_form_1b': [Form1BTemplate, TemplateUtils.form1bPage],
                '#ovc_offline_form_case_plan_template': [CasePlanTemplate, TemplateUtils.casePlanTemplate]
            };

            Object.entries(formEventHandlers).forEach(entry => {
                $(entry[0]).click(event => {
                    event.preventDefault();
                    TemplateUtils.showPage(entry[1][1]);
                    console.log("Showing form1a for selected ovc");
                    entry[1][0].init();
                    return false;
                });
            });
        }
    };
})();

// Handle all events on Form1A template
let Form1ATemplate = (function (){
    // Todo: Fix the case where the user is already on the form1a template, and the dom already loaded, injecting it messes things up, maybe clear the dom first

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
            TemplateUtils.initFormWizard("wizard-f1a-offline", 4);
            this._setupMultiSelects();
            this._setupFormEvents();
        },

        _setupFormEvents: function() {
            console.log("Setting form 1 events");
            window.addOfflineOvcService = this._addOfflineOvcService();
            window.saveForm1AOffline = this._saveForm1AOffline();
            window.resetForm1AOffline = this._resetForm1AOffline();
            window.addForm1ARowOffline = this._addForm1ARowOffline();
            window.removeForm1ARowOffline = this._removeForm1ARowOffline();
            window.goToOvcViewFromForm1aOffline = this._goToOvcViewFromForm1aOffline();
            this._setupPriorityFormEvents();
            this._setupDomainLog();
        },

        _setupPriorityFormEvents: function() {

            $('#date_of_priority').datepicker().on('change.dp', function(e) {
                let priorityDate = $("#date_of_priority").datepicker("getDate");
                let nextMonth = priorityDate.getMonth() + 1;

                if ([1, 5, 11].includes(nextMonth)) {
                    $('#div-priority-need0').css({'display': 'none'});
                    $('#div-priority-need1').css({'display': 'block'});
                    $('#div-priority-need1-controls').css({'display': 'block'});
                } else {
                    $('#div-priority-need0').css({'display': 'block'});
                    $('#div-priority-need1').css({'display': 'none'});
                    $('#div-priority-need1-controls').css({'display': 'none'});
                }
            });
        },

        assessmentData: [],
        priorityData: [],
        servicesData: [],

        _domainLog: {},

        _setupDomainLog: function() {
            let domains = ['DSHC', 'DPSS', 'DPRO', 'DHES', 'DHNU', 'DEDU'];
            let me = this;
            domains.forEach( domain => {
                me._domainLog[domain] = []
            });
        },

        _formEventsFactory: function() {
            let me = this;
            let _resetFormInputs = function(tableElement, refreshFields, valClearFields, htmlClearFields) {
                refreshFields.forEach((element) => {
                    element.multiselect("clearSelection");
                    element.multiselect('refresh');
                });

                valClearFields.forEach((element) => {
                    element.val('');

                });
                htmlClearFields.forEach((element) => {
                  element.html('');
                });

                if (tableElement !== null) {
                    tableElement.find("tr:gt(1)").remove();
                }
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

                        let formValuesNonEmpty = TemplateUtils.validateFormValues(formValues);

                        if (formValuesNonEmpty === null) {
                            return;
                        }

                        let rowCells = [
                            [
                                "td_style",
                                () => "#"
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_assessment_domain").join(", <br/>") +
                                    TemplateUtils.createInputElement("holmis_assessment_domain", formValuesNonEmpty[0])
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_assessment_coreservice").join(", <br/>") +
                                    TemplateUtils.createInputElement("holmis_assessment_coreservice", formValuesNonEmpty[1])
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_assessment_coreservice_status").join(", <br/>") +
                                    TemplateUtils.createInputElement("holmis_assessment_coreservice_status", formValuesNonEmpty[2])
                            ]
                        ];

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


                            // Grab form inputs and store them
                            $("#assessment_manager_table tr").each(function (row, tr) {
                                me.assessmentData[row] = {
                                    'olmis_assessment_domain': $(tr).find('input[id="holmis_assessment_domain"]').val(),
                                    'olmis_assessment_coreservice': $(tr).find('input[id="holmis_assessment_coreservice"]').val(),
                                    'olmis_assessment_coreservice_status': $(tr).find('input[id="holmis_assessment_coreservice_status"]').val()
                                };
                            });

                            me.assessmentData.shift();  // remove first row (headers)
                            me.assessmentData.shift();  // remove second row (controls)
                        };

                        TemplateUtils.createTable($('#assessment_manager_table'), rowCells, grabValuesAndRefreshInputs);

                        grabValuesAndRefreshInputs();
                    },
                    ADD_ROW: () => console.log('Adding assessment row'),
                    REMOVE: () => console.log("Removing assessment"),
                    RESET: () => {
                        console.log("Reset assessment");
                        _resetFormInputs(
                            $('#assessment_manager_table'),
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
                        let dateOfAssessment = $('#date_of_assessment').val();

                        if (!dateOfAssessment) {
                            TemplateUtils.alertDialog("Date of assessment must be filled in");
                            return;
                        }

                        let data = {
                            'assessment': {
                                'assessments': me.assessmentData,
                                'date_of_assessment': dateOfAssessment
                            }
                        };
                        TemplateUtils.saveFormData("Form1A", data);

                        _resetFormInputs(
                            $('#assessment_manager_table'),
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

                        me.assessmentData = [];
                    }
                },
                EVENTS: {
                    ADD: () => console.log('Adding event'),
                    ADD_ROW: () => console.log('Adding event row'),
                    REMOVE: () => console.log("Removing event"),
                    RESET: () => {
                        console.log("Reset event");
                        _resetFormInputs(
                            null,
                            [$("#olmis_critical_event")],
                            [$('#date_of_cevent')],
                            [$("#sel_olmis_critical_event")]);
                    },
                    SAVE: () => {
                        console.log("Save event");
                        let criticalEventDate = $('#date_of_cevent').val();
                        let criticalEvent = $('#olmis_critical_event').val();

                        if (!criticalEvent || criticalEvent === '') {
                            alert ('Please select one or more critical events');
                            return;
                        }


                        if(!criticalEventDate) {
                            alert ("Date critical event recorded must tbe filled in");
                            return;
                        }

                        let data = {
                            'event': {
                                'date_of_event': criticalEventDate,
                                'olmis_critical_event': criticalEvent.toString()
                            }
                        };
                        TemplateUtils.saveFormData("Form1A", data);
                        _resetFormInputs(
                            null,
                            [$("#olmis_critical_event")],
                            [$('#date_of_cevent')],
                            [$("#sel_olmis_critical_event")]);
                    }

                },
                PRIORITY: {
                    ADD: () => console.log('Adding priority'),
                    ADD_ROW: () => {
                        console.log('Adding priority row');

                        let formValues = [
                            [$("#olmis_priority_domain").val(),$("#olmis_priority_domain_errormsg")],
                            [$("#olmis_priority_service").val(), $("#olmis_priority_service_errormsg")],
                        ];
                        let formValuesNonEmpty = TemplateUtils.validateFormValues(formValues);

                        if (formValuesNonEmpty === null) {
                            $('#span_csi_alert').html("Some values haven't been filled");
                            return;
                        }

                        let totalServicesForDomains = Object
                            .values(me._domainLog)
                            .reduce( (total, nextValue) => total + nextValue.length, 0);

                        console.log("totalServicesForDomains: ", totalServicesForDomains);

                        if (totalServicesForDomains >= 3) {
                            TemplateUtils.alertDialog("You are violating CSI Priority assessment Rules which demands 3 a maximum of priorities from either domain.");
                            return false;
                        }

                        let olmisPriorityDomain = formValuesNonEmpty[0];
                        let olmisPriorityService = formValuesNonEmpty[1];

                        olmisPriorityService.forEach( service => {
                          let domainLog = me._domainLog[olmisPriorityDomain];
                          if (domainLog.includes(service)) {
                              TemplateUtils.alertDialog('One or more of the priority need you have selected have been captured.');
                              return;
                          }

                          if (domainLog.length < 3) {
                              me._domainLog[olmisPriorityDomain].push(service);
                          }
                        });

                        let rowCells = [
                            [
                                "td_style",
                                () => "#"
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_priority_domain").join(", <br/>") +
                                    TemplateUtils.createInputElement("holmis_priority_domain", formValuesNonEmpty[0])
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_priority_service").join(", <br/>") +
                                    TemplateUtils.createInputElement("holmis_priority_service", formValuesNonEmpty[1])
                            ],
                        ];

                        let grabValuesAndRefreshInputs = function () {
                            // Reset inputs
                            [$("#olmis_priority_domain"), $("#olmis_priority_service")].forEach(element => {
                                element.multiselect("clearSelection");
                                element.multiselect('refresh');
                            });

                            // Grab form inputs and store them
                            $('#priority_manager_table tr').each(function (row, tr) {
                                me.priorityData[row] = {
                                    "olmis_priority_domain": $(tr).find('input[id="holmis_priority_domain"]').val(),
                                    "olmis_priority_service": $(tr).find('input[id="holmis_priority_service"]').val()
                                }

                            });

                            me.priorityData.shift();  // remove first row (headers)
                            me.priorityData.shift();  // remove second row (controls)
                        };

                        TemplateUtils.createTable($('#priority_manager_table'), rowCells, grabValuesAndRefreshInputs);

                        grabValuesAndRefreshInputs();
                    },
                    REMOVE: () => console.log("Removing priority"),
                    RESET: () => {
                        console.log("Reset priority");

                        _resetFormInputs(
                            $('#priority_manager_table'),
                            [
                                $("#olmis_priority_domain"),
                                $("#olmis_priority_service")
                            ], [
                                $("#date_of_priority"),
                                $("#olmis_priority_service_provided_list")

                            ], [
                                $('#sel_olmis_priority_service')
                            ]
                        );
                    },
                    SAVE: () => {
                        console.log("Save priority")
                        let dateOfPriority = $('#date_of_priority').val();

                        if (!dateOfPriority) {
                            TemplateUtils.alertDialog("Date of priority must be filled in");
                            return;
                        }

                        let data = {
                            'priority': {
                                'priorities': me.priorityData,
                                'date_of_priority': dateOfPriority
                            }
                        };

                        TemplateUtils.saveFormData("Form1A", data);
                        _resetFormInputs(
                            $('#priority_manager_table'),
                            [
                                $("#olmis_priority_domain"),
                                $("#olmis_priority_service")
                            ], [
                                $("#date_of_priority"),
                                $("#olmis_priority_service_provided_list")

                            ], [
                                $('#sel_olmis_priority_service')
                            ]
                        );

                        me.priorityData = [];
                    }
                },
                SERVICE: {
                    ADD: () => console.log('Adding service'),
                    ADD_ROW: () => {
                        console.log('Adding service row')
                        let formValues = [
                            [$("#olmis_domain").val(),$("#olmis_domain_errormsg")],
                            [$("#olmis_service").val(), $("#olmis_service_errormsg")],
                            [$("#olmis_service_date").val(), $("#olmis_service_date_errormsg")],
                        ];


                        let formValuesNonEmpty = TemplateUtils.validateFormValues(formValues);

                        if (formValuesNonEmpty === null) {
                            $('#span_csi_alert').html("Some values haven't been filled");
                            return;
                        }

                        let rowCells = [
                            [
                                "td_style",
                                () => "#"
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_domain").join(", <br/>") +
                                    TemplateUtils.createInputElement("holmis_domain", formValuesNonEmpty[0])
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_service").join(", <br/>") +
                                    TemplateUtils.createInputElement("holmis_service", formValuesNonEmpty[1])
                            ],
                            [
                                "td_style",
                                () => TemplateUtils.selectedTextForElement("olmis_service_date").join(", <br/>") +
                                    TemplateUtils.createInputElement("holmis_service_date", formValuesNonEmpty[2])
                            ]
                        ];
                        let grabValuesAndRefreshInputs = function () {
                            // Reset form inputs
                            [
                                $("#olmis_domain"),
                                $("#olmis_service")
                            ].forEach((element) => {
                                element.multiselect("clearSelection");
                                element.multiselect('refresh');
                            });

                            $('#olmis_service_date').val('');
                            $("#sel_olmis_service").html('');

                            // Grab form inputs and store them
                            $("#services_manager_table tr").each(function (row, tr) {
                                me.servicesData[row] = {
                                    'olmis_domain': $(tr).find('input[id="holmis_domain"]').val(),
                                    'olmis_service': $(tr).find('input[id="holmis_service"]').val(),
                                    'olmis_service_date': $(tr).find('input[id="holmis_service_date"]').val()
                                };
                            });

                            me.servicesData.shift();  // remove first row (headers)
                            me.servicesData.shift();  // remove second row (controls)
                        };

                        TemplateUtils.createTable($('#services_manager_table'), rowCells, grabValuesAndRefreshInputs);

                        grabValuesAndRefreshInputs();
                    },
                    REMOVE: () => console.log("Removing service"),
                    RESET: () => {
                        console.log("Reset service");
                        _resetFormInputs(
                            $('#services_manager_table'),
                            [
                                $("#olmis_domain"),
                                $("#olmis_service")
                            ], [
                                $("#olmis_service_date"),
                                $("#date_of_service")
                            ], [
                                $('#sel_olmis_service')
                            ]
                        );
                    },
                    SAVE: () => {
                        console.log("Save service");
                        let dateOfService = $('#date_of_service').val();

                        if (!dateOfService) {
                            TemplateUtils.alertDialog("Date of service must be filled in");
                            return;
                        }

                        let data = {
                            'service': {
                                'services': me.servicesData,
                                'date_of_service': dateOfService
                            }
                        };
                        TemplateUtils.saveFormData("Form1A", data);

                        _resetFormInputs(
                            $('#services_manager_table'),
                            [
                                $("#olmis_domain"),
                                $("#olmis_service")
                            ], [
                                $("#olmis_service_date"),
                                $("#date_of_service")
                            ], [
                                $('#sel_olmis_service')
                            ]
                        );

                        me.servicesData = [];
                    }
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
            console.log("Setting up date fields");
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
                },
                '#olmis_priority_domain': {
                    fieldName: 'olmis_domain_id',
                    serviceField: '#olmis_priority_service',
                    errorField: '#olmis_priority_domain_errormsg',
                    'onPopulate': () =>  $("#sel_olmis_priority_service").html('')
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


// Handle all events on Form1B template
let Form1BTemplate = (function () {

    let ovc = undefined;

    return {
        init: function () {
            console.log("Form 1B");
            TemplateUtils.initFormWizard("wizard-f1b-offline", 6);
            TemplateUtils.formatDateFields([$("#olmis_service_date_form1b_offline")]);
            this._setupOnSubmitEvent();
        },

        setOvc: function (selectedOvc) {
            console.log("Setting ovc data on Form1B");
            this.ovc = selectedOvc;

            if(this.ovc === undefined) {
                return;
            }
            $("#offline_form1b_chv_child_chv_full_name").html(this.ovc.child_chv_full_name);
            $("#form_1b_offline_kyc").html([this.ovc.child_chv_full_name, this.ovc.sex_id, this.ovc.age].join(" | "));
            $("#caretaker_id_form1b_offline").val(this.ovc.caretaker_id);
            $("#person_id_form1b_offline").val(this.ovc.chv_id);
        },

        _setupOnSubmitEvent: function () {
            let form1B = $("#new_form1b_offline");
            let me = this;

            $("#submit_form1b_offline").on("click", function (event) {
                console.log("Form 1b submit clicked");
                event.preventDefault();
                event.stopImmediatePropagation();
                if (me.isFormValid(form1B)) {
                    me._submitForm(form1B)
                } else {
                    console.log("Form1b has errors");
                    let errorBox = $("#messages_form1b_offline");
                    errorBox.show();
                    errorBox.html('Make sure the month is correct and there is data.');
                    errorBox.attr("tabindex",-1).focus();
                }
            });
        },

        isFormValid:  function (form) {
            form.parsley().validate();
            let isDateValid = () => {
                let date = $('#olmis_service_date_form1b_offline').datepicker('getDate');
                let month = date.getMonth() + 1;
                return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ].includes(month);
            };

            return (form.parsley().isValid() && isDateValid())
        },

        _submitForm: function (form) {
            let data = form.serializeArray();
            console.log("About to submit form1B");
            let toSubmit = {
                'caretaker_id': null,
                'person_id': null,
                'services': [],
                'olmis_service_date':  undefined
            };
            data.forEach( item => {
                if (item.name === "caretaker_id_form1b_offline") {
                    toSubmit['caretaker_id'] = item.value;
                }

                if (item.name === "person_id_form1b_offline") {
                    toSubmit['person_id'] = item.value;
                }

                if (item.name === "f1b[]") {
                    toSubmit['services'].push(item.value);
                }

                if (item.name === "olmis_service_date_form1b_offline") {
                    toSubmit['olmis_service_date'] = item.value;
                }
            });

            TemplateUtils.saveFormData("Form1B", toSubmit);
            form.trigger("reset");
        }
    }
})();

// Handle all events on CasePlanTemplate template
let CasePlanTemplate = (function () {

    let ovc = undefined;

    let getFormInput = () => {
        return {
            'domain': [],
            'goal': [],
            'gaps': [],
            'actions': [],
            'services': [],
            'responsible': [],
            'date': [],
            'actual_completion_date': [],
            'results': [],
            'reasons': [],
            'if_first_cpara': [],
            'date_first_cpara': [],
            'cpt_date_caseplan': []
        };
    };

    let selectElement = (elements) => {
        return TemplateUtils.selectElement('#case_plan_template ', elements);
    };

    let formInput = getFormInput();

    let deletedIndexes = [];

    return {
        init: function () {
            console.log("CasePlanTemplate");
            this._setupFormInputs();
            this._setupEvents();
        },

        setOvc: function (selectedOvc) {
            console.log("Setting ovc data on CasePlanTemplate");
            ovc = selectedOvc;
        },

        _setupFormInputs: function () {
            let dateFirstCpara = selectElement('input[name=date_first_cpara_offline]');
            selectElement('input[name=if_first_cpara_offline], input[name=date_first_cpara_offline]').removeAttr('required');
            dateFirstCpara.attr('disabled', true);

            selectElement('input[name=if_first_cpara_offline]').change(function(){
                let value = $(this).val();
                if(value === 'AYES') {
                    dateFirstCpara.val('');
                    dateFirstCpara.attr('disabled', true);
                } else if(value === 'ANNO'){
                    dateFirstCpara.val('');
                    dateFirstCpara.removeAttr('disabled');
                }
            });

            selectElement('.services_cell_offline > div > select').multiselect({
                selectAllValue: 'multiselect-all',
                includeSelectAllOption: true,
                enableCaseInsensitiveFiltering: true,
                numberDisplayed: 1,
                maxHeight: 300,
                buttonWidth: '100%',
                buttonClass: 'btn btn-white'
            });

            selectElement('#wizard-case-plan-offline > input, #wizard-case-plan-offline > select').attr('required', true);

            let selectElements = selectElement('.goals_cell_offline > div > select').children();
            if (selectElements.length > 0 && selectElements[0].text !== 'Pick an item') {
                selectElement('.goals_cell_offline > div > select, .gaps_cell_offline > div > select, .actions_cell_offline > div > select, .domain_cell_offline > select').prepend('<option value="" disabled selected>Pick an item</option>');
            }

            [
                selectElement('#CPT_DATE'),
                selectElement('#CPT_ACTUAL_DATE_COMPLETION'),
                selectElement('input[name=cpt_date_caseplan_offline]'),
                selectElement('input[name=date_first_cpara_offline_offline]')
            ].forEach(element => element.datepicker({ format: 'yyyy-mm-dd' }));

            let domainElementsMap = {
                'DEDU': 'school_form',
                'DHES': 'stable_form',
                'DPRO': 'safe_form',
                'DHNU': 'healthy_form'
            };

            let domainElements = Object.values(domainElementsMap);

            // onDomain change
            selectElement('select[name=CPT_DOMAIN]').change(function (e) {
                let selectedDomain = selectElement('select[name=CPT_DOMAIN] option:selected').val();
                let domainInput = domainElementsMap[selectedDomain];
                if (domainInput === undefined) {
                    return;
                }
                let createOfflineInput = (input) => $('.' + input + '_offline' );

                createOfflineInput(domainInput).removeClass('hidden');

                domainElements
                    .filter(element => element !== domainInput)
                    .forEach(element => {
                        createOfflineInput(element).addClass('hidden');
                    });
            });

            selectElement('input[name="cpt_date_caseplan_offline"]').click(function (e) {
                selectElement('#wizard-case-plan-offline > input, #wizard-case-plan-offline > select, #wizard-case-plan-offline > .multiselect.dropdown-toggle.btn.btn-white').css({'border-color':'#ccd0d4'});
            });
        },

        _setupEvents: function() {
            let me = this;
            let eventsHandlers = {
                '#cancel_case_plan_template_offline': this._cancel,
                '#case_plan_template_offline_add_row': this._addRow,
                '#submit_case_plan_template_offline': this._submit
            };

            Object.entries(eventsHandlers).forEach(entry => {
                let element = entry[0];
                let eventHandler = entry[1];

                selectElement(element).on("click", function (event) {
                    event.preventDefault();
                    event.stopImmediatePropagation();
                    eventHandler(me);
                });
          })
        },

        _addRow: function (me) {
            console.log("Add Row CasePlan Template offline");
            let domain = selectElement('#id_CPT_DOMAIN option:selected').val();

            let getSelectedValues = (input) => selectElement('.' + input + "_offline > div:not(.hidden) > select > option:selected").val();

            let goals = getSelectedValues('goals_cell');
            let gaps = getSelectedValues('gaps_cell');
            let actions = getSelectedValues('actions_cell');
            let services = [];
            selectElement('.services_cell_offline > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active input[type=checkbox]').each(function () {
                let value = $(this).val();
                if(value !== 'multiselect-all'){
                    services.push(value);
                }
            });

            if (services.length < 1) {
                services = null;
            }

            let responsible = selectElement('#id_CPT_RESPONSIBLE option:selected').val();
            let date = selectElement('#CPT_DATE').val();
            let actual_completion_date = selectElement('#CPT_ACTUAL_DATE_COMPLETION').val();
            let if_first_cpara = selectElement('input[name=if_first_cpara_offline]:checked').val();
            let date_first_cpara = selectElement('input[name=date_first_cpara_offline]').val();
            let cpt_date_caseplan_offline = selectElement('input[name=cpt_date_caseplan_offline]').val();
            let results = selectElement('#id_CPT_RESULTS').val();
            let reasons = selectElement('#id_CPT_REASONS').val();

            $('.waleert').remove();

            selectElement('#wizard-case-plan-offline > input, #wizard-case-plan-offline > select').change(function (e) {
                $(this).addClass('d-c-1')
            });

            selectElement('#wizard-case-plan-offline > input, #wizard-case-plan-offline > select').focus(function (e) {
                selectElement('#wizard-case-plan-offline > input, #wizard-case-plan-offline > select, #wizard-case-plan-offline > .multiselect.dropdown-toggle.btn.btn-white').css('border', '1px solid #9fa2a5');
                $('.waleert').remove();
            });

            let createContainerElement = (strWithHTML) => {
                let container = document.createElement('div');
                let text = document.createTextNode(strWithHTML);
                container.appendChild(text);
                return container.innerHTML;
            };

            let servicesDisplay = [];

            selectElement('.services_cell_offline > div:not(.hidden) > div.btn-group > ul.multiselect-container > li.active label[class=checkbox]').each(function () {
                let text = createContainerElement($(this).text());
                if(text !== 'Select all') {
                    servicesDisplay.push('<li>'+ text +'</li>')
                }
            });

            let inputValues = {
                'domain': [domain, selectElement('select[name=CPT_DOMAIN] option[value='+domain+']').text()],
                'goals': [goals, selectElement('.goals_cell_offline> div:not(.hidden) > select option:selected').text()],
                'gaps': [gaps, selectElement('.gaps_cell_offline > div:not(.hidden) > select option:selected').text()],
                'actions': [actions, selectElement('.actions_cell_offline > div:not(.hidden) > select option[value=' + actions + ']').text()],
                'services': [services, servicesDisplay],
                'responsible': [responsible,  selectElement('select[name=CPT_RESPONSIBLE] option[value=' + responsible + ']').text()],
                'date': [date, date],
                'actual_completion_date': [actual_completion_date, actual_completion_date],
                'results': [results, selectElement('select[name=CPT_RESULTS] option[value='+results+']').text()],
                'reasons': [reasons, reasons]
            };

            let notToShowOnGrid = ['date', 'date_first_cpara', 'cpt_date_caseplan_offline'];

            let validInputs = Object.values(inputValues)
                .filter(inputValue => inputValue[0] !== null && inputValue[0] !== '');

            if (Object.values(inputValues).length !== validInputs.length) {
               selectElement('input:not(.d-c-1), select:not(.d-c-1), .multiselect.dropdown-toggle.btn.btn-white').not('a[tabindex] label.checkbox input[type=checkbox]').css('border', '1px solid red');
               selectElement('input:not(.d-c-1), select:not(.d-c-1)').not('a[tabindex] label.checkbox input[type=checkbox]').before("<small id='CPT_DATE_CASEPLAN_state_offline' class='waleert' style='color: red'>This field is required</small>");
               return;
            }
            selectElement('input:not(.d-c-1), select:not(.d-c-1), .multiselect.dropdown-toggle.btn.btn-white').not('a[tabindex] label.checkbox input[type=checkbox]').css('border', '1px solid #ccd0d4');

            formInput.domain.push(domain);
            formInput.goal.push(goals);
            formInput.gaps.push(gaps);
            formInput.actions.push(actions);
            formInput.services.push(services);
            formInput.responsible.push(responsible);
            formInput.date.push(date);
            formInput.actual_completion_date.push(actual_completion_date);
            formInput.if_first_cpara.push(if_first_cpara);
            formInput.date_first_cpara.push(date_first_cpara);
            formInput.results.push(results);
            formInput.reasons.push(reasons);
            formInput.cpt_date_caseplan.push(cpt_date_caseplan_offline);

            let tableCells = Object
                .entries(inputValues)
                .filter(entry => !notToShowOnGrid.includes(entry[0]))
                .map(entry => {
                    let entryKey = entry[0];
                    let entryDisplayValue = entry[1][1];
                    let value = entryDisplayValue;

                    if (entryKey === 'services') {
                        entryDisplayValue.forEach(item => {
                            if (item !== '' || item === null) {
                                value += "<li>" + item + "</li>";
                            }
                        });
                    }

                    return "<td id='tbl_offline_{td_id}'><ul class='ui-flow'>{display_value}</ul></td>"
                        .replace('{td_id}', entryKey)
                        .replace('{display_value}', value);
                });

            let rowId = TemplateUtils.randomNumber();
            let currentIndex = formInput.domain.length - 1;
            let rowElementId = 'row_offline_' + rowId + "_" + currentIndex;
            let btnId = 'remove_row_caseplan_offline_' + rowElementId;

            tableCells.push('<td><a href="#" id="{btn_id}" class="btn btn-xs btn-danger"><i class="fa fa-trash"></i> Remove</a></td>'.replace('{btn_id}', btnId));
            let tableRow = '<tr id = {row_id} >'.replace('{row_id}', rowElementId) + tableCells.join(" ") + '</tr>';

            selectElement("#submissions_table_offline tbody").append(tableRow);

            selectElement("#" + btnId).click(function (event) {
                event.preventDefault();
                $("#" + rowElementId).empty();
                $("#" + rowElementId).remove();

                deletedIndexes.push(currentIndex);
            });

            selectElement("#case_plan_offline_form").trigger("reset");
        },

        _submit: function (me) {
            console.log('Submit case plan template offline');
            let formInputMinusDeleted = {};

            if (deletedIndexes.length > 0)  {
                Object.entries(formInput).forEach(entry => {
                    let inputValues = entry[1];
                    formInputMinusDeleted[entry[0]] = [];

                    inputValues.forEach((value, index) => {
                        if (!deletedIndexes.includes(index)) {
                            formInputMinusDeleted[entry[0]].push(value);
                        }
                    });
                })
            } else {
                formInputMinusDeleted = formInput;
            }

            TemplateUtils.saveFormData("CasePlanTemplate", formInputMinusDeleted);
            me._cancel();
        },

        _cancel: function (me) {
            console.log("Cancelling case plan template offline");
            selectElement("#case_plan_offline_form").trigger("reset");
            selectElement("#submissions_table_offline tbody").html("");
            formInput = getFormInput();
            deletedIndexes = [];
        }
    }
})();

let TemplatesEventsFactory = function () {
    'use strict';

    console.log('TemplatesEventsFactory');

    let eventsHandlers = {
        'ovc_home': OvcHomeTemplate,
        'ovc_view': OvcViewTemplate,
        'ovc_form1a': Form1ATemplate,
        'ovc_form1b': Form1BTemplate,
        'case_plan_template': CasePlanTemplate
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
