import rules


@rules.predicate
def is_admin(user):
    return user.is_superuser


rules.add_perm('user.is_superuser', is_admin)
