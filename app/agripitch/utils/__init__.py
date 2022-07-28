from agripitch.models import SubCriteriaItem


def get_sub_criteria_item_by_label(label):
    return SubCriteriaItem.objects.get(label=label)
