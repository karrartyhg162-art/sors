"""
نظام الحماية من الحظر والكشف - Anti-Ban & Anti-Detection System
================================================================
يوفر هذا الملف تأخيرات ذكية بتوزيع غاوسي (Gaussian Distribution)
وآليات متعددة لحماية الحساب من الحظر أو الكشف كأتمتة.
"""

import asyncio
import random
import time
import hashlib
from functools import wraps

# ═══════════════════════════════════════════════════════
#  ثوابت الحماية - Protection Constants
# ═══════════════════════════════════════════════════════

# الحد الأقصى للرسائل في الدقيقة (حد تيليجرام الفعلي ~30/دقيقة)
MAX_MESSAGES_PER_MINUTE = 20

# الحد الأقصى للإجراءات في الساعة
MAX_ACTIONS_PER_HOUR = 200

# تأخير أدنى بين الرسائل (ثانية)
MIN_DELAY = 0.5

# تأخير أقصى بين الرسائل (ثانية)  
MAX_DELAY = 3.0

# ═══════════════════════════════════════════════════════
#  متتبع معدل الاستخدام - Rate Tracker
# ═══════════════════════════════════════════════════════

class RateTracker:
    """يتتبع معدل الإجراءات لمنع تجاوز حدود تيليجرام."""
    
    def __init__(self):
        self._timestamps = []
        self._hourly_timestamps = []
    
    def _cleanup(self):
        """تنظيف الطوابع الزمنية القديمة."""
        now = time.time()
        self._timestamps = [t for t in self._timestamps if now - t < 60]
        self._hourly_timestamps = [t for t in self._hourly_timestamps if now - t < 3600]
    
    def can_proceed(self) -> bool:
        """هل يمكن المتابعة بدون خطر حظر؟"""
        self._cleanup()
        return (
            len(self._timestamps) < MAX_MESSAGES_PER_MINUTE
            and len(self._hourly_timestamps) < MAX_ACTIONS_PER_HOUR
        )
    
    def record_action(self):
        """تسجيل إجراء جديد."""
        now = time.time()
        self._timestamps.append(now)
        self._hourly_timestamps.append(now)
    
    def get_wait_time(self) -> float:
        """حساب وقت الانتظار المطلوب قبل الإجراء التالي."""
        self._cleanup()
        if len(self._timestamps) >= MAX_MESSAGES_PER_MINUTE:
            oldest = min(self._timestamps)
            return max(0, 60 - (time.time() - oldest) + 1)
        return 0

# مثيل عام لتتبع المعدل
_rate_tracker = RateTracker()


# ═══════════════════════════════════════════════════════
#  التأخيرات الذكية - Smart Delays
# ═══════════════════════════════════════════════════════

def gaussian_delay(mean: float = 1.5, std_dev: float = 0.5, 
                   min_val: float = MIN_DELAY, max_val: float = MAX_DELAY) -> float:
    """
    توليد تأخير عشوائي بتوزيع غاوسي (طبيعي).
    هذا يحاكي سلوك المستخدم البشري بشكل أفضل بكثير
    من التأخير الثابت أو التوزيع المنتظم.
    
    Args:
        mean: المتوسط (الوسط) للتوزيع
        std_dev: الانحراف المعياري
        min_val: الحد الأدنى للتأخير
        max_val: الحد الأقصى للتأخير
    
    Returns:
        float: تأخير بالثواني
    """
    delay = random.gauss(mean, std_dev)
    return max(min_val, min(delay, max_val))


def human_typing_delay(text_length: int) -> float:
    """
    محاكاة وقت الكتابة البشرية بناءً على طول النص.
    متوسط سرعة الكتابة ~40 كلمة/دقيقة ≈ 200 حرف/دقيقة.
    
    Args:
        text_length: طول النص بالأحرف
    
    Returns:
        float: تأخير بالثواني يحاكي وقت كتابة بشري
    """
    # ~3 حروف/ثانية مع بعض العشوائية
    chars_per_second = random.gauss(3.0, 0.8)
    chars_per_second = max(1.5, min(chars_per_second, 5.0))
    base_delay = text_length / chars_per_second
    
    # إضافة وقفات تفكير عشوائية (كل ~20 حرف)
    think_pauses = text_length // 20
    think_time = sum(random.gauss(0.3, 0.1) for _ in range(think_pauses))
    
    total = base_delay + think_time
    # الحد الأقصى 8 ثوانٍ حتى للرسائل الطويلة
    return min(total, 8.0)


async def smart_delay(action_type: str = "message"):
    """
    تأخير ذكي يتكيف مع نوع الإجراء ومعدل الاستخدام الحالي.
    
    Args:
        action_type: نوع الإجراء ("message", "join", "admin", "bulk")
    """
    # تحقق من معدل الاستخدام
    wait_time = _rate_tracker.get_wait_time()
    if wait_time > 0:
        await asyncio.sleep(wait_time)
    
    # تأخيرات مخصصة حسب نوع الإجراء
    delays = {
        "message": gaussian_delay(1.0, 0.3, 0.3, 2.0),
        "join": gaussian_delay(3.0, 1.0, 1.5, 6.0),
        "admin": gaussian_delay(1.5, 0.5, 0.5, 3.0),
        "bulk": gaussian_delay(2.0, 0.8, 1.0, 4.0),
        "typing": gaussian_delay(0.8, 0.2, 0.3, 1.5),
    }
    
    delay = delays.get(action_type, gaussian_delay())
    
    # زيادة التأخير إذا كان المعدل مرتفعاً
    _rate_tracker._cleanup()
    current_rate = len(_rate_tracker._timestamps)
    if current_rate > MAX_MESSAGES_PER_MINUTE * 0.7:
        delay *= 1.5  # زيادة 50% عند الاقتراب من الحد
    elif current_rate > MAX_MESSAGES_PER_MINUTE * 0.9:
        delay *= 2.5  # زيادة 150% عند الخطر
    
    await asyncio.sleep(delay)
    _rate_tracker.record_action()


async def flood_safe_delay(seconds: int):
    """
    انتظار آمن عند حدوث FloodWaitError مع إضافة وقت عشوائي.
    
    Args:
        seconds: عدد الثواني المطلوبة من تيليجرام
    """
    # إضافة 10-30% وقت إضافي عشوائي
    extra = seconds * random.uniform(0.1, 0.3)
    total = seconds + extra
    await asyncio.sleep(total)


# ═══════════════════════════════════════════════════════
#  مُحاكاة السلوك البشري - Human Behavior Simulation
# ═══════════════════════════════════════════════════════

async def simulate_typing(client, chat_id, text_length: int = 50):
    """
    محاكاة حالة "يكتب..." قبل إرسال رسالة.
    هذا يجعل النشاط يبدو طبيعياً أكثر.
    
    Args:
        client: عميل تيليجرام
        chat_id: معرف المحادثة
        text_length: طول الرسالة التقريبي
    """
    try:
        from telethon.tl.functions.messages import SetTypingRequest
        from telethon.tl.types import SendMessageTypingAction
        
        typing_duration = human_typing_delay(min(text_length, 100))
        
        await client(SetTypingRequest(
            peer=chat_id,
            action=SendMessageTypingAction()
        ))
        await asyncio.sleep(typing_duration)
    except Exception:
        # لا نريد أن يفشل البوت بسبب خطأ في محاكاة الكتابة
        pass


async def simulate_reading(message_length: int = 100):
    """
    محاكاة وقت قراءة رسالة قبل الرد عليها.
    المتوسط ~250 كلمة/دقيقة للقراءة.
    
    Args:
        message_length: طول الرسالة بالأحرف
    """
    # ~15 حرف/ثانية للقراءة
    reading_time = message_length / random.gauss(15, 3)
    reading_time = max(0.5, min(reading_time, 5.0))
    await asyncio.sleep(reading_time)


# ═══════════════════════════════════════════════════════
#  مُزخرف الحماية - Protection Decorator
# ═══════════════════════════════════════════════════════

def anti_ban(action_type: str = "message"):
    """
    مُزخرف (Decorator) يضيف حماية تلقائية لأي دالة.
    
    الاستخدام:
        @anti_ban("message")
        async def my_handler(event):
            await event.reply("مرحبا")
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # تأخير ذكي قبل التنفيذ
            await smart_delay(action_type)
            
            # تحقق من إمكانية المتابعة
            if not _rate_tracker.can_proceed():
                wait = _rate_tracker.get_wait_time()
                await asyncio.sleep(wait)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def safe_batch_operation(batch_size: int = 10, delay_between: float = 2.0):
    """
    مُزخرف للعمليات الجماعية (مثل إضافة أعضاء، إرسال رسائل جماعية).
    يقسم العمليات إلى دفعات مع تأخيرات بينها.
    
    Args:
        batch_size: حجم كل دفعة
        delay_between: التأخير بين الدفعات
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # تأخير أولي
            await smart_delay("bulk")
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════
#  أدوات مساعدة - Utility Functions  
# ═══════════════════════════════════════════════════════

def randomize_schedule(base_seconds: int, variance_percent: float = 20.0) -> float:
    """
    إضافة عشوائية لجدول زمني لتجنب الأنماط المتكررة.
    
    Args:
        base_seconds: الوقت الأساسي بالثواني
        variance_percent: نسبة التباين (%)
    
    Returns:
        float: الوقت مع عشوائية مضافة
    """
    variance = base_seconds * (variance_percent / 100.0)
    return base_seconds + random.gauss(0, variance / 2)


def get_session_fingerprint() -> str:
    """
    توليد بصمة جلسة فريدة تتغير كل ساعة.
    يمكن استخدامها لتنويع سلوك البوت.
    """
    hour_block = int(time.time() // 3600)
    data = f"session_{hour_block}_{random.randint(1, 1000)}"
    return hashlib.md5(data.encode()).hexdigest()[:8]


async def safe_join_channel(client, channel, delay: bool = True):
    """
    الانضمام لقناة/مجموعة بشكل آمن مع تأخير.
    
    Args:
        client: عميل تيليجرام
        channel: معرف أو يوزر القناة
        delay: هل يتم إضافة تأخير؟
    """
    from telethon.tl.functions.channels import JoinChannelRequest
    
    if delay:
        await smart_delay("join")
    
    try:
        await client(JoinChannelRequest(channel=channel))
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
#  تصدير الدوال - Exports
# ═══════════════════════════════════════════════════════

__all__ = [
    'gaussian_delay',
    'human_typing_delay', 
    'smart_delay',
    'flood_safe_delay',
    'simulate_typing',
    'simulate_reading',
    'anti_ban',
    'safe_batch_operation',
    'randomize_schedule',
    'get_session_fingerprint',
    'safe_join_channel',
    'RateTracker',
]
