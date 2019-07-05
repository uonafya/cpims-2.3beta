/*
    A service exposing an abstractions to make the system work when there's no internet connection
*/

let OfflineModeService = function () {
    "use strict";

    let offlineModeClient = {
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
            this.storage.removeItem(key);
        },

        isConnectivityActive: function () {

        },

        notifyConnectivityStatus: function() {
            if (this.isConnectivityActive()) {
                console.log("active menu");
                console.log("show abnner");
            } else {
                console.log("deactive menu");
                console.log("show banner");
            }

        },

        appendDataToStorage: function(dataKey, data) {
            let existingData = this.retrieve(dataKey);

            if (existingData === null) {
                existingData = [dataToBeSubmitted];
            } else {
                existingData = existingData.push(data);
            }
            this.saveJson(dataKey, existingData)
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
        client: function () {
            console.log("Initializing offline mode client");
            // implement it as a singleton to ensure we have only one instance of it
            if (window.offlineModeClient === undefined) {
                offlineModeClient.lastOfflineTime = null;
                offlineModeClient.lastOnlineTime = (new Date()).getTime();
                window.offlineModeClient = offlineModeClient;
            }

            return window.offlineModeClient;
        }
    };
};

