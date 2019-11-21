from margin_strategy_sdk import *
from typing import Dict, List
"""
Below you find several functions that must/can be implemented. The
strategy should be implemented in an event based fashion, if
possible. This means the strategy itself is passive and only
reacts to the incoming update events.

It is however possible to spawn your own threads, for ongoing
tasks. In that case you have to ensure that NO threads are
running after calls to stop or suspend.

The calls to your functions should return almost immediately. They
will effectively time out after 2 seconds, causing the strategy to
stop. If the call stays below 2 seconds, but still takes
exceptionally long, the user might experience a freezing user
interface.

You can use print() to print something in the strategy output
widget or write_log() to write to the margin log (look up
write_log in the documentation).

Besides that the StrategyBase class contains a range of important
functions for your implementation such as place_limit_order,
cancel_order, get_currency_pair, get_buffered_candles and many
more. You can find all of them described in the documentation.

Before placing an order, ensure that the parameters are valid
using the functionalities of the TradingCapabilityManager that can
be acquired through the get_trading_capability_manager function of
the StrategyBase class.
"""


class Strategy(StrategyBase):
    def __init__(self) -> None:
        self.waiting_order_id = 0
        self.waiting_cancel_order_id = None
        self.strategy_state = dict()

    ##################################################################
    # strategy logic methods
    ##################################################################
    """
    Initializes the strategy. It is the first function that is
    called after the strategy creation.
    """
    def init(self) -> None:
        print("Strategy init function!")

    """
    Returns the configuration of this strategy used by the margin
    embedding code. What you return here will influence what kind of
    data updates your strategy will receive.
    """
    def get_strategy_config(self) -> StrategyConfig:
        s = StrategyConfig()
        s.required_data_updates = {StrategyConfig.ORDER_BOOK,
                                   StrategyConfig.TICKER,
                                   StrategyConfig.PUBLIC_TRADE_HISTORY,
                                   StrategyConfig.FUNDS}
        return s

    """
    Return the save state of the strategy. This function will be
    called regularly and on closing margin to ensure that the user
    can resume the strategy when restarting margin.
    Place everything that the strategy needs to remember through
    restarting or after a potential crash in the returned
    dictionary.
    """
    def save_strategy_state(self) -> Dict[str, str]:
        return self.strategy_state

    """
    Restore the strategy from the save state. This function is
    called after margin was closed or otherwise stopped and is
    restarted. The strategy_status parameter contains the data that
    you returned previously in save_strategy_state.
    """
    def restore_strategy_state(self, strategy_state: Dict[str, str]) -> None:
        self.strategy_state = strategy_state

    """
    Start the strategy. This function is called to start the
    strategy. After it is called, your strategy  will receive data
    updates on all the data that you subscribed for and can react to
    them accordingly.
    """
    def start(self) -> None:
        print("Strategy start function!")
        print("placing order")
        tcm = self.get_trading_capability_manager()
        # These values will need adaptation
        buy = True
        amount = 0.002
        price = 0.0001
        # make sure amount is rounded by exchange standards
        amount = tcm.round_amount(amount, RoundingType.ROUND)
        # example checks for order validity
        # (is_order_valid also does the min/max comparisons)
        assert(tcm.get_min_buy_amount(price) <= amount)
        assert(tcm.get_max_buy_amount(price) >= amount)
        assert(tcm.is_order_valid(buy, amount, price))
        # Uncomment to activate the order placing
        # self.waiting_order_id = self.place_limit_order(buy, amount, price)

    """
    Stop the strategy. When this function is called you have to
    ensure that nothing is running inside your python
    implementation. After the stop function is called, the python
    interpreter that the strategy was running on is discarded so
    there is no need to clean up any data you created.

    The user will also be asked whether he/she wants to cancel
    existing orders placed by the strategy, so there is no need for
    the Python strategy to do this.
    """
    def stop(self) -> None:
        print("Strategy stop function!")

    """
    Suspend the strategy. Similar to the stop function you have to
    ensure that nothing is running after this call. However the
    python interpreter is kept and unsuspend can be called to
    continue the strategy from its suspended state.
    The strategy can be suspended if the user manually suspends it,
    if there is a network outage or right before closing margin. You
    have to ensure the save_strategy_state function still works
    after the suspension.
    If margin was closed while your strategy was running, it will be
    restored to the suspended state on the next start.
    """
    def suspend(self) -> None:
        print("Strategy suspend called")

    """
    Unsuspend the strategy. After the strategy has been suspended it
    will be possible for the user to unsuspend it. In this case, the
    strategy should be back to the state prior to the suspend call
    after unsuspend is done.
    Note that there may be a succession of save_strategy_state, a
    restart of margin and the call to restore_strategy_state in
    between the suspend and unsuspend calls.
    """
    def unsuspend(self) -> None:
        print("Strategy unsuspend called")

    ##################################################################
    # public data update methods
    ##################################################################
    """
    Notifies the strategy of a new order book. This will only be
    called if your strategy configuration contains the
    StrategyConfig.ORDER_BOOK flag as a required data update.
    """
    def on_new_order_book(self, order_book: OrderBook) -> None:
        pass

    """
    Notifies the strategy of a new ticker.This will only be called
    if your strategy configuration contains the
    StrategyConfig.TICKER flag as a required data update.
    """
    def on_new_ticker(self, ticker: Ticker) -> None:
        pass

    """
    Notifies the strategy of a new public trades.This will only be
    called if your strategy configuration contains the
    StrategyConfig.PUBLIC_TRADE_HISTORY flag as a required data
    update.
    """
    def on_new_public_trades(self, trades: List[PublicTrade]) -> None:
        pass

    ##################################################################
    # private update methods
    ##################################################################
    """
    Notifies the strategy of an update to the user funds.This will
    only be called if your strategy configuration contains the
    StrategyConfig.FUNDS flag as a required data update.
    """
    def on_new_funds(self, funds: Dict[str, FundsEntry]) -> None:
        print("Strategy funds function!", funds)

    """
    Notifies the strategy of an update to a strategy-placed order.
    This function will be called whenever a change to one of the
    orders placed by it occurs. Look up the documentation of
    OrderUpdate to learn more about what the update contains.
    """
    def on_order_update(self, update: OrderUpdate) -> None:
        print("Order update status was: ", update.status)
        if update.status == OrderUpdate.FILLED:
            pass
        elif update.status == OrderUpdate.ADAPTED:
            pass
        elif update.status == OrderUpdate.CANCELED:
            pass
        elif update.status == OrderUpdate.NO_CHANGE:
            pass
        elif update.status == OrderUpdate.REAPPEARED:
            pass
        elif update.status == OrderUpdate.DISAPPEARED:
            pass
        elif update.status == OrderUpdate.PARTIALLY_FILLED:
            pass
        elif update.status == OrderUpdate.ADAPTED_AND_FILLED:
            pass
        elif update.status == OrderUpdate.OTHER_CHANGE:
            pass

    """
    When placing an order (using the place_limit_order function) you
    will receive a place_order_id as a result. When the placing of
    the order is finished, either this function or
    on_place_order_error_string will be called, providing the result
    of the order. This function covers the success case and includes
    the resulting order for a specific place_order_id.
    Note that the place_order_id will no longer be used after this
    call. Afterwards, use Order.id of the resulting order instead
    (for example to cancel the order or when handling order
    updates).
    """
    def on_place_order_success(self, place_order_id: int, order: Order) -> None:
        print("Strategy place order success")
        if self.waiting_order_id == place_order_id:
            print("Had waiting order id")
        else:
            print("Did not have waiting order id")

    """
    When placing an order (using the place_limit_order function) you
    will receive a place_order_id as a result. When the placing of
    the order is finished, either this function or
    on_place_order_success will be called, providing the result of
    the order. This function covers the error case and includes the
    error that occurred for a specific place_order_id.
    Note that the place_order_id will no longer be used after this
    call.
    """
    def on_place_order_error_string(self, place_order_id: int, error: str) -> None:
        self.exit(ExitReason.ERROR, error)

    """
    After a call to cancel_order you will have to wait for either
    this call or on_cancel_order_error_string to be called with the
    order_id of the to be canceled order.
    This function signifies the success of the canceling and
    provides the latest state of the canceled order.
    """
    def on_cancel_order_success(self, order_id: int, canceled_order: Order) -> None:
        print("Strategy cancel order success")
        if self.waiting_cancel_order_id == order_id:
            print("Had waiting cancel id")
            self.exit(ExitReason.FINISHED_SUCCESSFULLY)

    """
    After a call to cancel_order you will have to wait for either
    this call or on_cancel_order_success to be called with the
    order_id of the to be canceled order.
    This function signifies that there was an error while canceling
    and provides the corresponding error message.
    """
    def on_cancel_order_error_string(self, order_id: int, error: str) -> None:
        self.exit(ExitReason.ERROR, error)
