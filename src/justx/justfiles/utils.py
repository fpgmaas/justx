from justx.justfiles.models import Recipe, RecipeGroup


def group_recipes(recipes: list[Recipe]) -> list[RecipeGroup]:
    """Group recipes by group name, alphabetically, ungrouped last.

    Returns a list of RecipeGroup tuples. If no recipes have groups,
    returns [RecipeGroup(None, recipes)] for flat-list behavior.
    """
    if not recipes:
        return []

    if not any(r.groups for r in recipes):
        return [RecipeGroup(None, recipes)]

    seen_groups: dict[str, list[Recipe]] = {}
    ungrouped: list[Recipe] = []

    for recipe in recipes:
        if recipe.groups:
            for group in recipe.groups:
                seen_groups.setdefault(group, []).append(recipe)
        else:
            ungrouped.append(recipe)

    result: list[RecipeGroup] = []
    if ungrouped:
        result.append(RecipeGroup(None, ungrouped))
    result.extend(RecipeGroup(name, seen_groups[name]) for name in sorted(seen_groups))
    return result
