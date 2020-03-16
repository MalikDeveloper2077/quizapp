from django.db import models
from django.db.models import F
from django.conf import settings


default_user = settings.AUTH_USER_MODEL

LEVEL_CHOICES = [
    # Profile levels
    ('Бродяга 👨‍🌾', 'бродяга'),
    ('Новобранец 👨‍🎓', 'новобранец'),
    ('Учитель 👩‍🔬', 'учитель'),
    ('Профи 👨‍🎤', 'профи'),
    ('Граф 🧛‍♂️', 'граф'),
    ('Магистр 🧙‍♂️', 'магистр'),
]

LEVEL_XP_VALUES = [
    # level, count of the xp to get it, index in the list
    ('Бродяга 👨‍🌾', 0, 0),
    ('Новобранец 👨‍🎓', 250, 1),
    ('Учитель 👩‍🔬', 420, 2),
    ('Профи 👨‍🎤', 1000, 3),
    ('Граф 🧛‍♂️', 1500, 4),
    ('Магистр 🧙‍♂️', 3000, 5)
]


class Profile(models.Model):
    """Custom profile for a user"""
    user = models.OneToOneField(
        default_user,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    photo = models.ImageField(
        'Фотография',
        upload_to='user_photos/%Y/%m',
        default='../static/img/testuser.png'
    )
    level = models.CharField(
        'Уровень',
        max_length=30,
        choices=LEVEL_CHOICES,
        default=LEVEL_CHOICES[0][0]
    )
    xp = models.PositiveIntegerField('Опыт', default=0)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

    def increase_xp(self, value: int):
        """Increase the user xp

        Increase the user xp by given value in the args

        Args:
            value(int): count of the xp for increasing

        Returns:
            self.xp(int): count of new xp increased

        """
        self.xp += value
        self.save(update_fields=('xp',))

        return self.xp

    def check_level_up(self):
        """Check if the user level should be upgraded"""
        # If the user level is last
        if self.level == LEVEL_CHOICES[-1][0]:
            return False

        for lvl in LEVEL_XP_VALUES:
            if self.level == lvl[0]:
                # lvl is the current user level

                if self.xp < LEVEL_XP_VALUES[lvl[2] + 1][1]:
                    # if self.xp < the next level xp
                    return False

        return True

    def get_next_level(self):
        """Return the next user level"""
        for lvl in LEVEL_XP_VALUES:
            if self.level == lvl[0]:
                return LEVEL_XP_VALUES[lvl[2] + 1][0]

    def level_up(self, level: str):
        """Level up to the next level"""
        self.level = level
        self.save(update_fields=('level',))
