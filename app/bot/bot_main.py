from datetime import datetime
from os import getenv

from aiogram import Dispatcher, F
from aiogram import html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from app.bot.buttons.inline import make_inline_buttons
from app.bot.buttons.reply import make_reply_buttons
from database.models import User

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


class UsersState(StatesGroup):
    name = State()
    age = State()
    gender = State()


class DeleteUser(StatesGroup):
    waiting_for_id = State()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Assalamu alaykum - {html.bold(message.from_user.full_name)}")
    buttons = ['🆔 Get my Telegram ID', '👤 Add user', '👥 Get users']
    markup = make_reply_buttons(buttons, size=[1, 2])
    await message.answer('Select menu 👇', reply_markup=markup)


@dp.message(F.text.contains('Get my Telegram ID'))
async def get_id_handler(message: Message) -> None:
    telegram_id = message.from_user.id
    await message.answer(f"🆔 Your ID: {html.code(telegram_id)}", parse_mode="HTML")
    buttons = ['🆔 Get my Telegram ID', '👤 Add user', '👥 Get users']
    markup = make_reply_buttons(buttons, size=[1, 2])
    await message.answer('Select menu 👇', reply_markup=markup)


@dp.message(F.text == '👤 Add user')
async def warning_user_handler(message: Message) -> None:
    buttons = ['👌 I agree', '❌ Disagree']
    markup = make_reply_buttons(buttons=buttons, size=[1], repeat=True)
    await message.answer('⚠️ Everyone can see your data\nDo you want to continue?', reply_markup=markup)


@dp.message(F.text == '❌ Disagree')
async def disagree_handler(message: Message) -> None:
    buttons = ['🆔 Get my Telegram ID', '👤 Add user', '👥 Get users']
    markup = make_reply_buttons(buttons, size=[1, 2])
    await message.answer('Select menu 👇', reply_markup=markup)


@dp.message(F.text == '👌 I agree')
async def agree_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(UsersState.name)
    await message.answer('⌨️ Enter your name: ', reply_markup=ReplyKeyboardRemove())


@dp.message(UsersState.name)
async def name_age_handler(message: Message, state: FSMContext) -> None:
    name = message.text
    await state.set_data({'name': name})
    await state.set_state(UsersState.age)
    await message.answer(text='🔢 Send your age: ')


@dp.message(UsersState.age)
async def age_gender_handler(message: Message, state: FSMContext) -> None:
    age = message.text
    await state.update_data({'age': age})
    await state.set_state(UsersState.gender)
    buttons = ['🚹 Male', '🚺 Female']
    markup = make_reply_buttons(buttons, size=[2])
    await message.answer('Select your gender: ', reply_markup=markup)


@dp.message(UsersState.gender)
async def gender_handler(message: Message, state: FSMContext) -> None:
    gender = message.text if message.text in ['🚹 Male', '🚺 Female'] else None
    await state.update_data({'gender': gender})
    data = await state.get_data()
    data.update({"gender": gender})
    await state.clear()
    await state.set_data(data)
    username = message.from_user.username if message.from_user.username else None
    buttons = ['Confirm ✅', 'Cancel ❌']
    markup = make_reply_buttons(buttons, size=[2])
    await message.answer(f"Confirm your details:\n\n"
                         f"👤 Name: {data.get('name')}\n"
                         f"🔢 Age: {data.get('age')}\n"
                         f"🚻 Gender: {data.get('gender')}\n"
                         f"🔤 Username: {username}", reply_markup=markup)


@dp.message(F.text == 'Confirm ✅')
async def gender_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    user_id = message.from_user.id
    name = str(data.get('name'))
    try:
        age = int(data.get('age'))
    except Exception as e:
        buttons = ['👤 Add user', '👥 Get users']
        markup = make_reply_buttons(buttons, size=[2])
        await message.answer('Age format is invalid️❗️', reply_markup=markup)
    gender = str(data.get('gender'))
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = message.from_user.username if message.from_user.username else None
    try:
        user = {
            'id': user_id,
            'name': name,
            'age': age,
            'gender': gender,
            'saved_at': current_datetime,
            'username': username
        }
        User(**user).save()
        await state.clear()
        buttons = ['🆔 Get my Telegram ID', '👤 Add user', '👥 Get users']
        markup = make_reply_buttons(buttons, size=[1, 2])
        await message.answer('Saved successfully ✅\n\nSelect menu 👇', reply_markup=markup)
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        buttons = ['🆔 Get my Telegram ID', '👤 Add user', '👥 Get users']
        markup = make_reply_buttons(buttons, size=[1, 2])
        await message.answer('Failed to save to database. ❌\n\nSelect menu 👇', reply_markup=markup)


@dp.message(F.text == 'Cancel ❌')
async def gender_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    buttons = ['🆔 Get my Telegram ID', '👤 Add user', '👥 Get users']
    markup = make_reply_buttons(buttons, size=[1, 2])
    await message.answer('Canceled ❌\n\nSelect menu 👇', reply_markup=markup)


@dp.message(F.text == '👥 Get users')
async def get_users_handler(message: Message) -> None:
    if message.from_user.id == "ADMIN'S ID FOR DELETING USERS":
        users = User().get()
        if not users:
            await message.answer("No users found in the database.")
            return
        else:
            for user in users:
                buttons_data = [("🗑 Delete user", f"delete_user:{user.id}")]
                markup = make_inline_buttons(buttons_data)

                await message.answer(
                    f"🆔 ID: {html.code(user.id)}\n"
                    f"👤 Name: {user.name}\n"
                    f"🔤 Username: @{user.username}\n"
                    f"🔢 Age: {user.age}\n"
                    f"🚻 Gender: {user.gender}\n"
                    f"⌚️ Saved at: {user.saved_at}",
                    reply_markup=markup
                )
    else:
        users: list[User] = User().get()
        if users:
            for i, user in enumerate(users):
                await message.answer(f"№ {html.bold(i + 1)}\n"
                                     f"👤 Name: {user.name}\n"
                                     f"🔢 Age: {user.age}\n"
                                     f"🚻 Gender: {user.gender}\n"
                                     f"⌚️ Saved at: {user.saved_at}\n"
                                     f"🔤 Username: {user.username}\n")
            buttons = ['🆔 Get my Telegram ID', '👤 Add user', '👥 Get users']
            markup = make_reply_buttons(buttons, size=[1, 2])
            await message.answer('Select menu 👇', reply_markup=markup)
        else:
            await message.answer('❌ Not users found')


@dp.callback_query(F.data.startswith("delete_user:"))
async def process_delete_user_callback(callback:CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    try:
        User(id=user_id).delete()
        await callback.answer("User deleted!")
        await callback.message.edit_text(f"✅ User with ID {user_id} has been deleted.")

    except Exception as e:
        print(f"Error deleting user: {e}")
        await callback.answer("An error occurred.", show_alert=True)