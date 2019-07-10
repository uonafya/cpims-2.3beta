
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

            return () => {
                // submit event
                $("#find_ovc_form_offline").submit(event => {
                    let ovcName = $("#search_ovc_offline_name").val();

                    console.log("Searching ovc : " + ovcName);
                    me._drawOvcSearchResults(window.offlineModeClient.findOvc(ovcName));

                    event.preventDefault();
                    return false;
                });
            };
        },

        viewOvcOffline: function () {
            let me = this;

            return (id) => {
                console.log("Viewing ovc : " , id);
                Object.entries(window.offlineModeClient.registrationData).some( entry => {
                    let key = entry[0] ;
                    let value = entry[1];

                    if (key === id) {
                        me._fillOvcDetailsPage(JSON.parse(Base64.decode(value)));
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
            let me = this;
            console.log("OvcViewTemplate");
        }
    };
})();

let TemplatesEventsFactory = function () {
    'use strict';

    let eventsHandlers = {
        'ovc_home': OvcHomeTemplate.init(),
        'ovc_view': OvcHomeTemplate.init()
    };

    return {
        handle: (templates) => {
            templates.forEach(tpl => {
                if (eventsHandlers[tpl] !== undefined) {
                    eventsHandlers[tpl]();
                }
            })

        }
    }
};
