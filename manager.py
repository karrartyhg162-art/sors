import os
import json
import asyncio
import subprocess
from telethon import TelegramClient
import sys

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=4)

async def login_account(phone_number, api_id, api_hash, bot_token):
    session_name = f"session_{phone_number.replace('+', '')}"
    bot_session_name = f"bot_{phone_number.replace('+', '')}"
    
    print(f"\n--- جاري تسجيل الدخول للحساب {phone_number} ---")
    client = TelegramClient(session_name, int(api_id), api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input("الرجاء إدخال الكود الذي وصلك على تيليجرام: ")
        try:
            await client.sign_in(phone_number, code)
        except Exception as e:
            if "SessionPasswordNeededError" in str(type(e)):
                password = input("الرجاء إدخال كلمة المرور (التحقق بخطوتين): ")
                await client.sign_in(password=password)
            else:
                print(f"حدث خطأ أثناء تسجيل الدخول: {e}")
                await client.disconnect()
                return None
                
    print("\nتم تسجيل الدخول بنجاح كحساب مستخدم!")
    await client.disconnect()
    
    print("\n--- جاري التحقق من بوت التحكم ---")
    bot_client = TelegramClient(bot_session_name, int(api_id), api_hash)
    await bot_client.start(bot_token=bot_token)
    print("تم الاتصال ببوت التحكم بنجاح!")
    await bot_client.disconnect()
    
    return {
        "phone_number": phone_number,
        "api_id": api_id,
        "api_hash": api_hash,
        "bot_token": bot_token,
        "session_name": session_name,
        "bot_session_name": bot_session_name,
        "db_uri": f"sqlite:///{session_name}.db"
    }

def add_account():
    print("\n=== إضافة حساب جديد ===")
    phone_number = input("أدخل رقم الهاتف (مع رمز الدولة، مثال: +964...): ").strip()
    api_id = input("أدخل الـ API_ID: ").strip()
    api_hash = input("أدخل الـ API_HASH: ").strip()
    bot_token = input("أدخل توكن البوت (الخاص بهذا الحساب): ").strip()
    
    loop = asyncio.get_event_loop()
    account_data = loop.run_until_complete(login_account(phone_number, api_id, api_hash, bot_token))
    
    if account_data:
        accounts = load_accounts()
        # Remove if exists
        accounts = [acc for acc in accounts if acc["phone_number"] != phone_number]
        accounts.append(account_data)
        save_accounts(accounts)
        print("\n[+] تم حفظ الحساب بنجاح وإضافته إلى القائمة.")
    else:
        print("\n[-] فشل في إضافة الحساب.")

def run_all_accounts():
    accounts = load_accounts()
    if not accounts:
        print("\nلا توجد حسابات مضافة. الرجاء إضافة حساب أولاً.")
        return
        
    print(f"\n=== جاري تشغيل {len(accounts)} حساب(حسابات) ===")
    processes = []
    
    for acc in accounts:
        env = os.environ.copy()
        env["APP_ID"] = str(acc["api_id"])
        env["API_HASH"] = acc["api_hash"]
        env["TG_BOT_TOKEN"] = acc["bot_token"]
        env["SESSION_NAME"] = acc["session_name"]
        env["BOT_SESSION_NAME"] = acc["bot_session_name"]
        env["DB_URI"] = acc["db_uri"]
        
        print(f"[*] تشغيل الحساب: {acc['phone_number']}")
        # Run python -m zthon
        p = subprocess.Popen([sys.executable, "-m", "zthon"], env=env)
        processes.append(p)
        
    print("\n[+] جميع الحسابات تعمل الآن في الخلفية.")
    print("اضغط Ctrl+C لإيقاف جميع الحسابات.")
    
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\n[!] جاري إيقاف جميع الحسابات...")
        for p in processes:
            p.terminate()
        print("تم الإيقاف.")

def main():
    while True:
        print("\n" + "="*30)
        print("مدير حسابات الحارس الذكي (Multi-Accounts Manager)")
        print("="*30)
        print("1. إضافة حساب جديد")
        print("2. تشغيل جميع الحسابات المضافة")
        print("3. عرض الحسابات المضافة")
        print("4. الخروج")
        
        choice = input("\nاختر (1-4): ").strip()
        
        if choice == '1':
            add_account()
        elif choice == '2':
            run_all_accounts()
        elif choice == '3':
            accounts = load_accounts()
            print("\n=== الحسابات المضافة ===")
            if not accounts:
                print("لا توجد حسابات مضافة.")
            else:
                for i, acc in enumerate(accounts, 1):
                    print(f"{i}. رقم الهاتف: {acc['phone_number']} | الجلسة: {acc['session_name']}")
        elif choice == '4':
            print("خروج...")
            break
        else:
            print("خيار غير صالح.")

if __name__ == "__main__":
    main()
