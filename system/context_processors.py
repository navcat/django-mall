from django.db.models import Sum

from utils import constants


def shop_cart(request):
    """ 购物车统计 """
    user = request.user
    cart_list = []
    cart_total = {}
    if user.is_authenticated:
        cart_list = user.carts.filter(status=constants.TRANS_STATU_INIT)
        # 总金额
        cart_total = cart_list.aggregate(sum_amount=Sum('amount'), sum_count=Sum('count'))
    return {
        'constants': constants,
        'cart_list': cart_list,
        'cart_total': cart_total
    }