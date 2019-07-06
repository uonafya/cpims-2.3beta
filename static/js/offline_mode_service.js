/*
    A service exposing an abstractions to make the system work when there's no internet connection
*/

let OfflineModeService = function (userId, offlineModeCapabilityEnabled) {
    "use strict";

    let offlineModeClient = {
        isConnectionOn: true,

        isOfflineModeCapabilityEnabled: offlineModeCapabilityEnabled,

        connectivityCheckSecondsInterval: 60000,

        userId: userId,

        connectionNotificationElementId: undefined,

        onlineModeMenuItemsSelector: undefined,

        lastOnlineTime: undefined,

        lastOfflineTime: undefined,

        storage: localStorage,

        save: function (key, data) {
            this.storage.setItem(key, data);
        },

        saveJson: function(key, data) {
            this.save(key, Base64.encode(JSON.stringify(data)));
        },

        retrieve: function (key) {
            return this.storage.getItem(key);
        },

        retrieveJson: function(key) {
            let data = this.retrieve(key);

            if (data === null) {
                console.log("No data found in storage with key: " + key);
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

        checkConnectivity: function () {
            this.isConnectionOn = navigator.onLine;
        },

        periodicallyCheckConnectivity: function() {
            setInterval(() => {
               this.checkConnectivity();
               this.notifyConnectivityStatus();
            }, this.connectivityCheckSecondsInterval);
        },

        notifyConnectivityStatus: function() {

            if (this.isConnectionOn) {
                $(this.onlineModeMenuItemsSelector).show();
                $(this.connectionNotificationElementId).html("You are now online, offline mode switched off");
                this._notificationStatusBadge('alert-info', 'alert-danger');
                this._handleIsOnline();
            } else {
                $(this.onlineModeMenuItemsSelector).hide();
                $(this.connectionNotificationElementId).html("Switching to offline mode, no internet connection");
                this._notificationStatusBadge('alert-danger', 'alert-info');
            }
        },

        _handleIsOnline: function() {
            if (this.isOfflineModeCapabilityEnabled) {
                console.log("Handling is  online");
                // this.submitData(this.onSubmitFormSuccess(), this.onSubmitFormError());
            }
        },

        _notificationStatusBadge: function(badgeToAdd, badgeToRemove) {
            // only apply the badges if offline capability is enabled
            if (this.isOfflineModeCapabilityEnabled) {
                $(this.connectionNotificationElementId).addClass(badgeToAdd);
                $(this.connectionNotificationElementId).removeClass(badgeToRemove);
            }
        },

        appendDataToStorage: function(dataKey, data) {
            let existingData = this.retrieveJson(dataKey);

            if (existingData === null) {
                existingData = [data];
            } else {
                existingData.push(data);
            }
            this.saveJson(dataKey, existingData);
        },

        formDataKey: function () {
            return Base64.encode("form_data_" + this.userId);
        },

        saveFormData: function(data, submissionUrl) {
            let me = this;
            let dataToBeSubmitted = {
                'submissionUrl': submissionUrl,
                'data': {
                    'userId': me.userId,
                    'payload': data,
                    'savedOn': (new Date()).getTime()
                }
            };
            this.appendDataToStorage(this.formDataKey(), Base64.encode(dataToBeSubmitted));
        },

        onSubmitFormSuccess: function() {
            return ((index, remainingDataToSubmit) =>  {
               console.log(remainingDataToSubmit);
               // purge from the store
                delete remainingDataToSubmit[index];

                let unSubmittedData = remainingDataToSubmit.filter(item => item !== undefined);

                if (unSubmittedData.length === 0) {
                    // all data has been submitted
                    this.remove(this.formDataKey());

                    $(this.connectionNotificationElementId).html("You are now online, offline mode switched off. " +
                        "All saved data has been submitted");
                } else {
                    this.saveJson(this.formDataKey(), unSubmittedData);
                }
                return unSubmittedData
            })
        },

        onSubmitFormError: function() {
            return (response =>  {
                console.log(response) ;
            })
        },

        submitData: function (dataKey, successHandler, errorHandler) {

            let dataToSubmit = this.retrieveJson(dataKey);

            if (dataToSubmit == null) {
                console.log("There is no pending data to be submitted");
                return;
            }

            dataToSubmit.filter(item => item !== undefined).forEach((toSubmit, index) => {
                $.ajax({
                    url: data.submissionUrl,
                    type: "POST",
                    data: JSON.stringify(toSubmit.data),
                    success: (message) => {
                        console.log("Saved form data submitted successfully: " + message);
                        dataToSubmit = this.onSubmitFormSuccess(index, dataToSubmit);
                    },
                    error: errorHandler
                });
            });
        }
    };

    return {
        client: function (connectionNotificationElementId, onlineModeMenuItemsSelector, connectivityCheckSecondsInterval) {
            console.log("Initializing offline mode client");
            // implement it as a singleton to ensure we have only one instance of it
            if (window.offlineModeClient === undefined) {
                offlineModeClient.connectionNotificationElementId = $("#" + connectionNotificationElementId);
                offlineModeClient.onlineModeMenuItemsSelector = $("." + onlineModeMenuItemsSelector);
                offlineModeClient.lastOfflineTime = null;
                offlineModeClient.lastOnlineTime = (new Date()).getTime();
                offlineModeClient.connectivityCheckSecondsInterval = connectivityCheckSecondsInterval;
                offlineModeClient.userId = userId;
                offlineModeClient.checkConnectivity();
                offlineModeClient.notifyConnectivityStatus();
                offlineModeClient.periodicallyCheckConnectivity();
                window.offlineModeClient = offlineModeClient;
            }

            return window.offlineModeClient;
        },

        onLoginEventHandler: function () {
            console.log("Handling on login event handler");
        }
    };
};

