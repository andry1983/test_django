# pylint: disable=trailing-whitespace,import-error,no-name-in-module
from typing import List, Union

from apps.users.models import UserReferrerCode, User


def get_tree_root_owner_by_referrer_id(id_referrer: int) -> Union[int, None]:
    if not id_referrer:
        return
    if not isinstance(id_referrer, int):
        raise ValueError(f'the id_referrer parameter must be of'
                         f' type int, not {type(id_referrer)}')

    parent_id = UserReferrerCode.objects.raw(
        '''
        WITH RECURSIVE owner(id, owner_user_id) AS (
        SELECT id, owner_user_id FROM user_referrer_code
        WHERE owner_user_id = %d
        UNION ALL 
        SELECT c.id, c.owner_user_id FROM user_referrer_code c, owner o 
        WHERE c.referrer_user_id = o.owner_user_id
        ) SELECT id, owner_user_id FROM owner order by owner_user_id limit 1;
           '''.replace('\n', '') % id_referrer
    )[:]

    return parent_id[0].owner_user_id if parent_id else None


def get_referrers_by_owner_id(owner_id: int) -> Union[List[User], None]:
    if not owner_id:
        return
    if not isinstance(owner_id, int):
        raise ValueError(f'the owner_id parameter must be of'
                         f' type int, not {type(owner_id)}')

    return User.objects.raw(
        '''
        WITH RECURSIVE r_owner(owner_user_id, referrer_user_id) AS (
            SELECT owner_user_id, referrer_user_id
            FROM user_referrer_code
            WHERE owner_user_id = %d and referrer_user_id is not null
            UNION ALL
            SELECT c.owner_user_id, c.referrer_user_id
            FROM user_referrer_code c,
                 r_owner ro
            WHERE c.owner_user_id = ro.referrer_user_id
        )
        SELECT u.*
        FROM r_owner join "user" u on u.id = owner_user_id order by u.id;
        '''.replace('\n', '') % owner_id
    )[:]


def update_referrer_owners_points(referrer_owner_id: int) -> List[User]:
    updates_ids = set()
    referrer_root_user_id: [int] = get_tree_root_owner_by_referrer_id(
        referrer_owner_id)
    owners = get_referrers_by_owner_id(referrer_root_user_id)
    if owners:
        for idx, user in enumerate(owners):
            if not user.id in updates_ids:
                updates_ids.add(user.id)
                user.points = len(owners[idx:]) + 1
                user.save()
    return owners
