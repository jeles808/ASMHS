import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import sqlite3
from fpdf import FPDF
from db import init_db, fetch_all_answers,save_answers
from openpyxl import Workbook
from keyboards import (keyboard_start, Keyboard_q3, Keyboard_q4, Keyboard_q5, Keyboard_q6_q9,
                       Keyboard_q7_q8_q11_q12_q13_q15, Keyboard_q10, Keyboard_q14, Keyboard_q16,
                       Keyboard_q17, get_administrator_keyboard)

bot = Bot(token='6735071514:AAHE1uVzht-JYxDEHoCvd7s7nvtwJQ5Vzls')
dp = Dispatcher()


all_user_answers = []

ADMINISTRATORS_IDS = []

class Questions(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()
    question_11 = State()
    question_12 = State()
    question_13 = State()
    question_14 = State()
    question_15 = State()
    question_16 = State()
    question_17 = State()
    question_18 = State()


questions = {
    1: "Вопрос 1: Как вас зовут?",
    2: "Вопрос 2: Ваш возраст",
    3: "Вопрос 3: На каком вы курсе?",
    4: "Вопрос 4: Из какой вы группы?",
    5: "Вопрос 5: Как часто Вы занимаетесь физической активностью?",
    6: "Вопрос 6: Оцените ваше общее физическое состояние",
    7: "Вопрос 7: Испытываете ли Вы проблемы с сном?",
    8: "Вопрос 8: Имеете ли Вы хронические заболевания?",
    9: "Вопрос 9: Как Вы оцениваете свой рацион питания?",
    10: "Вопрос 10: Сколько раз в день Вы обычно едите?",
    11: "Вопрос 11: Чувствовали ли Вы стресс или тревогу за последние несколько месяцев?",
    12: "Вопрос 12: Есть ли у Вас кто-то, с кем Вы можете поговорить о своих проблемах?",
    13: "Вопрос 13: Испытывали ли Вы чувство депрессии или безнадежности в последнее время?",
    14: "Вопрос 14: Как часто Вы употребляете алкогольные напитки?",
    15: "Вопрос 15: Курите ли Вы?",
    16: "Вопрос 16: Сколько часов в день Вы обычно проводите за компьютером или смартфоном вне учебного времени?",
    17: "Вопрос 17: Как часто физическое или психологическое состояние мешает Вам учиться?",
    18: "Благодарим за прохождения теста и желаем удачи в учебе!"
}



init_db()



@dp.message(lambda message: message.text == 'Результаты')
async def send_results(message: types.Message):
    if message.from_user.id in ADMINISTRATORS_IDS:
        answers = fetch_all_answers()
        if answers:
            answers_text = "\n".join([f"{r[0]}, User ID: {r[1]}, Answer 1: {r[2]}, Answer 2: {r[3]}, Answer 3: {r[4]},"
                                       f" Answer 4: {r[5]}, Answer 5: {r[6]}, Answer 6: {r[7]}, Answer 7: {r[8]},"
                                       f" Answer 8: {r[9]}, Answer 9: {r[10]}, Answer 10: {r[11]},  Answer 11: {r[12]},"
                                       f" Answer 12: {r[13]}, Answer 13: {r[14]}, Answer 14: {r[15]},"
                                       f" Answer 15: {r[16]}, Answer 16: {r[17]},"
                                       f" Answer 17: {r[18]}" for r in answers])
            await message.answer(answers_text[:4096])  # Telegram ограничивает длину сообщения 4096 символами
        else:
            await message.answer("Нет сохраненных результатов.")
    else:
        await message.answer("У вас нет доступа к этой команде.")




column_to_question = {
    'answer_5': "Как часто Вы занимаетесь физической активностью?",
    'answer_6': "Оцените ваше общее физическое состояние",
    'answer_7': "Испытываете ли Вы проблемы с сном?",
    'answer_8': "Имеете ли Вы хронические заболевания?",
    'answer_9': "Как Вы оцениваете свой рацион питания?",
    'answer_10': "Сколько раз в день Вы обычно едите?",
    'answer_11': "Чувствовали ли Вы стресс или тревогу за последние несколько месяцев?",
    'answer_12': "Есть ли у Вас кто-то, с кем Вы можете поговорить о своих проблемах?",
    'answer_13': "Испытывали ли Вы чувство депрессии или безнадежности в последнее время?",
    'answer_14': "Как часто Вы употребляете алкогольные напитки?",
    'answer_15': "Курите ли Вы?",
    'answer_16': "Сколько часов в день Вы обычно проводите за компьютером или смартфоном вне учебного времени?",
    'answer_17': "Как часто физическое или психологическое состояние мешает Вам учиться?"
}



def answer_analysis():
    conn = sqlite3.connect('answers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answers';")
    tables = cursor.fetchall()
    analysis_results = []
    excluded_columns = ['id', 'user_id', 'Start', 'answer_1', 'answer_2', 'answer_3', 'answer_4']

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        total_rows = cursor.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()[0]

        for column in columns:
            column_name = column[1]
            if column_name not in excluded_columns and column_name in column_to_question:
                question_text = column_to_question[column_name]
                cursor.execute(f"SELECT {column_name}, COUNT({column_name}) FROM {table_name} GROUP BY {column_name};")
                values_count = cursor.fetchall()

                column_results = f"Вопрос: {question_text}\n"
                for value_count in values_count:
                    value = value_count[0]
                    count = value_count[1]
                    percentage = (count / total_rows) * 100
                    column_results += f"Значение: {value} | Процент: {percentage:.2f}%\n"
                analysis_results.append(column_results)

    conn.close()
    return "\n".join(analysis_results)


def create_pdf_analysis(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('font', '', 'Hero-Regular.ttf', uni=True)
    pdf.set_font('font', size=14)
    pdf.cell(200, 14, "Мониторинг здоровья обучающихся", 0, 1, 'C')

    pdf.set_font('font', size=12)
    for line in data.split('\n'):
        pdf.multi_cell(190, 6, txt=line)
    pdf_file_path = 'analysis_results.pdf'
    pdf.output(pdf_file_path)
    return pdf_file_path


@dp.message(lambda message: message.text == 'Анализ ответов PDF')
async def send_pdf_analysis(message: types.Message):
    if message.from_user.id in ADMINISTRATORS_IDS:
        analysis_text = answer_analysis()
        if analysis_text:
            pdf_file_path = create_pdf_analysis(analysis_text)
            with open(pdf_file_path, "rb") as file:
                pdf_document = types.FSInputFile(path=pdf_file_path)
                await message.answer_document(document=pdf_document)
        else:
            await message.answer("Нет данных для анализа.")
    else:
        await message.answer("У вас нет доступа к этой команде.")



def is_admininistrator(user_id):
    return user_id in ADMINISTRATORS_IDS




def create_full_database_xlsx():
    conn = sqlite3.connect('answers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7, answer_8,"
                   " answer_9, answer_10, answer_11, answer_12, answer_13,"
                   " answer_14, answer_15, answer_16, answer_17 FROM answers")
    answers = cursor.fetchall()
    conn.close()
    workbook = Workbook()
    sheet = workbook.active
    column_headers = ["ID", "User ID"] + [questions[i] for i in range(1, 18)]
    sheet.append(column_headers)
    for answer in answers:
        sheet.append(answer)
    xlsx_file_path = 'full_answers_database.xlsx'
    workbook.save(xlsx_file_path)
    return xlsx_file_path


@dp.message(lambda message: message.text == 'Все ответы XLSX')
async def send_full_database_xlsx(message: types.Message):
    if message.from_user.id in ADMINISTRATORS_IDS:
        xlsx_file_path = create_full_database_xlsx()
        xlsx_document = types.FSInputFile(xlsx_file_path)
        await message.answer_document(document=xlsx_document)
    else:
        await message.answer("У вас нет доступа к этой команде.")



@dp.message(CommandStart())
async def cmd_start(message:Message, state: FSMContext):
    if message.from_user.id in ADMINISTRATORS_IDS:
        await message.answer('Здравствуйте, хотите посмотреть результаты опроса?',
                             reply_markup=get_administrator_keyboard())
    else:
        await state.update_data(Start='Старт')
        await message.answer('Здравствуйте, сейчас вам будет предоставлен '
                         'тест для котнтроля вашего здоровья, если вы готовы'
                         ' нажмите кнопку СТАРТ', reply_markup=keyboard_start())
        await state.set_state(Questions.question_1)


async def ask_question(message: types.Message, state: FSMContext, question_number: int, markup):
    await message.answer(questions[question_number], reply_markup=markup)
    await state.update_data(question_number=question_number)


@dp.message(Questions.question_1)
async def answer_question_1(message: types.Message, state:FSMContext):
    await state.update_data(answer_1=message.text)
    await ask_question(message, state, 1, None)
    await state.set_state(Questions.question_2)


@dp.message(Questions.question_2)
async def answer_question_2(message: types.Message, state:FSMContext):
    await state.update_data(answer_2=message.text)
    await ask_question(message, state, 2, None)
    await state.set_state(Questions.question_3)


@dp.message(Questions.question_3)
async def answer_question_3(message: types.Message, state:FSMContext):
    await state.update_data(answer_3=message.text)
    await ask_question(message, state, 3, Keyboard_q3)
    await state.set_state(Questions.question_4)


@dp.message(Questions.question_4)
async def answer_question_4(message: types.Message, state:FSMContext):
    await state.update_data(answer_4=message.text)
    await ask_question(message, state, 4, Keyboard_q4)
    await state.set_state(Questions.question_5)


@dp.message(Questions.question_5)
async def answer_question_5(message: types.Message, state:FSMContext):
    await state.update_data(answer_5=message.text)
    await ask_question(message, state, 5, Keyboard_q5)
    await state.set_state(Questions.question_6)


@dp.message(Questions.question_6)
async def answer_question_6(message: types.Message, state:FSMContext):
    await state.update_data(answer_6=message.text)
    await ask_question(message, state, 6, Keyboard_q6_q9)
    await state.set_state(Questions.question_7)


@dp.message(Questions.question_7)
async def answer_question_7(message: types.Message, state:FSMContext):
    await state.update_data(answer_7=message.text)
    await ask_question(message, state, 7, Keyboard_q7_q8_q11_q12_q13_q15)
    await state.set_state(Questions.question_8)


@dp.message(Questions.question_8)
async def answer_question_8(message: types.Message, state:FSMContext):
    await state.update_data(answer_8=message.text)
    await ask_question(message, state, 8, Keyboard_q7_q8_q11_q12_q13_q15)
    await state.set_state(Questions.question_9)


@dp.message(Questions.question_9)
async def answer_question_9(message: types.Message, state:FSMContext):
    await state.update_data(answer_9=message.text)
    await ask_question(message, state, 9, Keyboard_q6_q9)
    await state.set_state(Questions.question_10)


@dp.message(Questions.question_10)
async def answer_question_10(message: types.Message, state:FSMContext):
    await state.update_data(answer_10=message.text)
    await ask_question(message, state, 10, Keyboard_q10)
    await state.set_state(Questions.question_11)


@dp.message(Questions.question_11)
async def answer_question_11(message: types.Message, state:FSMContext):
    await state.update_data(answer_11=message.text)
    await ask_question(message, state, 11, Keyboard_q7_q8_q11_q12_q13_q15)
    await state.set_state(Questions.question_12)


@dp.message(Questions.question_12)
async def answer_question_12(message: types.Message, state:FSMContext):
    await state.update_data(answer_12=message.text)
    await ask_question(message, state, 12, Keyboard_q7_q8_q11_q12_q13_q15)
    await state.set_state(Questions.question_13)


@dp.message(Questions.question_13)
async def answer_question_13(message: types.Message, state:FSMContext):
    await state.update_data(answer_13=message.text)
    await ask_question(message, state, 13, Keyboard_q7_q8_q11_q12_q13_q15)
    await state.set_state(Questions.question_14)


@dp.message(Questions.question_14)
async def answer_question_14(message: types.Message, state:FSMContext):
    await state.update_data(answer_14=message.text)
    await ask_question(message, state, 14, Keyboard_q14)
    await state.set_state(Questions.question_15)


@dp.message(Questions.question_15)
async def answer_question_15(message: types.Message, state:FSMContext):
    await state.update_data(answer_15=message.text)
    await ask_question(message, state, 15, Keyboard_q7_q8_q11_q12_q13_q15)
    await state.set_state(Questions.question_16)


@dp.message(Questions.question_16)
async def answer_question_16(message: types.Message, state:FSMContext):
    await state.update_data(answer_16=message.text)
    await ask_question(message, state, 16, Keyboard_q16)
    await state.set_state(Questions.question_17)


@dp.message(Questions.question_17)
async def answer_question_17(message: types.Message, state:FSMContext):
    await state.update_data(answer_17=message.text)
    await ask_question(message, state, 17, Keyboard_q17)
    await state.set_state(Questions.question_18)



@dp.message(Questions.question_18)
async def answer_question_18(message: types.Message, state:FSMContext):
    await state.update_data(answer_18=message.text)
    await ask_question(message, state, 18, ReplyKeyboardRemove())
    await state.set_state(Questions.question_1)
    data = await state.get_data()
    save_answers(message.from_user.id,  data['answer_1'], data['answer_2'], data['answer_3'], data['answer_4'],
                  data['answer_5'], data['answer_6'], data['answer_7'], data['answer_8'], data['answer_9'],
                  data['answer_10'], data['answer_11'], data['answer_12'], data['answer_13'], data['answer_14'],
                  data['answer_15'], data['answer_16'], data['answer_17'], data['answer_18'])
    await state.set_state(None)
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__=='__main__':
    asyncio.run(main())

