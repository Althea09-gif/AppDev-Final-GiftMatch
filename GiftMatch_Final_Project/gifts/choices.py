RECIPIENT_CHOICES = [
    ('partner', 'Partner'),
    ('family', 'Family'),
    ('friend', 'Friend'),
    ('coworker', 'Coworker'),
]

OCCASION_CHOICES = [
    ('birthday', 'Birthday'),
    ('anniversary', 'Anniversary'),
    ('monthsary', 'Monthsary'),
    ('graduation', 'Graduation'),
    ('christmas', 'Christmas'),
    ('new_year', 'New Year'),
    ('valentines', "Valentine's Day"),
    ('mothers_day', "Mother's Day"),
    ('fathers_day', "Father's Day"),
    ('family_reunion', 'Family Reunion'),
    ('wedding', 'Wedding'),
    ('baby_shower', 'Baby Shower'),
    ('promotion', 'Promotion'),
    ('retirement', 'Retirement'),
    ('other', 'Other Special Event'),
]

STORE_CHOICES = [
    ('Shopee', 'Shopee'),
    ('Lazada', 'Lazada'),
    ('TikTok Shop', 'TikTok Shop'),
    ('Temu', 'Temu'),
    ('Other', 'Other'),
]

MARKETPLACE_CHOICES = [
    ('any', 'Any Marketplace'),
    ('Shopee', 'Shopee'),
    ('Lazada', 'Lazada'),
    ('TikTok Shop', 'TikTok Shop'),
    ('Temu', 'Temu'),
]

RECIPIENT_OCCASION_MAP = {
    'partner': ['anniversary', 'valentines', 'monthsary', 'birthday', 'christmas'],
    'family': ['mothers_day', 'fathers_day', 'family_reunion', 'birthday', 'christmas', 'new_year'],
    'friend': ['birthday', 'graduation', 'christmas', 'new_year'],
    'coworker': ['birthday', 'promotion', 'retirement', 'christmas', 'graduation'],
}
