import json
from DevTools.EntityMetadata.Fields.Datetime import Datetime
from DevTools.EntityMetadata.Fields.Json_Array import Json_Array
from DevTools.EntityMetadata.Fields.Text import Text
from DevTools.EntityMetadata.Fields.Varchar import Varchar
from DevTools.EntityMetadata.Fields.Link import Link
from DevTools.EntityMetadata.Fields.Link_Multiple import Link_Multiple
from DevTools.EntityMetadata.Fields.Enum import Enum
from DevTools.EntityMetadata.Fields.Boolean import Boolean
from DevTools.EntityMetadata.Fields.Duration import Duration
from DevTools.EntityMetadata.Fields.Link_Parent import Link_Parent
from DevTools.EntityMetadata.Links.BelongsTo import BelongsTo
from DevTools.EntityMetadata.Links.HasMany import HasMany
from DevTools.EntityMetadata.Links.BelongsToParent import BelongsToParent


class Event:
    @staticmethod
    def create_new_entity(**kwargs):
        name = Varchar("name")
        name.set_value('required', True)
        name.set_value('pattern', '$noBadCharacters')

        status = Enum("status")
        status.set_value('options', [
            "Planned",
            "Held",
            "Not Held"
        ])
        status.set_value('default', "Planned")
        status.set_value('style', {
            "Held": "success"
        })
        status.set_value('audited', True)

        dateStart = Datetime("dateStart")
        dateStart.set_value('required', True)
        dateStart.set_value('default', "javascript: return this.dateTime.getNow(15);")
        dateStart.set_value('audited', True)

        dateEnd = Datetime("dateEnd")
        dateEnd.set_value('required', True)
        dateEnd.set_value('after', "dateStart")
        dateEnd.set_value('suppressValidationList', [
            "required"
        ])

        isAllDay = Boolean("isAllDay")
        isAllDay.set_value('layoutListDisabled', True)
        isAllDay.set_value('layoutDetailDisabled', True)
        isAllDay.set_value('layoutMassUpdateDisabled', True)

        duration = Duration("duration")
        duration.set_value('start', "dateStart")
        duration.set_value('end', "dateEnd")
        duration.set_value('options', [
            300,
            600,
            900,
            1800,
            2700,
            3600,
            7200,
            10800
        ])
        duration.set_value('default', 300)
        duration.set_value('notStorable', True)
        duration.set_value('select', {
            "select": "TIMESTAMPDIFF_SECOND:(dateStart, dateEnd)"
        })
        duration.set_value('order', {
            "order": [
                [
                    "TIMESTAMPDIFF_SECOND:(dateStart, dateEnd)",
                    "{direction}"
                ]
            ]
        })

        parent = Link_Parent("parent")
        parent.set_value('entityList', [
            "Account",
            "Lead",
            "Contact"
        ])

        description = Text("description")

        reminders = Json_Array("reminders")
        reminders.set_value('notStorable', True)
        reminders.set_value('view', 'crm:views/meeting/fields/reminders')
        reminders.set_value('layoutListDisabled', True)
        reminders.set_value('validatorClassNameList', [
            "Espo\\Modules\\Crm\\Classes\\FieldValidators\\Event\\Reminders\\Valid",
            "Espo\\Modules\\Crm\\Classes\\FieldValidators\\Event\\Reminders\\MaxCount"
        ])

        createdAt = Datetime("createdAt")
        createdAt.set_value('readOnly', True)

        modifiedAt = Datetime("modifiedAt")
        modifiedAt.set_value('readOnly', True)

        createdBy = Link("createdBy")
        createdBy.set_value('readOnly', True)
        createdBy.set_value('view', 'views/fields/user')

        modifiedBy = Link("modifiedBy")
        modifiedBy.set_value('readOnly', True)
        modifiedBy.set_value('view', 'views/fields/user')

        assignedUser = Link("assignedUser")
        assignedUser.set_value('required', False)
        assignedUser.set_value('view', 'views/fields/assigned-user')

        teams = Link_Multiple("teams")
        teams.set_value('view', 'views/fields/teams')

        link_parent = BelongsToParent("parent")
        link_parent.set_value('foreign', f"{kwargs['entity_name']}Children")

        link_createdBy = BelongsTo("createdBy")
        link_createdBy.set_value('entity', 'User')

        link_modifiedBy = BelongsTo("modifiedBy")
        link_modifiedBy.set_value('entity', 'User')

        link_assignedUser = BelongsTo("assignedUser")
        link_assignedUser.set_value('entity', 'User')

        link_teams = HasMany("teams")
        link_teams.set_value('entity', 'Team')
        link_teams.set_value('relationName', 'entityTeam')
        link_teams.set_value('layoutRelationshipsDisabled', True)

        return json.dumps({
            "fields": {
                name.name: name.data,
                status.name: status.data,
                dateStart.name: dateStart.data,
                dateEnd.name: dateEnd.data,
                isAllDay.name: isAllDay.data,
                duration.name: duration.data,
                parent.name: parent.data,
                description.name: description.data,
                reminders.name: reminders.data,
                createdAt.name: createdAt.data,
                modifiedAt.name: modifiedAt.data,
                createdBy.name: createdBy.data,
                modifiedBy.name: modifiedBy.data,
                assignedUser.name: assignedUser.data,
                teams.name: teams.data
            },
            "links": {
                link_parent.name: link_parent.data,
                link_createdBy.name: link_createdBy.data,
                link_modifiedBy.name: link_modifiedBy.data,
                link_assignedUser.name: link_assignedUser.data,
                link_teams.name: link_teams.data
            },
            "collection": {
                "orderBy": "dateStart",
                "order": "desc"
            },
            "indexes": {
                "dateStartStatus": {
                    "columns": [
                        "dateStart",
                        "status"
                    ]
                },
                "dateStart": {
                    "columns": [
                        "dateStart",
                        "deleted"
                    ]
                },
                "status": {
                    "columns": [
                        "status",
                        "deleted"
                    ]
                },
                "assignedUser": {
                    "columns": [
                        "assignedUserId",
                        "deleted"
                    ]
                },
                "assignedUserStatus": {
                    "columns": [
                        "assignedUserId",
                        "status"
                    ]
                },
                "createdAt": {
                    "columns": [
                        "createdAt"
                    ]
                },
                "createdAtId": {
                    "unique": True,
                    "columns": [
                        "createdAt",
                        "id"
                    ]
                }
            }
        }, indent=4)
