import json
from DevTools.Entity.Fields.Datetime import Datetime
from DevTools.Entity.Fields.Text import Text
from DevTools.Entity.Fields.Varchar import Varchar
from DevTools.Entity.Fields.Link import Link
from DevTools.Entity.Fields.Link_Multiple import Link_Multiple
from DevTools.Entity.Fields.Email import Email
from DevTools.Entity.Fields.Phone import Phone
from DevTools.Entity.Fields.Address import Address
from DevTools.Entity.Fields.Url import Url
from DevTools.Entity.Links.BelongsTo import BelongsTo
from DevTools.Entity.Links.HasMany import HasMany
from DevTools.Entity.Links.HasChildren import HasChildren


class Company:
    @staticmethod
    def create_new_entity(**kwargs):
        name = Varchar("name")
        name.set_value('required', True)
        name.set_value('pattern', '$noBadCharacters')

        description = Text("description")

        website = Url("website")
        website.set_value('strip', True)

        emailAddress = Email("emailAddress")

        phoneNumber = Phone("phoneNumber")
        phoneNumber.set_value('typeList', [
            "Office",
            "Mobile",
            "Fax",
            "Other"
        ])
        phoneNumber.set_value('defaultType', "Office")

        billingAddress = Address("billingAddress")

        billingAddressStreet = Text("billingAddressStreet")
        billingAddressStreet.set_value('maxLength', 255)
        billingAddressStreet.set_value('dbType', "varchar")

        billingAddressCity = Varchar("billingAddressCity")

        billingAddressState = Varchar("billingAddressState")

        billingAddressCountry = Varchar("billingAddressCountry")

        billingAddressPostalCode = Varchar("billingAddressPostalCode")

        shippingAddress = Address("shippingAddress")
        shippingAddress.set_value('view', 'crm:views/account/fields/shipping-address')

        shippingAddressStreet = Text("shippingAddressStreet")
        shippingAddressStreet.set_value('maxLength', 255)
        shippingAddressStreet.set_value('dbType', "varchar")

        shippingAddressCity = Varchar("shippingAddressCity")

        shippingAddressState = Varchar("shippingAddressState")

        shippingAddressCountry = Varchar("shippingAddressCountry")

        shippingAddressPostalCode = Varchar("shippingAddressPostalCode")

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
                description.name: description.data,
                website.name: website.data,
                emailAddress.name: emailAddress.data,
                phoneNumber.name: phoneNumber.data,
                billingAddress.name: billingAddress.data,
                billingAddressStreet.name: billingAddressStreet.data,
                billingAddressCity.name: billingAddressCity.data,
                billingAddressState.name: billingAddressState.data,
                billingAddressCountry.name: billingAddressCountry.data,
                billingAddressPostalCode.name: billingAddressPostalCode.data,
                shippingAddress.name: shippingAddress.data,
                shippingAddressStreet.name: shippingAddressStreet.data,
                shippingAddressCity.name: shippingAddressCity.data,
                shippingAddressState.name: shippingAddressState.data,
                shippingAddressCountry.name: shippingAddressCountry.data,
                shippingAddressPostalCode.name: shippingAddressPostalCode.data,
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
                "name": {
                    "columns": [
                        "name",
                        "deleted"
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
