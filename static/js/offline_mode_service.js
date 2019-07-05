/*
    A service exposing an abstractions to make the system work when there's no internet connection
*/

let OfflineModeService = function () {
    "use strict";

    let offlineModeClient = {
        isConnectionOn: true,

        connectivityCheckSecondsInterval: 60000,

        connectionNotificationElementId: undefined,

        onlineModeMenuItemsSelector: undefined,

        connectivityCheckUrl: undefined,

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
            let me = this;
            $.ajax({
                url: this.connectivityCheckUrl,
                type: "GET",
                success: function () {
                    me.isConnectionOn = true;

                } ,
                error: function () {
                    me.isConnectionOn = false;
                }
            });
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
                $(this.connectionNotificationElementId).addClass('alert-info');
                $(this.connectionNotificationElementId).removeClass('alert-danger');
            } else {
                $(this.onlineModeMenuItemsSelector).hide();
                $(this.connectionNotificationElementId).html("Switching to offline mode, no internet connection");
                $(this.connectionNotificationElementId).removeClass('alert-info');
                $(this.connectionNotificationElementId).addClass('alert-danger');
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

        saveFormData: function(dataKey, data, submissionUrl) {
            let dataToBeSubmitted = {
                'submissionUrl': submissionUrl,
                'data': data,
                'savedOn': (new Date()).getTime()
            };
            this.appendDataToStorage(dataToBeSubmitted);
        },

        submitData: function (dataKey, successHandler, errorHandler) {

            let dataToSubmit = this.retrieveJson(dataKey);

            if (dataToSubmit == null) {
                return errorHandler("There is no pending data to be submitted")
            }

            dataToSubmit.forEach(data => {
                $.ajax({
                    url: data.submissionUrl,
                    type: "POST",
                    data: JSON.stringify(data.data),
                    success: successHandler ,
                    error: errorHandler
                });
            });
        }

    };

    return {
        client: function (connectivityCheckUrl, connectionNotificationElementId, onlineModeMenuItemsSelector, connectivityCheckSecondsInterval) {
            console.log("Initializing offline mode client");
            // implement it as a singleton to ensure we have only one instance of it
            if (window.offlineModeClient === undefined) {
                offlineModeClient.connectivityCheckUrl = connectivityCheckUrl;
                offlineModeClient.connectionNotificationElementId = $("#" + connectionNotificationElementId);
                offlineModeClient.onlineModeMenuItemsSelector = $("." + onlineModeMenuItemsSelector);
                offlineModeClient.lastOfflineTime = null;
                offlineModeClient.lastOnlineTime = (new Date()).getTime();
                offlineModeClient.connectivityCheckSecondsInterval = connectivityCheckSecondsInterval;
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

