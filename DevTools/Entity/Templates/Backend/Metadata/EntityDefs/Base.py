import json
from DevTools.Entity.Fields.Datetime import Datetime
from DevTools.Entity.Fields.Text import Text
from DevTools.Entity.Fields.Varchar import Varchar
from DevTools.Entity.Fields.Link import Link
from DevTools.Entity.Fields.Link_Multiple import Link_Multiple
from DevTools.Entity.Links.BelongsTo import BelongsTo
from DevTools.Entity.Links.HasMany import HasMany


class Base:
    @staticmethod
    def create_new_entity(**kwargs):
        name = Varchar("name")
        name.set_value('required', True)
        name.set_value('pattern', '$noBadCharacters')

        description = Text("description")

        createdAt = Datetime("createdAt")
        createdAt.set_value('readOnly', True)

        modifiedAt = Datetime("modifiedAt")
        modifiedAt.set_value('readOnly', True)

        createdBy = Link("createdBy")
        createdBy.set_value('view', 'views/fields/user')
        createdBy.set_value('readOnly', True)

        modifiedBy = Link("modifiedBy")
        modifiedBy.set_value('view', 'views/fields/user')
        modifiedBy.set_value('readOnly', True)

        assignedUser = Link("assignedUser")
        assignedUser.set_value('view', 'views/fields/assigned-user')
        assignedUser.set_value('required', False)

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

        return json.dumps({
            "fields": {
                name.name: name.data,
                description.name: description.data,
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
                link_teams.name: link_teams.data
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
