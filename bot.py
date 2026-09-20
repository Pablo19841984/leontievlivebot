import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types

TOKEN = "8715848937:AAH-wFcvVPHl4cGk43kvNCm38HhkMFyr6Hw"
ADMIN_ID = "-5179878586"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    name = State()
    problem = State()
    consequences = State()
    goal = State()
    readiness = State()

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Ваша проблема?")
    await state.set_state(Form.problem)

@dp.message(Form.problem)
async def process_problem(message: types.Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await message.answer("Последствия, если не решить?")
    await state.set_state(Form.consequences)

@dp.message(Form.consequences)
async def process_consequences(message: types.Message, state: FSMContext):
    await state.update_data(consequences=message.text)
    await message.answer("Желаемый результат?")
    await state.set_state(Form.goal)

@dp.message(Form.goal)
async def process_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer("Готовность (1-10)?")
    await state.set_state(Form.readiness)

@dp.message(Form.readiness)
async def process_readiness(message: types.Message, state: FSMContext):
    data = await state.update_data(readiness=message.text)
    user = message.from_user
    # Получаем ссылку на юзера, если есть username, иначе просто имя
    user_info = f"@{user.username}" if user.username else user.full_name
    
    result = (f"📩 **Новая заявка!**\n"
              f"👤 Отправитель: {user.full_name} ({user_info})\n"
              f"🆔 ID: {user.id}\n\n"
              f"📝 **Анкета:**\n"
              f"Имя: {data['name']}\n"
              f"Проблема: {data['problem']}\n"
              f"Последствия: {data['consequences']}\n"
              f"Цель: {data['goal']}\n"
              f"Готовность: {message.text}")
    
    try:
        await bot.send_message(chat_id="-5179878586", text=result, parse_mode="Markdown")
        await message.answer("Спасибо! Заявка отправлена.")
    except Exception as e:
        await message.answer(f"Ошибка отправки: {e}")
    await state.clear()
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
