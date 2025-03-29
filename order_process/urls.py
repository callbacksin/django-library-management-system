from django.urls import path

from order_process.views import \
    OrderSummaryView, \
    add_to_cart, \
    remove_from_cart, \
    send_order, \
    OrderListView, \
    OrderDetailView, \
    set_orderbook_unavailable, \
    set_orderbook_available, \
    complete_order, \
    CompletedOrderListView, \
    CompletedOrderDetailView, \
    UserOrderListView, \
    UserOrderDetailView

urlpatterns = [
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<pk>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
    path('send-order/', send_order, name='send_order'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('completed-orders/', CompletedOrderListView.as_view(), name='completed_orders'),
    path('order/<pk>', OrderDetailView.as_view(), name='order'),
    path('completed-order/<pk>', CompletedOrderDetailView.as_view(), name='completed_order'),
    path('set-unavailable/<pk>', set_orderbook_unavailable, name='unset'),
    path('set-available/<pk>', set_orderbook_available, name='set'),
    path('complete-order/<pk>', complete_order, name='complete_order'),
    path('my-orders/', UserOrderListView.as_view(), name='user_orders'),
    path('my-order/<pk>', UserOrderDetailView.as_view(), name='user_order'),
]
