# Uynarxla Bot

Uynarxla Bot - bu Telegram bot bo'lib, foydalanuvchilarga Tashkent shahrida kvartira narxlarini baholash imkonini beradi. Bot foydalanuvchilardan joylashuv va kvartira ma'lumotlarini (qavat, umumiy qavatlar, xonalar soni, maydon) oladi va ma'lumotlar to'plamidan foydalanib, 80-90% aniqlik bilan kvartira narxlarini taqdim etadi.

## Asosiy Xususiyatlar
- Foydalanuvchilar joylashuv va kvartira tafsilotlarini kiritish orqali narx baholash.
- 2GIS Geocoder API dan foydalanish.
- Oson o'rnatish va ishlatish uchun qulay interfeys.

## Talablar
- Python 3.8+
- Aiogram 2.25
- [Other required libraries (list them here if any)]

## API Hujjatlari
- [2GIS Geocoder API](https://docs.2gis.com/)

## O'rnatish
1. Repositoriyani klonlang:

    ```bash
    git clone https://github.com/bekiake/uynarxla_bot.git
    cd uynarxla_bot
    ```

2. Virtual muhit yarating va uni faollashtiring:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Qaramliklarni o'rnating:

    ```bash
    pip install -r requirements.txt
    ```

4. `.env` faylini yarating va quyidagi o'zgaruvchilarni qo'shing:

    ```bash
    BOT_TOKEN=your_bot_token
    API_KEY_2GIS=your_2gis_api_key
    ```

## Botni Ishga Tushirish
Botni polling usuli yordamida ishga tushirish uchun:

```bash
python bot.py

```
## Hissa Qo'shish
Repo'ni fork qiling, yangi filial yarating va pull so'rovlarini yuboring. Hissangiz uchun oldindan rahmat!

