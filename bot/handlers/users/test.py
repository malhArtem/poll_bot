from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.keyboard import TestCallbackFactory, AnalysisCallbackFactory, BuyCallbackFactory, InviteCallbackFactory
from db.models.tests import Tests
from db.models.tests_answers import Answers
from db.models.tests_progress import Progress
from db.models.tests_questions import Questions

router = Router()


@router.callback_query(TestCallbackFactory.filter(F.question_number == 1))
async def question(callback: types.CallbackQuery, callback_data: TestCallbackFactory, session, state: FSMContext):
    question = await Questions.get_question_by_test_id(test_id=callback_data.test_id,
                                                       question_number=callback_data.question_number,
                                                       session=session)
    answers = await Answers.get_answers_for_question(test_id=callback_data.test_id,
                                                     question_id=question.id,
                                                     session=session)
    await Progress.add_progress(callback_data.test_id, callback.from_user.id, callback_data.question_number, session=session)
    await state.update_data(question_number=question.id)
    await state.update_data(score=0)

    text = f"{question.question}\n\n"

    builder = InlineKeyboardBuilder()
    for i, answer in enumerate(answers):
        text += f"{i+1}. {answer.answer}\n"

        builder.button(text=str(i+1), callback_data=TestCallbackFactory(test_id=callback_data.test_id,
                                                                        question_number=callback_data.question_number + 1,
                                                                        answer_id=answer.id))

    builder.adjust(2)
    await callback.answer()
    await callback.message.edit_text(text=text, reply_markup=builder.as_markup())


@router.callback_query(TestCallbackFactory.filter())
async def answer(callback: types.CallbackQuery, callback_data: TestCallbackFactory, session, state: FSMContext):
    selected_answer = await Answers.get_answer(callback_data.answer_id, session)
    data = await state.get_data()
    await state.update_data(question_number=callback_data.question_number)

    await state.update_data(score=data.get('score', 0) + selected_answer.score)

    test = await Tests.get_test(callback_data.test_id, session)
    if test.show_answer:
        await callback.answer(selected_answer.comment)

    question = await Questions.get_question_by_test_id(test_id=callback_data.test_id,
                                                       question_number=callback_data.question_number,

                                                       session=session)
    print(question)
    if question is None:

        data = await state.get_data()
        points = data.get('score', 0)
        text = test.last_message.format(points=points)
        print(text)

        if test.is_free:
            builder = InlineKeyboardBuilder()
            builder.button(text="Получить разбор", callback_data=AnalysisCallbackFactory(test_id=callback_data.test_id))
            await callback.message.edit_text(text, reply_markup=builder.as_markup())
        else:
            text2 = "Спасибо за учаситие в тесте, вы можете приобрести полный разбор теста"
            builder = InlineKeyboardBuilder()
            builder.button(text="Приобрести за 100 рублей", callback_data=BuyCallbackFactory(test_id=callback_data.test_id))

            if test.invite_answer:
                builder.button(text="Пригласить друга", callback_data=InviteCallbackFactory(test_id=callback_data.test_id))
            await callback.message.edit_text(text)
            await callback.message.answer(text2, reply_markup=builder.as_markup())
        return

    answers = await Answers.get_answers_for_question(test_id=callback_data.test_id,
                                                     question_id=question.id,
                                                     session=session)

    text = f"{question.question}\n\n"

    builder = InlineKeyboardBuilder()
    for i, answer in enumerate(answers):
        text += f"{i + 1}. {answer.answer}\n"

        builder.button(text=str(i + 1), callback_data=TestCallbackFactory(test_id=callback_data.test_id,
                                                                          question_number=callback_data.question_number + 1,
                                                                          answer_id=answer.id))

    builder.adjust(2)

    await callback.message.edit_text(text=text, reply_markup=builder.as_markup())

