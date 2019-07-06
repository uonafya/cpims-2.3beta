/*
    A service exposing an abstractions to make the system work when there's no internet connection
*/

let OfflineModeService = function (_userId, offlineModeCapabilityEnabled) {
    "use strict";

    let offlineModeClient = {
        _isConnectionOn: true,

        _isOfflineModeCapabilityEnabled: offlineModeCapabilityEnabled,

        _connectivityCheckSecondsInterval: 60000,

        _userId: _userId,

        _connectionNotificationElementId: undefined,

        _onlineModeMenuItemsSelector: undefined,

        _storage: localStorage,

        lastOnlineTime: undefined,

        lastOfflineTime: undefined,

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
                this._handleIsOnline();
            } else {
                $(this._onlineModeMenuItemsSelector).hide();
                $(this._connectionNotificationElementId).html("Switching to offline mode, no internet connection");
                this._notificationStatusBadge('alert-danger', 'alert-info');
            }
        },

        _handleIsOnline: function() {
            if (this._isOfflineModeCapabilityEnabled) {
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
            return ((index, remainingDataToSubmit) =>  {
               console.log(remainingDataToSubmit);
               // purge from the store
                delete remainingDataToSubmit[index];

                let unSubmittedData = remainingDataToSubmit.filter(item => item !== undefined);

                if (unSubmittedData.length === 0) {
                    // all data has been submitted
                    this.remove(this._formDataKey());

                    $(this._connectionNotificationElementId).html("You are now online, offline mode switched off. " +
                        "All saved data has been submitted");
                } else {
                    this.saveJson(this._formDataKey(), unSubmittedData);
                }
                return unSubmittedData
            })
        },

        _onSubmitFormError: function() {
            return (response =>  {
                console.log(response) ;
            })
        },

        submitData: function (dataKey, successHandler, errorHandler) {

            let dataToSubmit = this.retrieveJson(dataKey);

            if (dataToSubmit === null) {
                return;
            }

            dataToSubmit.filter(item => item !== undefined).forEach((toSubmit, index) => {
                let decodedData = JSON.parse(Base64.decode(toSubmit));
                $.ajax({
                    url: decodedData.submissionUrl,
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(decodedData.data),
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
                    },
                    success: function (message) {
                        console.log("Saved form data submitted successfully: " + message);
                        dataToSubmit = successHandler(index, dataToSubmit);
                    },
                    error: errorHandler
                });
            });
        }
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
            }

            return window.offlineModeClient;
        },

        onLoginEventHandler: function () {
            console.log("Handling on login event handler");
        }
    };
};

