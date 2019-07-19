/*
    A service exposing abstractions to make the system work when there's no internet connection
*/

let OfflineModeService = function (_userId, offlineModeCapabilityEnabled, dataFetchUrl, templatesFetchUrl, servicesFetchUrl, templateEventsHandler) {
    "use strict";

    let offlineModeClient = {
        _isConnectionOn: true,

        _isOfflineModeCapabilityEnabled: offlineModeCapabilityEnabled,

        _connectivityCheckSecondsInterval: 60000,

        _userId: _userId,

        _onlineContainerSelector: $("#online_block"),

        _offlineModePageSelector: $(".offline_page"),

        _connectionNotificationElementId: undefined,

        _onlineModeMenuItemsSelector: undefined,

        _storage: localStorage,

        _isSavedDataSubmissionPaused: false,

        lastOnlineTime: undefined,

        lastOfflineTime: undefined,

        templates: undefined,

        services: undefined,

        save: function (key, data) {
            this._storage.setItem(key, data);
        },

        saveJson: function(key, data) {
            this.save(key, Base64.encode(JSON.stringify(data)));
        },

        retrieve: function (key) {
            return this._storage.getItem(key);
        },

        retrieveJson: function(key) {
            let data = this.retrieve(key);

            if (data === null) {
                return null;
            }
            return JSON.parse(Base64.decode(data));
        },

        remove: function (key) {
            localStorage.removeItem(key);
        },

        removeMany: function(keys) {
            keys.forEach(this.remove);
        },

        isOfflineModeActive: function () {
            let me = this;
            return this._isOfflineModeCapabilityEnabled && (() => {
               me.checkConnectivity();
               return !me._isConnectionOn;
            })();
        },

        checkConnectivity: function () {
            this._isConnectionOn = navigator.onLine;
        },

        periodicallyCheckConnectivity: function() {
            setInterval(() => {
               this.checkConnectivity();
               this.notifyConnectivityStatus();
            }, this._connectivityCheckSecondsInterval);
        },

        notifyConnectivityStatus: function() {

            if (this._isConnectionOn) {
                $(this._onlineModeMenuItemsSelector).show();
                $(this._connectionNotificationElementId).html("You are now online, offline mode switched off");
                this._notificationStatusBadge('alert-info', 'alert-danger');
                $(".offline_page").hide();
                $(".btn_ovc_home_offline").hide();
                this._handleIsOnline();
            } else {
                $(this._onlineModeMenuItemsSelector).hide();
                $(this._connectionNotificationElementId).html("Switching to offline mode, no internet connection");
                this._notificationStatusBadge('alert-danger', 'alert-info');
                this._onlineContainerSelector.hide();
                $(".btn_ovc_home_offline").show();
            }
        },

        _handleIsOnline: function() {
            if (this._isOfflineModeCapabilityEnabled) {
                this._onlineContainerSelector.show();
                this._offlineModePageSelector.hide();
                this.submitData(this._formDataKey(), this._onSubmitFormSuccess(), this._onSubmitFormError());
            }
        },

        _notificationStatusBadge: function(badgeToAdd, badgeToRemove) {
            // only apply the badges if offline capability is enabled
            if (this._isOfflineModeCapabilityEnabled) {
                $(this._connectionNotificationElementId).addClass(badgeToAdd);
                $(this._connectionNotificationElementId).removeClass(badgeToRemove);
            }
        },

        _appendDataToStorage: function(dataKey, data) {
            let existingData = this.retrieveJson(dataKey);

            if (existingData === null) {
                existingData = [data];
            } else {
                existingData.push(data);
            }
            this.saveJson(dataKey, existingData);
        },

        _formDataKey: function () {
            return Base64.encode("form_data_" + this._userId);
        },

        _formDataKeyStaging: function(keySalt) {
            return this._formDataKey() + "_" + keySalt;
        },

        _templatesStorageKey: Base64.encode("ovc_offline_templates"),

        fetchTemplates: function() {
            let _offlineModeClient = window.offlineModeClient;
            let me = this;

            if (me.templates !== undefined) {
                this._injectTemplatesToDom(me.templates);
                console.log("Templates already initialized");
                return;
            }
            let templates = _offlineModeClient.retrieve(me._templatesStorageKey);

            if (templates !== null) {
                me.templates = JSON.parse(Base64.decode(templates));
                this._injectTemplatesToDom(me.templates);
                console.log("Templates loaded from the cache");
                return;
            }

            $.ajax({
                url: templatesFetchUrl,
                type: "GET",
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
                    _offlineModeClient.remove(me._templatesStorageKey);

                },
                success: function (data) {
                    console.log("Successfully initialized templates");
                    me.templates = data.data;
                    _offlineModeClient.save(me._templatesStorageKey, Base64.encode(data.data));
                    me._injectTemplatesToDom(JSON.parse(data.data));
                },
                error: function () {
                    console.log("Error loading templates");
                    me.templates = undefined;
                }
            });
        },

        _injectTemplatesToDom: function(templates) {
            Object.entries(templates).forEach(entry => {
                let tplName = entry[0];
                let tplContent = entry[1];
                $("#" + tplName).html(tplContent);
            });

            templateEventsHandler.handle(Object.keys(templates));
        },

        _servicesStorageKey: Base64.encode("ovc_offline_services"),

        fetchServices: function() {
            let _offlineModeClient = window.offlineModeClient;
            let me = this;

            if (me.services !== undefined) {
                console.log("Services already initialized");
                return;
            }
            let services = _offlineModeClient.retrieve(me._servicesStorageKey);

            if (services !== null) {
                me.services = JSON.parse(Base64.decode(services));
                console.log("Services loaded from the cache");
                return;
            }

            $.ajax({
                url: servicesFetchUrl,
                type: "GET",
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
                    _offlineModeClient.remove(me._servicesStorageKey);

                },
                success: function (data) {
                    console.log("Successfully initialized services");
                    me.services = JSON.parse(Base64.decode(data.data));
                    _offlineModeClient.save(me._servicesStorageKey, data.data);
                },
                error: function () {
                    console.log("Error loading services");
                    me.services = undefined;
                }
            });
        },

        saveFormData: function(data, submissionUrl) {
            let me = this;
            let dataToBeSubmitted = {
                'submissionUrl': submissionUrl,
                'data': {
                    '_userId': me._userId,
                    'payload': data,
                    'savedOn': (new Date()).getTime()
                }
            };
            this._appendDataToStorage(this._formDataKey(), Base64.encode(JSON.stringify(dataToBeSubmitted)));
        },

        _onSubmitFormSuccess: function() {
            return ((submittedData, remainingDataToSubmit) =>  {
                // purge from staging store
                this.remove(this._formDataKeyStaging(submittedData.savedOn));
                // purge from the yet to be submitted store
                if (remainingDataToSubmit === undefined || remainingDataToSubmit.filter(item => item !== undefined).length === 0) {
                    $(this._connectionNotificationElementId).html("You are now online, offline mode switched off. " +
                        "All saved data has been submitted");
                }
            })
        },

        _onSubmitFormError: function() {
            return (response =>  {
                // Todo - a response could have a page / form where the user should be redirected
                console.log(response) ;
                // a user gets re-directed to a page with pre-filled in data. We do not want multiple re-directions in succession
                this._isSavedDataSubmissionPaused = true;
            })
        },

        _purgeFormDataFromStore: function(index, data) {
            // purge from the store
            delete data[index];

            let remainingData = data.filter(item => item !== undefined);

            if (remainingData.length === 0) {
                // no remaining data, delete the key from the store completely
                this.remove(this._formDataKey());
            } else {
                this.saveJson(this._formDataKey(), remainingData);
            }
            return remainingData

        },

        _moveToStagingStore: function(me, keySalt, dataItemToMoveIndex, dataItemToMove, allData) {
            let remainingData = me._purgeFormDataFromStore(dataItemToMoveIndex, allData);
            me.save(me._formDataKeyStaging(keySalt), Base64.encode(JSON.stringify(dataItemToMove)));
            return remainingData;
        },

        submitData: function (dataKey, successHandler, errorHandler) {
            console.log("About to submit saved form data");
            let dataToSubmit = this.retrieveJson(dataKey);

            if (dataToSubmit === null) {
                console.log("No pending data to be submitted");
                return;
            }

            let moveToStagingStore = this._moveToStagingStore;
            let me = this;

            dataToSubmit.filter(item => item !== undefined && !me._isSavedDataSubmissionPaused).forEach((toSubmit, index) => {
                let decodedData = JSON.parse(Base64.decode(toSubmit));
                $.ajax({
                    url: decodedData.submissionUrl,
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(decodedData.data),
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
                        dataToSubmit = moveToStagingStore(me, decodedData.data.savedOn, index, decodedData, dataToSubmit);
                    },
                    success: function (message) {
                        console.log("Saved form data submitted successfully: " + message);
                        dataToSubmit = successHandler(decodedData.data, dataToSubmit);
                    },
                    error: errorHandler
                });
            });
        },

        onLoginEventHandler: function () {
            console.log("Handling on login event handler");
            this._initializeRegistrationData();
            // fetch services first before templates because templates depend on the services data
            this.fetchServices();
            this.fetchTemplates();
        },

        onLogoutEventHandler: function (me) {
            console.log("Logging out and clearing data from cache so that it gets refreshed on the next login");
            me.clearStorage();
        },

        clearStorage: function() {
            // Do not clear any form data saved, just in case it hasn't been submitted yet
            let formKeysToClear = [
                this._registrationDataStorageKey(),
                this._templatesStorageKey,
                this._servicesStorageKey
            ];

            formKeysToClear.forEach(this.remove);
            this.isRegistrationDataInitialized = false;
            this.registrationData = undefined;
            this.templates = undefined;
            this.services = undefined;
        },

        _registrationDataStorageKey: function () {
            return Base64.encode("ovc_data_key");
        },

        isRegistrationDataInitialized: false,

        registrationData: undefined,

        currentSelectedOvc: undefined,

        _initializeRegistrationData: function () {
            let _offlineModeClient = window.offlineModeClient;
            let me = this;

            if (me.registrationData !== undefined) {
                console.log("Registration data already initialized");
                return;
            }

            me.registrationData = _offlineModeClient.retrieveJson(me._registrationDataStorageKey());

            if (me.registrationData !== null) {
                console.log("Registration data loaded from cache");
                return;
            }

            $.ajax({
                url: dataFetchUrl,
                type: "GET",
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
                    _offlineModeClient.remove(me._registrationDataStorageKey());

                },
                success: function (data) {
                    console.log("Successfully initialized registration data");
                    me.isRegistrationDataInitialized = true;
                    me.registrationData = data.data;
                    _offlineModeClient.saveJson(me._registrationDataStorageKey(), data.data);
                },
                error: function () {
                    console.log("Error initializing registration data");
                    me.isRegistrationDataInitialized = false
                }
            });
        },

        toAscii: function(str) {
            let asciiStr = '';
            str.split('').forEach( i => asciiStr = asciiStr + i.charCodeAt(i));
            return asciiStr;
        },

        findOvc: function (ovcName) {
            this._initializeRegistrationData();

            let foundOvcs = [];

            let me = this;

            let ovcNameAsAscii = ovcName.toUpperCase().split(' ').map(me.toAscii);

            Object.entries(this.registrationData).map( entry => {
               let key = entry[0] ;
               let value = entry[1];

               let ovcFound = ovcNameAsAscii
                   .map(it => key.includes(it))
                   .filter(it => it)
                   .length > 0;

               if (ovcFound) {
                   foundOvcs.push(JSON.parse(Base64.decode(value)));
               }
            });

            return foundOvcs;
        },
    };

    return {
        client: function (_connectionNotificationElementId, _onlineModeMenuItemsSelector, _connectivityCheckSecondsInterval) {
            console.log("Initializing offline mode client");
            // Implementing it as a singleton to ensure we have only one instance of it
            if (window.offlineModeClient === undefined) {
                offlineModeClient._connectionNotificationElementId = $("#" + _connectionNotificationElementId);
                offlineModeClient._onlineModeMenuItemsSelector = $("." + _onlineModeMenuItemsSelector);
                offlineModeClient.lastOfflineTime = null;
                offlineModeClient.lastOnlineTime = (new Date()).getTime();
                offlineModeClient._connectivityCheckSecondsInterval = _connectivityCheckSecondsInterval;
                offlineModeClient._userId = _userId;
                offlineModeClient.checkConnectivity();
                offlineModeClient.notifyConnectivityStatus();
                offlineModeClient.periodicallyCheckConnectivity();
                window.offlineModeClient = offlineModeClient;

                // if the user is logged in
                if (offlineModeClient._userId !== "" || offlineModeClient._userId !== null) {
                    offlineModeClient.onLoginEventHandler();
                    $("#logout_button").on("click", function () {
                        offlineModeClient.onLogoutEventHandler(window.offlineModeClient);
                    });
                }
            }

            return window.offlineModeClient;
        },
    };
};

