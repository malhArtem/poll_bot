from aiogram.filters.callback_data import CallbackData


class TestCallbackFactory(CallbackData, prefix="test"):
    test_id: int
    question_number: int
    answer_id: int = 0


class AnalysisCallbackFactory(CallbackData, prefix="analysis"):
    test_id: int


class BuyCallbackFactory(CallbackData, prefix="buy"):
    test_id: int


class InviteCallbackFactory(CallbackData, prefix="invite"):
    test_id: int


class PaidCallbackFactory(CallbackData, prefix="paid"):
    test_id: int
    user_id: int


class SendAnalysisCallbackFactory(CallbackData, prefix="send"):
    test_id: int
    user_id: int