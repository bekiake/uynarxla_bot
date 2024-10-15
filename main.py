import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from geo_api import get_geodata
from environs import Env
import asyncio
from model import predict_price


# Define your environment variables
env = Env()
env.read_env()
API_TOKEN = env.str("API_TOKEN")

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # Storage to keep the state
dp = Dispatcher(bot, storage=storage)

# Define the states for the conversation
class States(StatesGroup):
    apartment_floor = State()
    building_floors = State()
    area = State()
    rooms = State()
    state_of_repair = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    location_button = KeyboardButton('Send location', request_location=True)
    location_markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(location_button)
    await message.reply("Salom, Iltimos, joyingizni yuboring", reply_markup=location_markup)

# Handle the location input
@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lng = message.location.longitude
    location_confirm_markup = InlineKeyboardMarkup(one_time_keyboard=True, row_width=2)
    location_confirm_markup.add(InlineKeyboardButton('Ha', callback_data='yes'))
    location_confirm_markup.add(InlineKeyboardButton('Yo\'q', callback_data='no'))
    
    manzil = get_geodata(lat, lng)  # Get the address or info about the location
    await message.reply(f"Joyingiz: {manzil}\nUshbu manzilni tasdiqlaysizmi?", reply_markup=location_confirm_markup)

    # Save the location to user state for further processing
    await state.update_data(location=(lat, lng))

@dp.callback_query_handler(lambda query: query.data in ['yes', 'no'])
async def handle_apartment_data(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        new_callback = InlineKeyboardMarkup()
        new_callback.add(InlineKeyboardButton('✅ Tasdiqlandi', callback_data='confirm'))
        await call.message.edit_reply_markup(new_callback)
        await call.message.reply("Uy qavatini kiriting:\n(Faqat raqamlarda!)")
        await States.apartment_floor.set()  # Set state to apartment_floor
    else:
        location_button = KeyboardButton('Send location', request_location=True)
        location_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(location_button)
        await call.message.reply("Salom, Iltimos, joyingizni yuboring", reply_markup=location_markup)

@dp.callback_query_handler(lambda query: query.data == 'confirm')
async def show_alert(call : types.CallbackQuery):
    await call.answer('✅ Tasdiqlandi', show_alert=True)
    
@dp.message_handler(state=States.apartment_floor)
async def get_apart_floor(message: types.Message, state: FSMContext):
    try:
        apartment_floor = int(message.text)
        await state.update_data(apartment_floor=apartment_floor)
        await message.reply("Binoingiz qancha qavatli?\n(Faqat raqamlarda kiriting!)")
        await States.building_floors.set()  # Set state to building_floors
    except ValueError:
        await message.reply("Faqat raqamlarda kiriting!")
        await States.apartment_floor.set()  # Stay in the same state

@dp.message_handler(state=States.building_floors)
async def get_building_floors(message: types.Message, state: FSMContext):
    try:
        building_floors = int(message.text)
        await state.update_data(building_floors=building_floors)
        await message.reply("Uy maydoni necha kv.m?")
        await States.area.set()  # Set state to area
    except ValueError:
        await message.reply("Faqat raqamlarda kiriting!")
        await States.building_floors.set()  # Stay in the same state
        
@dp.message_handler(state=States.area)
async def get_area(message: types.Message, state: FSMContext):
    try:
        area = int(message.text)
        await state.update_data(area=area)
        await message.reply("Uyda nechta xona bor?")
        await States.rooms.set()  # Set state to rooms
    except ValueError:
        await message.reply("Faqat raqamlarda kiriting!")
        await States.area.set()  # Stay in the same state

@dp.message_handler(state=States.rooms)
async def get_rooms(message: types.Message, state: FSMContext):
    try:
        rooms = int(message.text)
        await state.update_data(rooms=rooms)
        data = await state.get_data()
        apartment_floor = data.get('apartment_floor')
        building_floors = data.get('building_floors')
        area = data.get('area')
        rooms = data.get('rooms')
        lat, lng = data.get('location')
    
    # Here, you would call your price prediction function
        price = predict_price(rooms, area, apartment_floor, building_floors, lat, lng)
    
        await message.reply(f"Uy narxi: ${price}")
        await state.finish()
    except ValueError:
        await message.reply("Faqat raqamlarda kiriting!")
        await States.rooms.set()  # Stay in the same state


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
