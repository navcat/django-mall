from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from mall.models import Product
from mine.models import Order, Collection, Cart
from utils import constants, tools


class OrderList(ListView):
    """ 订单列表 """
    model = Order
    template_name = 'mine/order_list.html'

    def get_queryset(self):
        # 当前用户的订单，排除已删除的订单
        # 根据状态查询
        status = self.request.GET.get('status', '')
        query = Q(user=self.request.user)
        if status:
            query = query & Q(status=status)
        return Order.objects.filter(query).exclude(
            status=constants.TRANS_STATU_DELETED
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            status = int(self.request.GET.get('status', ''))
        except ValueError:
            status = ''
        context['status'] = status
        return  context


class OrderDetail(DetailView):
    """  订单详情 """
    model = Order
    slug_field = 'sn'
    slug_url_kwarg = 'sn'
    template_name = 'mine/order_info.html'


class CollectList(ListView):
    """  产品收藏列表 """
    model = Collection
    paginate_by = 10
    template_name = 'mine/product_collect.html'


@login_required
def collect_add(request, pk):
    """ 添加收藏"""
    product = get_object_or_404(Product, uid=pk, is_valid=True)
    Collection.objects.get_or_create(product=product, user=request.user)
    return HttpResponse('ok')


@login_required
@transaction.atomic()
def cart_add(request, pk):
    """ 添加到购物车"""
    count = int(request.POST.get('count', 1))
    product = get_object_or_404(Product, uid=pk, is_valid=True)
    # 校验库存
    if product.sku_count <= count:
        return HttpResponse('no')
    # 库存减1
    product.update_store_count(count)
    # 添加到购物车，保存快照
    # 如果购物车中已经存在，则将购买数量增加1，并更新价格
    try:
        cart = Cart.objects.get(product=product, user=request.user, status=constants.TRANS_STATU_INIT)
        count = cart.count + 1
        cart.count = count
        cart.amount = cart.price * count
        cart.save()
    except Cart.DoesNotExist:
        Cart.objects.create(product=product,
                            user=request.user,
                            name=product.name,
                            img=product.img,
                            price=product.price,
                            origin_price=product.origin_price,
                            amount=product.price * count,
                            count=count
                            )
    return HttpResponse('ok')


@login_required
@transaction.atomic()
def order_submit(request):
    """ 提交订单 """
    # 用户的默认地址
    default_addr = request.user.default_addr
    if not default_addr:
        # 请先完善地址信息
        messages.error(request, '请先完善地址信息')
        return redirect('accounts:address_list')

    # 查找用户的购物车信息
    cart_list = request.user.carts.filter(status=constants.TRANS_STATU_INIT)
    # 总金额
    cart_total = cart_list.aggregate(sum_amount=Sum('amount'), sum_count=Sum('count'))
    order = Order.objects.create(
        sn=tools.generate_trans_id(),
        user=request.user,
        buy_count=cart_total['sum_count'],
        buy_amount=cart_total['sum_amount'],
        to_user=default_addr.username,
        to_area=default_addr.show_region,
        to_addr=default_addr.address,
        to_phone=default_addr.phone,
    )
    # 更新购物车中的数据
    cart_list.update(status=constants.TRANS_STATU_SUBMIT, order=order)
    return redirect('mine:order_info', sn=order.sn)


@login_required
@transaction.atomic()
def order_pay(request, sn):
    """ 订单支付 """
    user = request.user
    order = get_object_or_404(Order, sn=sn, user=user)
    # 判断余额
    if user.integral < order.buy_amount:
        messages.error(request, '您的积分余额不足')
        return redirect('mine:order_info', sn=sn)
    # 扣除积分
    user.ope_integral_account(0, order.buy_amount)
    # 更改订单状态
    order.status = constants.TRANS_STATU_PAIED
    order.save()
    # 更改购物车列表中的状态
    order.carts.all().update(status = constants.TRANS_STATU_PAIED)
    messages.success(request, '恭喜支付成功')
    return redirect('mine:order_info', sn=sn)