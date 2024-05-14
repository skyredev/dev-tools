import json
from DevTools.EntityMetadata.Fields.Datetime import Datetime
from DevTools.EntityMetadata.Fields.Text import Text
from DevTools.EntityMetadata.Fields.Varchar import Varchar
from DevTools.EntityMetadata.Fields.Link import Link
from DevTools.EntityMetadata.Fields.Link_Multiple import Link_Multiple
from DevTools.EntityMetadata.Fields.Enum import Enum
from DevTools.EntityMetadata.Fields.Email import Email
from DevTools.EntityMetadata.Fields.Phone import Phone
from DevTools.EntityMetadata.Fields.Address import Address
from DevTools.EntityMetadata.Links.BelongsTo import BelongsTo
from DevTools.EntityMetadata.Links.HasMany import HasMany
from DevTools.EntityMetadata.Links.HasChildren import HasChildren


class Person:
    @staticmethod
    def create_new_entity(**kwargs):
        name = Varchar("name")
        name.set_value('required', True)
        name.set_value('pattern', '$noBadCharacters')

        salutationName = Enum("salutationName")
        salutationName.set_value('options', [
            "",
            "Mr.",
            "Ms.",
            "Mrs.",
            "Dr."
        ])

        firstName = Varchar("firstName")
        firstName.set_value('maxLength', 100)

        lastName = Varchar("lastName")
        lastName.set_value('maxLength', 100)
        lastName.set_value('required', True)

        description = Text("description")

        emailAddress = Email("emailAddress")

        phoneNumber = Phone("phoneNumber")
        phoneNumber.set_value('typeList', [
            "Mobile",
            "Office",
            "Home",
            "Fax",
            "Other"
        ])
        phoneNumber.set_value('defaultType', "Mobile")

        address = Address("address")

        addressStreet = Text("addressStreet")
        addressStreet.set_value('maxLength', 255)
        addressStreet.set_value('dbType', "varchar")

        addressCity = Varchar("addressCity")

        addressState = Varchar("addressState")

        addressCountry = Varchar("addressCountry")

        addressPostalCode = Varchar("addressPostalCode")

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

        link_meetings = HasMany("meetings")
        link_meetings.set_value('entity', 'Meeting')
        link_meetings.set_value('foreign', 'parent')
        link_meetings.set_value('layoutRelationshipsDisabled', True)

        link_calls = HasMany("calls")
        link_calls.set_value('entity', 'Call')
        link_calls.set_value('foreign', 'parent')
        link_calls.set_value('layoutRelationshipsDisabled', True)

        link_tasks = HasChildren("tasks")
        link_tasks.set_value('entity', 'Task')
        link_tasks.set_value('foreign', 'parent')
        link_tasks.set_value('layoutRelationshipsDisabled', True)

        link_emails = HasChildren("emails")
        link_emails.set_value('entity', 'Email')
        link_emails.set_value('foreign', 'parent')
        link_emails.set_value('layoutRelationshipsDisabled', True)

        return json.dumps({
            "fields": {
                name.name: name.data,
                salutationName.name: salutationName.data,
                firstName.name: firstName.data,
                lastName.name: lastName.data,
                description.name: description.data,
                emailAddress.name: emailAddress.data,
                phoneNumber.name: phoneNumber.data,
                address.name: address.data,
                addressStreet.name: addressStreet.data,
                addressCity.name: addressCity.data,
                addressState.name: addressState.data,
                addressCountry.name: addressCountry.data,
                addressPostalCode.name: addressPostalCode.data,
                createdAt.name: createdAt.data,
                modifiedAt.name: modifiedAt.data,
                createdBy.name: createdBy.data,
                modifiedBy.name: modifiedBy.data,
                assignedUser.name: assignedUser.data,
                teams.name: teams.data
            },
            "links": {
                link_createdBy.name: link_createdBy.data,
                link_modifiedBy.name: link_modifiedBy.data,
                link_assignedUser.name: link_assignedUser.data,
                link_teams.name: link_teams.data,
                link_meetings.name: link_meetings.data,
                link_calls.name: link_calls.data,
                link_tasks.name: link_tasks.data,
                link_emails.name: link_emails.data
            },
            "collection": {
                "orderBy": "createdAt",
                "order": "desc"
            },
            "indexes": {
                "firstName": {
                    "columns": [
                        "firstName",
                        "deleted"
                    ]
                },
                "name": {
                    "columns": [
                        "firstName",
                        "lastName"
                    ]
                },
                "assignedUser": {
                    "columns": [
                        "assignedUserId",
                        "deleted"
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
