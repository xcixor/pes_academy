from agripitch.models import SubCriteriaItemResponse, SubCriteriaItem


def get_sub_criteria_item_by_label(label):
    return SubCriteriaItem.objects.get(label=label)


def get_sub_criteria_item_response_if_exist(sub_criteria_item):
    response = None
    try:
        response = SubCriteriaItemResponse.objects.get(
            sub_criteria_item=sub_criteria_item)
    except SubCriteriaItemResponse.DoesNotExist:
        pass
    return response
