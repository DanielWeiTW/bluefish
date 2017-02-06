{
    "@odata.type": "#LogService.v1_0_2.LogService",
    "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/LogServices/Members/$entity",
    "@odata.id": "/redfish/v1/Managers/1/LogServices/Log",
    "Id": "Log",
    "Name": "System Log Service",
    "MaxNumberOfRecords": 1000,
    "OverWritePolicy": "WrapsWhenFull",
    "DateTime": "{{DateTime}}",
    "DateTimeLocalOffset": "+00:00",
    "ServiceEnabled": true,
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "Oem": {},
    "Actions": {
        "#LogService.ClearLog": {
            "target": "/redfish/v1/Managers/1/LogServices/Log/Actions/LogService.ClearLog"
        }
    },
    "Entries": {
        "@odata.id": "/redfish/v1/Managers/1/LogServices/Log/Entries"
    }
}